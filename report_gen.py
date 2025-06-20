from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from datetime import date
from reportlab.lib import colors
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from app.api_functions import authenticate,send_email
import base64
import json,time

doc=SimpleDocTemplate("Phone.pdf",pagesize=A4)

full_data=[]
with open('contacts.json') as file:
    full_data=json.load(file)

data=[
    ['Sl.No','Name','Phone\nNumber','Status','Last\nCalled','Address','works']
]

empty_row=['','','','','','','']
count=0
for cust in full_data:
    contact=[]
    for ph in cust['phone_numbers']:
        try:
            if date.today().year-ph['last_called']>=1:
                count+=1
                name='\n'.join(cust['Cust_Name'].split(' '))
                status='\n'.join(ph['status'].split(' '))
                address='\n'.join(cust['address'].split(','))
                unformatted_works=cust['unformatted_works']
                try:
                    unformatted_works='\n'.join(cust['unformatted_works'].split(':'))
                except AttributeError:
                    pass

                tmp=[count,name,ph['number'],status,
                     ph['last_called'],address,unformatted_works]
                data.append(tmp)
            else:
                break
        except KeyError:
            continue

column_widths = [20, 55, 60, 70, 40, 150, 100]
table = Table(data, colWidths=column_widths)

style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background for rows
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  
    ('FONTSIZE', (0, 0), (-1, -1), 8),  
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
])

table.setStyle(style)
doc.build([table])

print("PDF Generated Successfully")

date_now=f'{date.today().day}-{date.today().month}-{date.today().year}'
msg=MIMEMultipart()
msg['From']='chennaiservice10@gmail.com'
msg['To']='rosalinddevotta@gmail.com'
msg['Subject']=f'Daily Contacts {date_now}'
with open('Phone.pdf','rb') as file:
    msg.attach(MIMEApplication(file.read(),name=f'Phone {date_now}.pdf'))

encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
message = {"raw": encoded_message}

creds=authenticate('people_CLIENT_FILE.json',['https://mail.google.com/'],'report_gen')
send_email(creds,message)
print("Email Sent!")
time.sleep(20)