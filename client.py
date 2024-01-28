import json
import requests

url = "http://localhost:3000"

data = {
    "username": "example_user",
    "message": "Hello, server!"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.text)