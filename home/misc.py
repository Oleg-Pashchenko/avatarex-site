import openpyxl


def get_search_rules(file_id, search_rules):
    if file_id == '':
        return []

    first_row_data = []
    workbook = openpyxl.load_workbook('uploads/' + file_id + '.xlsx')
    sheet = workbook.active
    for row in sheet.iter_rows(min_row=1, max_row=2, values_only=True):
        if not first_row_data:
            first_row_data = list(row)


    rules_view = []
    for k in first_row_data:
        if k in search_rules:
            rules_view.append({'t': k, 'v': search_rules[k]})
        else:
            rules_view.append({'t': k, 'v': ''})
    return rules_view
