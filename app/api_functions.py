import os,json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date
import time
import sys

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

def fetch_contacts(creds):
    people_service=build('people','v1', credentials=creds)

    data=[]
    next_page_token=None
    while True:
        try:
            people = people_service.people().connections().list(resourceName='people/me',personFields='names,emailAddresses,addresses,phoneNumbers,biographies',
                                                                    pageSize=1000,pageToken=next_page_token).execute()
            connections = people.get('connections', [])
            next_page_token = people.get("nextPageToken")
            data.append(people)
            print(f"Contacts fetched: {len(connections)}")
            if not next_page_token:
                break
        except HttpError:
            time.sleep(0.5)
            continue
        
    with open('unformatted_contacts.json','w',encoding='utf-8') as file:
        json.dump(data,file,indent=4)
        print('Created file unformatted_contacts.json successfully')
    return 0

def send_email(creds,create_message):
    send_message=None
    try:
        gmail_service=build('gmail','v1',credentials=creds)
        send_message = (gmail_service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        sys.exit(1)
    return send_message

def update_contact_email(creds,contact:dict):
    people_service=build('people','v1',credentials=creds)
    day=date.today().day
    month=date.today().month
    year=int(str(date.today().year)[2:])
    today=f'{day}.{month}.{year}'
    resourceName=contact['resourceName']

    temp=None
    with open('unformatted_contacts.json','r',encoding='utf-8') as file:
        temp=json.load(file)
    
    required_contact=None
    for list_of_contacts in temp:
        list_of_contacts=list_of_contacts['connections']
        for c in list_of_contacts:
            if c['etag']==contact['etag'] and c['resourceName']==resourceName:
                required_contact=c
                break
    
    required_contact['emailAddresses'][0]['type']=f'Mail Sent on {today}'
    required_contact['emailAddresses'][0]['formattedType']=f'Mail Sent on {today}'
    person={
        'resourceName':resourceName,
        'etag':contact['etag'],
        'emailAddresses':required_contact['emailAddresses']
    }
    return people_service.people().updateContact(resourceName=resourceName,body=person,personFields='emailAddresses',
                                          updatePersonFields='emailAddresses').execute()