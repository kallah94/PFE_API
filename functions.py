from flask import jsonify


def cust_jsonify(fields_list, results):
    column_list = []
    for i in fields_list:
        column_list.append(i[0])
    json_data = []
    for row in results:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        json_data.append(data_dict)
    return json_data
