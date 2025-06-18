import os,json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def authenticate(CLIENT_FILE,SCOPES:list,purpose:str):
    creds=None
    if os.path.exists(f'{purpose}_token.json'):
        creds=Credentials.from_authorized_user_file(f'{purpose}_token.json',SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(CLIENT_FILE,SCOPES)
            creds=flow.run_local_server(port=0)
        with open(f'{purpose}_token.json','w') as token:
            token.write(creds.to_json())
    return creds

creds = authenticate('people_CLIENT_FILE.json',['https://www.googleapis.com/auth/contacts'],'people')

def get_contacts(creds):
    people_service=build('people','v1', credentials=creds)

    data=[]
    next_page_token=None
    while True:
        people = people_service.people().connections().list(resourceName='people/me',personFields='names,emailAddresses,addresses',pageToken=next_page_token).execute()
        try:
            next_page_token=people["nextPageToken"]
        except KeyError:
            break
        print(len(data))
        data.append(people)
        
    with open('contacts.json','w') as file:
        json.dump(data,file,indent=4)
        print('Created file contacts.json successfully')
    return 0