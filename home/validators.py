from typing import Optional

from django.core.exceptions import ValidationError
from pydantic import BaseModel, Field
from pydantic.v1 import validator

import ssl
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from home import models


class BoundedSituationsFields(BaseModel):
    hi_message: str = Field(min_length=1)
    openai_error_message: str = Field(min_length=1)
    database_error_message: str = Field(min_length=1)
    service_settings_error_message: str = Field(min_length=1)


class UpdateModeValidator(BaseModel):
    qualification_fields: dict = Field(validation_alias='qualification_fields')
    qualification_finished: str = Field(validation_alias='qualificationFinished')
    bounded_situations_fields: dict = Field(validation_alias='bounded_situations_fields')
    database_mode_fields: dict = Field(validation_alias='database_mode_fields')
    mode: str = Field(min_length=1)

    @validator('mode')
    def validate_mode(self, v):
        modes = ['knowledge', 'database', 'd_k']
        if v not in modes:
            raise ValueError(f"Мод должен быть один из: {modes}")
        return v

    @validator('bounded_situations_fields')
    def validate_qualification_fields(self, v):
        try:
            BoundedSituationsFields(**v)
        except ValidationError as er:
            print(er)
        return v


class PromptModeValidator(BaseModel):
    context: str = Field(min_length=1)
    tokens_limit: int = Field(gt=100, lt=16000, validation_alias='max_tokens')
    temperature: int = Field(multiple_of=2)
    model: str = Field(min_length=1, validation_alias='model')
    qualification_finished: str = Field(min_length=1, validation_alias='qualificationFinished')
    # qualification_fields: models.ForeignKey
    fine_tuned_model_id: Optional[int] = Field(None, alias='fine_tuned_id')

    @validator('model')
    def validate_model(cls, v: str):
        models = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k']
        if v not in models:
            raise ValueError(f'Модель должна быть одна из: {models}')
        return v


# class UpdateModeValidator(BaseModel):
#     qualification: models.ModeQualification
#     bounded_situations: models.ModeMessages
#
#     # @validator('qualification')
#     # def validate_qualification(self, v):
#     #     print(v)
#     #     print("\n")
#     #
#     # @validator('bounded_situations')
#     # def validate_bounded_situations(self, v):
#     #     print(v)
#     #     print("\n")


def validate_google_doc(link):
    # Create an SSL context that does not verify the server's certificate
    ssl_context = ssl._create_unverified_context()

    request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request, context=ssl_context) as response:
        content = response.read().decode("utf-8")
        soup = BeautifulSoup(content, 'html.parser')
        td_elements = soup.find_all('td', class_='s0')
        is_valid = round(len(td_elements) / 2) >= 2
        if not is_valid:
            raise ValidationError("Таблица должна содержать минимум 2 строчки")

    return link
