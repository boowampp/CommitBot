import requests
import json
import time
import random
import string
import base64

# github repo info
owner = 'repo owner'
repo = 'repo name'
path = 'repo path (README.md)'
token = 'github temp token'

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_readme():
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        readme_content = content['content']
        sha = content['sha']
        return readme_content, sha
    else:
        raise Exception(f'Error getting README: {response.status_code}')

def update_readme(new_content, sha):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {token}'}
    message = 'Update README with random string'
    content_b64 = base64.b64encode(new_content.encode()).decode()
    data = {
        'message': message,
        'content': content_b64,
        'sha': sha
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print('README updated successfully.')
    else:
        raise Exception(f'Error updating README: {response.status_code}')

while True:
    try:
        readme_content, sha = get_readme()
        random_string = generate_random_string()
        new_readme_content = readme_content + '\n' + random_string
        update_readme(new_readme_content, sha)
        time.sleep(5)
    except Exception as e:
        print(f'An error occurred: {e}')
        break