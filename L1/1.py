import json
import requests

user = 'zukapa'
url = f'https://api.github.com/users/{user}/repos'
response = requests.get(url)
json_data = response.json()
for repo in json_data:
    print(repo['full_name'])
with open('repo.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, indent=2, ensure_ascii=False)
