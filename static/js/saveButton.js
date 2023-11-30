function saveData(mode, pipeline_id) {
    var dataObject = {};
    dataObject["currentUrl"] = window.location.href;

    dataObject['pipeline_id'] = pipeline_id;
    /*
    var boundedSituationsFields = {};

    dataObject['mode'] = mode;
    dataObject['pipeline_id'] = pipeline_id;

    console.log(dataObject);
    boundedSituationsFields["hi_message"] = document.getElementById("hi-message").value;
    boundedSituationsFields["database_error_message"] = document.getElementById("db-error-message").value;
    boundedSituationsFields["openai_error_message"] = document.getElementById("openai-error-message").value;
    boundedSituationsFields["service_settings_error_message"] = document.getElementById("service_settings_error_message").value;
    dataObject["bounded_situations_fields"] = boundedSituationsFields;

     */

    const data = {};


    if (window.location.href.includes('database')) {
        dataObject["view_rule"] = document.getElementById("view-rule").value;
        dataObject["result_count"] = document.getElementById("results-count").value;
        // Get all the select elements within the #search-rules container
        const selectElements = document.querySelectorAll('#search-rules select');

        selectElements.forEach(selectElement => {
            const parameterName = selectElement.closest('.align-items-center').querySelector('.input-group-text').textContent.trim().replace('Введенный параметр ', '');
            const selectedOperator = selectElement.value;

            data[parameterName] = selectedOperator;
        });
    }


    if (window.location.href.includes('prompt-mode')) {
        const PromptObject = {};

        dataObject['qualificationFinished'] = document.getElementById("qualificationFinished").value;
        const elements = document.querySelectorAll('.rule');
        elements.forEach((element) => {

            const contextElement = document.getElementById('id_context');
            const context = contextElement ? contextElement.value : '';

            const maxTokensElement = document.getElementById('id_max_tokens');
            const maxTokens = maxTokensElement ? maxTokensElement.value : '';

            const temperatureElement = document.getElementById('id_temperature');
            const temperature = temperatureElement ? temperatureElement.value : '';

            const modelElement = document.getElementById('id_model');
            const model = modelElement ? modelElement.value : '';

            const fineTunelModelIdElement = document.getElementById('id_fine_tunel_model_id');
            const fineTunelModelId = fineTunelModelIdElement ? fineTunelModelIdElement.value : '';


            PromptObject.context = context;
            PromptObject.maxTokens = maxTokens;
            PromptObject.temperature = temperature;
            PromptObject.model = model;
            PromptObject.fineTunelModelId = fineTunelModelId;
            dataObject['prompt-data'] = PromptObject;

        });


        const checkboxObject = {
            mode: 'inactive' // По умолчанию чекбокс неактивен
        };
        if (window.location.href.includes('knowledge-mode')) {

            var boundedSituationsFields = {};

            dataObject['mode'] = mode;

            console.log(dataObject);
            boundedSituationsFields["hi_message"] = document.getElementById("hi-message").value;
            boundedSituationsFields["database_error_message"] = document.getElementById("db-error-message").value;
            boundedSituationsFields["openai_error_message"] = document.getElementById("openai-error-message").value;
            boundedSituationsFields["service_settings_error_message"] = document.getElementById("service_settings_error_message").value;
            dataObject["bounded_situations_fields"] = boundedSituationsFields;

            const data = {};


            const knowledgeObject = {};
            const knowledgeBoundedObject = {};
            const elements = document.querySelectorAll('.rule');
            dataObject['qualificationFinished'] = document.getElementById("qualificationFinished").value;
            elements.forEach((element) => {
                    const checkboxObject = {};
                    //const modeCheckbox = element.querySelector('[name="checkbox"]');
                    // Проверяем, активен ли чекбокс
                    //const isModeCheckboxChecked = modeCheckbox ? modeCheckbox.checked : false;


                    if (modeCheckbox.checked === true) {
                        // Чекбокс активен
                        checkboxObject.mode = 'active';
                        dataObject['checkbox'] = checkboxObject;
                        // Чекбокс активен, считываем значения полей ввода и выбора

                        // Чекбокс активен, считываем содержимое textarea и значения других полей
                        const contextElement = document.getElementById('id_context');
                        const context = contextElement ? contextElement.value : '';

                        const maxTokensElement = document.getElementById('id_max_tokens');
                        const maxTokens = maxTokensElement ? maxTokensElement.value : '';

                        const temperatureElement = document.getElementById('id_temperature');
                        const temperature = temperatureElement ? temperatureElement.value : '';

                        const modelElement = document.getElementById('id_model');
                        const model = modelElement ? modelElement.value : '';

                        const fineTunelModelIdElement = document.getElementById('id_fine_tunel_model_id');
                        const fineTunelModelId = fineTunelModelIdElement ? fineTunelModelIdElement.value : '';

                        // Записываем в объект knowledgeObject
                        knowledgeObject.context = context;
                        knowledgeObject.maxTokens = maxTokens;
                        knowledgeObject.temperature = temperature;
                        knowledgeObject.model = model;
                        knowledgeObject.fineTunelModelId = fineTunelModelId;
                        dataObject['knowledge-prompt'] = knowledgeObject;
                    }
                    if (modeCheckbox.checked === false) {
                        // Чекбокс неактивен
                        checkboxObject.mode = 'inactive';
                        dataObject['checkbox'] = checkboxObject;
                        const hiMessageElement = document.getElementById('hi-message');
                        const hiMessage = hiMessageElement ? hiMessageElement.value : '';

                        const openaiErrorMessageElement = document.getElementById('openai-error-message');
                        const openaiErrorMessage = openaiErrorMessageElement ? openaiErrorMessageElement.value : '';

                        const dbErrorMessageElement = document.getElementById('db-error-message');
                        const serviceSettingsErrorMessageElement = document.getElementById('service_settings_error_message');


                        const dbErrorMessage = dbErrorMessageElement ? dbErrorMessageElement.value : '';
                        const serviceSettingsErrorMessage = serviceSettingsErrorMessageElement ? serviceSettingsErrorMessageElement.value : '';

                        // Записываем значения в объект
                        knowledgeBoundedObject.hiMessage = hiMessage;
                        knowledgeBoundedObject.openaiErrorMessage = openaiErrorMessage;
                        knowledgeBoundedObject.dbErrorMessage = dbErrorMessage;
                        knowledgeBoundedObject.serviceSettingsErrorMessage = serviceSettingsErrorMessage;


                    }
                }
            )

            dataObject['knowledge-bounded'] = knowledgeBoundedObject;


        }
    }

    const elements = document.querySelectorAll('.rule');


    const qualificationFields = [];

    elements.forEach((element, order) => {
        const fieldElements = element.querySelectorAll('[name="field-name"], [name="field-value"]');
        const responseElements = element.querySelectorAll('[name^="response_name_"],[name^="number_select_"],[name^="time_select_"]');

        const blockData = {
            'order': order + 1,  // Порядковый номер для родительского словаря
            'field_name': '',
            'question': '',
            'additional_questions': [],
        };

        fieldElements.forEach((fieldElement) => {
            const fieldName = fieldElement.name;
            const fieldValue = fieldElement.value;

            if (fieldName === 'field-name') {
                blockData['field_name'] = fieldValue;
            } else if (fieldName === 'field-value') {
                blockData['question'] = fieldValue;
            }
        });

        let additionalOrder = 1;  // Порядковый номер для дополнительных вопросов

        responseElements.forEach((responseElement, index) => {
            const responseName = responseElement.name;
            const responseValue = responseElement.value;

            // Если поле вопроса не пусто
            if (responseName.trim() !== '') {
                const responseNameElement = element.querySelector(`[name="response_name_${index}"]`);
                const timeNumberElement = element.querySelector(`[name="number_select_${index}"]`);
                const timeTypeElement = element.querySelector(`[name="time_select_${index}"]`);

                const fieldtext = responseNameElement ? responseNameElement.value : '';
                const timeNumber = timeNumberElement ? parseInt(timeNumberElement.value) : 0;
                const timeType = timeTypeElement ? timeTypeElement.value : '';

                // Если вопрос не пустой, добавляем его в массив additional_questions
                if (fieldtext.trim() !== '') {
                    const additionalQuestion = {
                        'order': additionalOrder,  // Порядковый номер для дополнительного вопроса
                        'question': fieldtext,
                        'time_number': timeNumber,
                        'time_type': timeType,
                    };

                    blockData['additional_questions'].push(additionalQuestion);
                    additionalOrder++;  // Увеличиваем порядковый номер для следующего вопроса
                }
            }
        });

        if (blockData['field_name'].trim() !== '' && blockData['question'].trim() !== '') {
            qualificationFields.push(blockData);
        }
    });

    console.log(qualificationFields);


// Ваш дальнейший код
    dataObject['qualification_fields'] = qualificationFields;
    console.log(dataObject);

// Отправка запроса
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataObject),
    };
    fetch(`/api/v1/update-mode/`, requestOptions).then(response => {
            window.location.href = '/home';
        }
    )
}

