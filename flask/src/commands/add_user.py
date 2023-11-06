import requests
from dotenv import dotenv_values

env = dotenv_values(".env")
FLASK_APP_URL = f"http://localhost:{env['FLASK_PORT']}/api/register"
user = {
    "username": env['FLASK_USER_NAME'],
    "email": env['FLASK_USER_EMAIL'],
    "password": env['FLASK_USER_PASSWORD']
}
response = requests.post(FLASK_APP_URL, json=user)

if response.status_code == 201:
    print("Add admin user successfully")

else:
    print("Error on adding admin user.", "Status code:", response.status_code)
