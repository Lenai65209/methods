import json

import requests as requests

response = requests.get('https://api.github.com/users/Lenai65209/repos')
with open('repos.json', 'w') as f:
    f.write(json.dumps(response.json(), sort_keys=True, indent=4))

with open('repos.json', 'r') as f:
    d = json.load(f)
    dic_response = {}
    print('Список репозиториев:', end='')
    for i in range(len(d)):
        dic_response[f'{i+1}']=d[i]['name']
        print(f'\n{d[i]["name"]}', end='')

with open('repos_name.json', 'w') as f:
    f.write(json.dumps(dic_response, sort_keys=True, indent=4))
