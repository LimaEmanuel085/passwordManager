import requests
import secrets
import string

def gen_password(length=12):
    char = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(char) for _ in range(length))
    return password
password = gen_password()

url = 'http://127.0.0.1:8080/hash'
json = {
    'password': password
}
headers = {
    'content-type': 'application/json'
}

response = requests.post(url, json=json, headers=headers)
print('POST /hash', response.json())

url = 'http://127.0.0.1:8080/verify'
json = response.json()

response = requests.post(url, json=json, headers=headers)
print('POST /verify', response.json())