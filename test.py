import requests

url = "https://emkc.org/api/v2/piston/execute"

payload = {
    "language": "python3",
    "source": "print('Hello, World!')"
}

response = requests.post(url, json=payload)
result = response.json()

print(result)