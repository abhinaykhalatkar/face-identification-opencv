
# from oneNoteOp.onenoteauth import OneNoteAuth
# from oneNoteOp.onenote import OneNote

# authenticator = OneNoteAuth(client_id="a84beec0-3795-4acb-ba8c-3207c883c346", 
#                             client_secret="Ta-8Q~YeaZImhNY6NodLtUIlzjWddvvwl-N-Ibht", 
#                             redirect_url="http://localhost:8085",
#                             scope='Notes.ReadWrite User.Read')

# onenote_instance = OneNote(client_id="a84beec0-3795-4acb-ba8c-3207c883c346", 
#                             client_secret="Ta-8Q~YeaZImhNY6NodLtUIlzjWddvvwl-N-Ibht", 
#                            redirect_url="http://localhost:8085",
#                            scope='Notes.ReadWrite User.Read')

# token = authenticator.get_token()
import requests

# Your app's details
client_id = 'cb6007b5-cca0-41ec-a488-a10dd5e7819b'
client_secret = '915f8dc0-4ffe-4e2d-8863-616145f2b04f'
tenant_id = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'  
# Endpoint for obtaining the token
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

# Data for the POST request
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'  # This scope indicates that the app requires the permissions defined in the app registration.
}

response = requests.post(token_url, data=token_data)
token_response_data = response.json()

access_token = token_response_data.get('access_token')
