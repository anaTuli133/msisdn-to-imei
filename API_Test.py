import requests

url = "http://127.0.0.1:8000/api/"

headers = {
    "Content-Type": "application/json",
    "x-api-key": "your-secret-key"
}

payload = {
    "msisdn": ["8801550155096"],
    "start_date": "2026-01-30",
    "end_date": "2026-01-31"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())

#Rahi Sir Number
#8801550155096