import json

alert_data={
    "Threat_type":"SQL Injection",
    "Severity":"High",
    "is_reserved":False
}
print("-------------------Before--------------")

print(alert_data)
print(type(alert_data))

json_string=json.dumps(alert_data) #Using dumps() method to convert Python to json

print("---------------After using dumps() method---------------")

print(json_string)
print(type(json_string))

alert_data_dict=json.loads(json_string)  #Using loads() mathods to convert json to Python

print("---------------After using loads() method---------------")
print(alert_data_dict)
print(type(alert_data_dict))