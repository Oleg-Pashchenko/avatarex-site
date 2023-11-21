function saveData(mode, pipeline_id) {
    var dataObject = {};
    dataObject["currentUrl"] = window.location.href;

    var boundedSituationsFields = {};
    dataObject['mode'] = mode;
    dataObject['pipeline_id'] = pipeline_id;
    dataObject['qualificationFinished'] = document.getElementById("qualificationFinished").value;
    console.log(dataObject);
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
// Квалификация
const elements = document.querySelectorAll('.rule');
const qualificationFields = [];

elements.forEach((element) => {
    const childElements = element.querySelectorAll('[name^="response-name-"], [name^="number-select-"], [name^="time-select-"], [name="field-name"], [name="field-value"]');

    const blockData = {};
    childElements.forEach((childElement) => {
        const fieldName = childElement.name;
        const fieldValue = childElement.value;
        // Добавьте проверки, если необходимо, и сохраните данные
        blockData[fieldName] = fieldValue;
    });

    // Пример: добавление данных блока в массив
    qualificationFields.push(blockData);
});

// Вывод объекта qualificationFields в консоль для проверки
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

