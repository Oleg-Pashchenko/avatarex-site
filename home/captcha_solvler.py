from twocaptcha import TwoCaptcha

api_key = "b766f9f6b4bb7a59286bd1b1c1c1daf4"

solver = TwoCaptcha(api_key)
result = ''
try:
    result = solver.recaptcha(
        sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',
        url='https://rucaptcha.com/demo/recaptcha-v2')
except Exception as e:
    print(e)

print(result)
