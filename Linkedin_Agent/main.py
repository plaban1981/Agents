from linkedin_content_crew import LinkedInContentCrew
from IPython.display import display, Markdown
import requests
import json
api_url = 'https://api.linkedin.com/v2/ugcPosts'
credentials = 'credentials.json'
#read credentials
def read_creds(filename):
    '''
    Store API credentials in a safe place.
    If you use Git, make sure to add the file to .gitignore
    '''
    with open(filename) as f:
        credentials = json.load(f)
    return credentials
#
access_token = read_creds(credentials)['access_token']
#
def post_to_linkedin(content: str) -> str:
        """Post content to LinkedIn"""
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
                        'text': content + "\n\n This Post is created by AI Agent!!!!",
                    },
                    'shareMediaCategory': 'ARTICLE',
                    'media': [
                        {
                            'status': 'READY',
                            'description': {
                                'text': 'Read our latest blog post about LinkedIn API!',
                            },
                            'originalUrl': 'https://nayakpplaban.medium.com/building-an-ai-powered-linkedin-content-post-publishing-pipeline-automating-research-writing-and-a701bd525f79',
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

def main():
    try:
        # Initialize the crew
        print("Initializing LinkedIn Content Crew...")
        content_crew = LinkedInContentCrew()
        
        # Get topic from user
        topic = input("Enter the topic for your LinkedIn post: ")
        print(f"\nStarting content creation and posting process for topic: {topic}")
        
        # Run the complete process
        result = content_crew.run(topic)
        
        # Display results
        print("\nProcess completed successfully!")
        print("\nGenerated Content:")
        print(result['content'])
        print("\nPosting Result:")
        post_to_linkedin(result['content'].raw)
       
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main() 