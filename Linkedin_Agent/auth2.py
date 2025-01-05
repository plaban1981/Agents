import requests
import json
api_url = 'https://api.linkedin.com/v2/ugcPosts'
credentials = 'credentials.json'

def get_linkedin_id(access_token):
    url = 'https://api.linkedin.com/v2/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        linkedin_id = user_data['id']  # This is your LinkedIn numeric ID
        print(f"Your LinkedIn ID is: {linkedin_id}")
        return linkedin_id
    else:
        print(f"Error fetching LinkedIn ID: {response.content}")
        return None
def read_creds(filename):
    '''
    Store API credentials in a safe place.
    If you use Git, make sure to add the file to .gitignore
    '''
    with open(filename) as f:
        credentials = json.load(f)
    return credentials
credentials = read_creds(credentials)
access_token = credentials['access_token']
print(f"usedid : {get_linkedin_id(access_token)}")
headers = {
    'Authorization': f'Bearer {access_token}',
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/json',
}

post_body = {
    'author': 'urn:li:person:kfW51gr4Ja',
    'lifecycleState': 'PUBLISHED',
    'specificContent': {
        'com.linkedin.ugc.ShareContent': {
            'shareCommentary': {
                'text': 'Check out our latest blog post!',
            },
            'shareMediaCategory': 'ARTICLE',
            'media': [
                {
                    'status': 'READY',
                    'description': {
                        'text': 'Read our latest blog post about LinkedIn API!',
                    },
                    'originalUrl': '<your_blog_post_url>',
                },
            ],
        },
    },
    'visibility': {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
    },
}

response = requests.post(api_url, headers=headers, json=post_body)
if response.status_code == 201:
    print('Post successfully created!')
else:
    print(f'Post creation failed with status code {response.status_code}: {response.text}')
