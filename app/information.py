import csv,re,os,json


def get_information():
    if not os.path.exists('contacts.json'):
        print("contacts.json does not exist")
        return -1
    contacts_unformatted=[]
    with open('contacts.json', 'r') as file:
        contacts_unformatted=json.load(file)
    contacts=[]
    for contact in contacts_unformatted:
        pass

def get_contacts(csv_file_name):
    '''Argument must be a csv file name downloaded directly from google contacts\n
    Returns only the necessary details in list format where each customer is stored as a dictionary'''

    keys=['First Name','Middle Name','Last Name','Notes','E-mail 1 - Label','E-mail 1 - Value','Phone 1 - Label','Phone 1 - Value','Phone 2 - Value',
            'Address 1 - Formatted','Address 1 - Street','Address 1 - City','Address 1 - Extended Address']

    reader=None
    with open(csv_file_name,'r',encoding='utf-8') as file:
        reader=csv.DictReader(file)
    customers=[]
    # reader will have all the contacts
    for contact in list(reader):
        if 'cust' in contact['First Name'].lower():
            cust={}
            for key in contact:
                if key in keys:
                    cust[key]=contact[key]

            unformatted_address=list(re.split(r'[\n.]+',cust['Address 1 - Formatted'])) # unformatted address with name and extra details

            name=''
            for item in unformatted_address:
                if re.search(r'Mrs? \w+',item):
                    name=re.findall(r'Mrs? \w+', item)[0] # name with mr or mrs
            
            area=''
            for item in unformatted_address:
                if re.search(r'[Cc]hennai',item):
                    address=re.split(r',',item)
                    area=address[-2].strip()

            phone_numbers=[] # will contain the list of phone numbers
            if cust['Phone 1 - Value']: phone_numbers.append(cust['Phone 1 - Value'])
            if cust['Phone 2 - Value']: phone_numbers.append(cust['Phone 2 - Value'])

            unformatted_works=list(re.split(r'[\n]+', cust['Notes']))
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

            try:
                full_date=re.findall(r'[0-9]+\.[0-9]+\.[0-9]+',cust['E-mail 1 - Label'])[-1]
                email_sent_year='20' + full_date.split('.')[-1]
            except IndexError:
                email_sent_year=''
                print("E-mail 1 - Label is empty")
            
            try:
                full_date=re.findall(r'[0-9]+\.[0-9]+\.[0-9]+',cust['Phone 1 - Label'])[-1]
                last_called='20' + full_date.split('.')[-1]
            except IndexError:
                last_called=''
                print("Phone 1 - Label is empty")

            final_cust={} # all the required details of customer will be compiled here
            
            if cust['Last Name'].strip() and cust['Middle Name'].strip():
                final_cust['Cust_Name']=cust['First Name'].strip() + ' ' + cust['Middle Name'].strip() + ' ' + cust['Last Name'].strip()
            elif cust['Middle Name'].strip():
                final_cust['Cust_Name']=cust['First Name'].strip() + ' ' + cust['Middle Name'].strip()
            else:
                final_cust['Cust_Name']=cust['First Name'].strip()

            final_cust['name']=name
            final_cust['phone_numbers']=phone_numbers
            final_cust['last_called']=last_called.strip()
            final_cust['email']=cust['E-mail 1 - Value'].strip()
            final_cust['email_sent_year']=email_sent_year.strip()
            final_cust['area']=area
            final_cust['works']=works
            customers.append(final_cust)
    return customers

# people.googleapis.com