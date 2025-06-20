from app.api_functions import authenticate,fetch_contacts,update_contact_email
from app.api_functions import send_email
from app.get_information import get_information
from app.create_message import create_message
from datetime import date
import json
import time

# fetch contacts
creds = authenticate('people_CLIENT_FILE.json',['https://www.googleapis.com/auth/contacts'],'people')
return_code=fetch_contacts(creds)
if return_code==0:
    print("Contacts fetched successfully")

# save fetched contacts
return_code=get_information()
if return_code==-1:
    print("ERROR!")
else:
    print("Contacts saved successfully")

contacts=[]
with open('contacts.json','r',encoding='utf-8') as file:
    contacts=json.load(file)


creds_gmail=authenticate('gmail_CLIENT_FILE.json',['https://mail.google.com/'],'gmail')
creds_people=authenticate('people_CLIENT_FILE.json',['https://www.googleapis.com/auth/contacts'],'people')

for contact in contacts:
    if not contact['email']:
        continue
    if (date.today().year-contact['email_sent_year'])<2:
        continue
    send_email(creds_gmail,create_message(contact))
    update_contact_email(creds_people,contact)
print('Success! Emails sent and contacts updated successfully')
time.sleep(20)