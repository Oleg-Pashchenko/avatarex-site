function saveData(mode, pipeline_id) {
    var dataObject = {};
    dataObject["currentUrl"] = window.location.href;
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

    const data = {};*/


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

    }


    const checkboxObject = {
        mode: 'inactive' // По умолчанию чекбокс неактивен
    };
    if (window.location.href.includes('knowledge-mode')) {
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


    const elements = document.querySelectorAll('.rule');
    const qualificationFields = [];

    elements.forEach((element) => {
        const fieldElements = element.querySelectorAll('[name="field-name"], [name="field-value"]');
        const responseElements = element.querySelectorAll('[name^="response-name-"],[name^="number-select-"],[name^="time-select-"]');

        const blockData = {};

        fieldElements.forEach((fieldElement) => {
            const fieldName = fieldElement.name;
            const fieldValue = fieldElement.value;

            // Если поле начинается с "field-name", добавляем его значение как ключ
            if (fieldName.startsWith('field-name')) {
                const key = fieldValue;
                const valueElement = element.querySelector('[name="field-value"]');
                const value = valueElement ? valueElement.value : '';

                blockData[key] = value;
            }
        });

        responseElements.forEach((responseElement, index) => {
            const RespName = responseElement.name;
            const RespValue = responseElement.value;


            blockData[RespName] = RespValue;
        });

        qualificationFields.push(blockData);
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

