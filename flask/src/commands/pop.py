import requests
import base64
from dotenv import dotenv_values

env = dotenv_values(".env")
host = f"http://localhost:{env['FLASK_PORT']}/"

loginUrl = f"{host}/api/login"
credentials = base64.b64encode(f"{env['FLASK_USER_NAME']}:{env['FLASK_USER_PASSWORD']}".encode()).decode()
response = requests.get(loginUrl, headers={'Authorization': f'Basic {credentials}'})

if response.status_code == 200:
    print('Authorise successfully')
    token = response.json()['token']

    print('Please wait for parsing words..')
    popUrl = f"{host}/api/pop"
    response = requests.post(popUrl, json={}, headers={'x-api-key': token})
    if response.status_code == 201:
        print("Parsing complete", response.text)
    else:
        print("Error on parsing")
        print("Status code:", response.status_code)

else:
    print("Can not authorise")
