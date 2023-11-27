import hashlib
import json
import dotenv
import os
import requests
from django.utils import timezone

from home.models import Transactions, Subscriptions

dotenv.load_dotenv()
headers = {
    'content-type': 'application/json'
}
terminal_key = os.getenv('TERMINAL_KEY')
secret_password = os.getenv('SECRET_PASSWORD')


def _sha256_to_string(input_string):
    input_bytes = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()
    return sha256_hash


def get_secret_hash(data):
    secret_array = []
    for k, v in data.items():
        secret_array.append({k: v})
    secret_array.append({'Password': secret_password})
    sorted_data = sorted(secret_array, key=lambda x: next(iter(x.items()), ('', '')))
    concat_str = ''
    for s in sorted_data:
        for k, v in s.items():
            concat_str += str(v)
    return _sha256_to_string(concat_str)


def create_payment(cost, owner_id, sub_type):
    new_transaction = Transactions(
        sub_type=sub_type,
        date=timezone.now().date(),
        amount=cost,
        payment_id="",
        owner_id=owner_id,
        is_finished=False,
    )

    new_transaction.save()

    # Retrieve the ID of the newly created transaction
    transaction_id = new_transaction.id

    url = 'https://securepay.tinkoff.ru/v2/Init'
    data = {
        "TerminalKey": terminal_key,
        "Amount": 100,# cost * 100,
        "OrderId": transaction_id,
        "Description": "Оплата подписки",
    }

    data['Token'] = get_secret_hash(data)
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()
    new_transaction.payment_id = resp['PaymentId']
    new_transaction.save()
    return resp['PaymentURL']


def get_payment_status(payment_id):
    url = 'https://securepay.tinkoff.ru/v2/GetState'
    data = {
        "TerminalKey": terminal_key,
        "PaymentId": payment_id
    }
    data['Token'] = get_secret_hash(data)
    return requests.post(url, data=json.dumps(data), headers=headers).json()


def update(owner_id):
    transactions = Transactions.objects.filter(owner_id=owner_id, is_finished=False)
    for transaction in transactions:
        if transaction.payment_id == '':
            continue
        status_info = get_payment_status(transaction.payment_id)
        print(status_info)
        if status_info['Status'] == 'CONFIRMED':
            transaction.is_finished = True
            transaction.save()

    transactions = Transactions.objects.filter(owner_id=owner_id, is_finished=True)

    for transaction in transactions:
        # Check if the transaction_id exists in Subscriptions
        if not Subscriptions.objects.filter(transaction_id=transaction.id).exists():
            # If not, create a new subscription
            if transaction.sub_type == 1:
                period = 30
            else:
                period = 365 * 3
            new_subscription = Subscriptions(
                date_start=timezone.now().date(),
                period=period,  # Set the period as needed
                owner_id=owner_id,
                transaction_id=transaction.id,
            )
            new_subscription.save()


def get_person_info(owner_id):
    subscriptions = Subscriptions.objects.filter(owner_id=owner_id)
    count = 0
    for subscription in subscriptions:
        current_date = timezone.now().date()
        remaining_days = ((subscription.date_start + timezone.timedelta(days=subscription.period)) - current_date).days
        if int(remaining_days) > 0:
            count += int(remaining_days)

    transactions = Transactions.objects.filter(owner_id=owner_id, is_finished=True)
    return count, transactions


def is_user_new(owner_id):
    return not Subscriptions.objects.filter(owner_id=owner_id).exists()
