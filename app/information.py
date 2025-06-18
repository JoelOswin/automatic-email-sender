import re,os,json


def get_information():
    if not os.path.exists('temp.json'):
        print("contacts.json does not exist")
        return -1
    
    contacts_unformatted=[]
    with open('temp.json', 'r') as file:
        contacts_unformatted=json.load(file)

    contacts=[]
    defaulters_address=[]
    defaulters_emails=[]
    defaulters_phone=[]

    for list_of_contacts in contacts_unformatted:
        list_of_contacts=list_of_contacts['connections']
        
        for contact in list_of_contacts:
            cust={}
            if 'cust' in contact['names'][0]['displayName'].lower():
                Cust_Name=contact['names'][0]['displayName']
                address_full=''
                try:
                    address_full=contact['addresses'][0]['formattedValue']
                    if not address_full:
                        raise KeyError
                except KeyError:
                    defaulters_address.append(Cust_Name)

                email=None
                try:
                    email=contact['emailAddresses'][0]['value']
                    if not email:
                        raise KeyError
                except KeyError:
                    defaulters_emails.append(Cust_Name)
                
                unformatted_address=list(re.split(r'[\n.]+',address_full)) # unformatted address with name and extra details
                
                name=''
                for item in unformatted_address:
                    if re.search(r'Mrs? \w+',item):
                        name=re.findall(r'Mrs? \w+', item)[0] # name with mr or mrs

                area=''
                try:
                    if re.search(r'(.*[\n ]+.*)?[Cc]hennai',address_full):
                        address=re.search(r'(.*[\n ]+.*)?[Cc]hennai',address_full)[0].split(',')
                        area=address[-2].strip()
                except IndexError:
                    address=re.search(r'(.*[\n ]+.*)?[Cc]hennai',address_full)[0].split(',')[-1].split('\n')
                    area=address[-2].strip()
                    if not area:
                        defaulters_address.append(Cust_Name)
                except KeyError:
                    pass

                email_sent_year=None
                try:
                    email_sent_year=int('20' + re.findall(r'[0-9]+.[0-9]+.[0-9]+',contact['emailAddresses'][0]['type'])[-1].split('.')[-1])
                except IndexError:
                    email_sent_year=2023
                except ValueError:
                    email_sent_year=int('20' + re.findall(r'[0-9]+.[0-9]+.[0-9]+',contact['emailAddresses'][0]['type'])[-1].split(' ')[-1])
                except KeyError:
                    pass
                
                works=[]
                try:
                    notes=contact['biographies'][0]['value']
                    unformatted_works=list(re.split(r'[\n]+', notes))
                    for i in unformatted_works:
                        if 'in' not in i.lower():
                            unformatted_works.remove(i)

                    works=[] # works in proper format will be stored here
                    for item in unformatted_works:
                        work={}
                        work['type']=re.split(r'[()]+',re.findall(r'\(.*\)',item)[0])[1].strip()
                        work['year']=re.findall(r' [0-9][0-9][0-9][0-9] ', item)[0].strip()
                        work['cost']=re.findall(r'₹[0-9]+',item)[0].strip()
                        works.append(work)
                except KeyError:
                    pass
                except IndexError:
                    works.append(contact['biographies'][0]['value'])

                cust['Cust_Name']=Cust_Name
                cust['name']=name
                cust['area']=area
                cust['email']=email
                cust['email_sent_year']=email_sent_year
                cust['works']=works
                cust['address']=address_full

                cust['phone_numbers']=[]
                try:
                    for ph in contact['phoneNumbers']:
                        temp={'number':ph['value'], 'status':ph['type']}

                        last_called=None
                        try:
                            tmp=re.findall(r'[0-9]+.[0-9]+.[0-9]+',ph['type'])[-1].split('.')[-1]
                            last_called=int('20' + tmp)
                        except ValueError:
                            last_called=int('20' + re.findall(r'[0-9]+.[0-9]+.[0-9]+',ph['type'])[-1].split(' ')[-1])
                        except IndexError:
                            cust['phone_numbers'].append(temp)
                            continue

                        temp.update({'last_called':last_called})
                        cust['phone_numbers'].append(temp)
                except KeyError:
                    defaulters_phone.append(Cust_Name)

                contacts.append(cust)

    with open('contacts.json','w',encoding='utf-8') as file:
        json.dump(contacts,file,indent=4)
        print("Successfully created contacts.json")