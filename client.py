import json
import requests

url = "http://localhost:3000/message"  # Ось зміна шляху на /message
data = {
    "username": "example_user",
    "message": "Hello, server!"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)  # Замінено data=json.dumps(data) на json=data

print(response.status_code)
print(response.text)