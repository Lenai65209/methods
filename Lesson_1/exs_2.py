import json

import requests

app_id = 51600575
vk_version = '5.81'
auth_url = f'https://oauth.vk.com/authorize?client_id={app_id}&display=page' \
           f'&&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,' \
           f'notify,photos,wall,email,mail,groups,stats,offline' \
           f'&response_type=token&v={vk_version}'

print(f'Перейдите по ссылке:\n{auth_url}\nдля получения токена доступа.')
access_token: str = input('\nВведите токен доступа: ')

response = requests.get(
    f'https://api.vk.com/method/groups.get?extended=1&fields=bdate&access_token={access_token}&v={vk_version}')
response_json = response.json()
with open('groups.json', 'w') as file:
    json.dump(response_json, file)

print('\nСписок сообществ, на которые вы подписаны')
for group in response_json['response']['items']:
    print(f"{group['name']}")
