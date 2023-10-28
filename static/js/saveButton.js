function saveData(mode, pipeline_id) {
    var dataObject = {};
    dataObject["currentUrl"] = window.location.href;

    var boundedSituationsFields = {};
    dataObject['mode'] = mode;
    dataObject['pipeline_id'] = pipeline_id;
    boundedSituationsFields["hi_message"] = document.getElementById("hi-message").value;
    boundedSituationsFields["database_error_message"] = document.getElementById("db-error-message").value;
    boundedSituationsFields["openai_error_message"] = document.getElementById("openai-error-message").value;
    boundedSituationsFields["service_settings_error_message"] = document.getElementById("service_settings_error_message").value;
    dataObject["bounded_situations_fields"] = boundedSituationsFields;
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


    dataObject['database_mode_fields'] = data;
    const qualificationFelds = {};
// Квалификация
    const elements = document.querySelectorAll('.rule');

    elements.forEach((element) => {
        const fieldNameInput = element.querySelector('[name="field-name"]');
        const fieldValueInput = element.querySelector('[name="field-value"]');
        const fieldName = fieldNameInput.value;
        const fieldValue = fieldValueInput.value;
        qualificationFelds[fieldName] = fieldValue;
    });
    dataObject['qualification_fields'] = qualificationFelds;
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

