from django import forms


class AmoRegisterForm(forms.Form):
    email = forms.CharField(required=True)
    host = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    account_chat_id = forms.CharField(required=True)


class GptDefaultMode(forms.Form):
    CONTEXT_CHOICES = (
        ('gpt-3.5-turbo', 'gpt-3.5-turbo'),
        ('gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k'),
    )

    VOICE_CHOICES = (
        (True, 'active'),
        (False, 'passive')
    )

    context = forms.CharField(widget=forms.Textarea(attrs={'class': 'rounded-value',
                                                           'placeholder': 'Введите ваш контекст запроса'
                                                           }))
    max_tokens = forms.IntegerField(
        min_value=100, required=True, widget=forms.NumberInput(attrs={'class': 'rounded-value',
                                                                      'placeholder': 'от 100 токенов'
                                                                      })
    )
    temperature = forms.FloatField(
        min_value=0, max_value=2, required=True, widget=forms.NumberInput(attrs={'class': 'rounded-value',
                                                                                 'placeholder': 'от 0 до 2'
                                                                                 }
                                                                          ))
    voice_message_detection = forms.ChoiceField(required=True, choices=VOICE_CHOICES,

                                                widget=forms.Select(attrs={'class': 'rounded-value'}))
    model = forms.ChoiceField(choices=CONTEXT_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'rounded-value'}))
    fine_tunel_model_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'rounded-value',
                                                                                        'placeholder': 'Если вы хотите использовать собственную модель укажите ее ID'}))
