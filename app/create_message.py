import re,os

import markdown
import base64
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

img_path='images/'

def capitalize_first_letter(string,seperator=' '):
    try:
        str_list=string.split(seperator)
        final_str_list=[]
        for str in str_list:
            str=str.lower()
            final_str_list.append(str[0].upper()+str[1::])
        return ' '.join(final_str_list)
    except IndexError:
        return string

def create_message(cust_dict,From_address='chennaiservice4@gmail.com'):
    if not cust_dict['email']:
        print(f'Empty Email : {cust_dict['Cust_Name']}')
        return -1
    
    CONST_rupee='&#x20B9;'
    name_present=True
    if not cust_dict['name']:
        name_present=False
    
    name=''
    if not name_present:
        if re.search(r'[Cc]ust  ?(\w+)',cust_dict['Cust_Name'])[1].lower()=='dr' or re.search(r'[Cc]ust  ?(\w+)',cust_dict['Cust_Name'])[1].lower()=='captain' or len(re.search(r'[Cc]ust  ?(\w+)',cust_dict['Cust_Name'])[1])==1:
            name=re.search(r'[Cc]ust  ?(\w+[ \.&]+\w+)',cust_dict['Cust_Name'])[1]
        else:
            name=re.search(r'[Cc]ust  ?(\w+)',cust_dict['Cust_Name'])[1]

    phone_numbers=[]
    for ph in cust_dict['phone_numbers']:
        phone_numbers.append(ph['number'])
    if name_present:
        message_content=f'<b>Dear {cust_dict['name']}</b><br>' + r' \ '.join(phone_numbers) + '<br><br>'
    else:
        if re.search(r'[Cc]ust  ?(\w+)',cust_dict['Cust_Name'])[1].lower()=='dr':
            message_content=f'<b>Dear {name}</b><br>' + r' \ '.join(phone_numbers) + '<br><br>'
        else:
            message_content=f'<b>Dear Customer {name}</b><br>' + r' \ '.join(phone_numbers) + '<br><br>'

    work_given=True
    for work in cust_dict['works']:
        if type(work) is dict:
            work_given=True
            break
        else:
            work_given=False

    if 'mrs' in cust_dict['name'].lower():
            message_content+='Madam, '
    elif 'mr' in cust_dict['name'].lower():
        message_content+='Sir, '
    else:
        if name_present:
            message_content+=cust_dict['name'] + ', '
        else:
            message_content+=name + ', '

    if work_given:
        message_content+='Thank you very much for'

        works=[]
        for work in cust_dict['works']:
            if type(work) is dict:
                works.append(work)
        count=1
        #print(cust_dict['works'])
        if len(works)>1:
            message_content+=':<br>'
            for work in works:
                message_content+=f'{count}. <b>{capitalize_first_letter(work['type'])}</b> work in {work['year']} for {CONST_rupee}{work['cost'].split('\u20b9')[-1]}<br>'
                count+=1
            message_content+=f'at {cust_dict['area']}<br>'
        elif len(works)==1:
            work=works[0]
            message_content+=f' <b>{capitalize_first_letter(work['type'])}</b> work in {work['year']} for {CONST_rupee}{work['cost'].split('\u20b9')[-1]}<br>'
            message_content+=f'at {cust_dict['area']}<br>'
        else:
            message_content+=f" We are a company called <b>CHENNAI SERVICE</b> You've previously enquired us about our works. I humbly request you to have a look at our other services.<br>"
    else:
        work=''
        if re.search(r'for \w+',cust_dict['works'][-1]):
            work=re.findall(r'for \w+',cust_dict['works'][-1])[-1]
        year=cust_dict['works'][-1].split(':')[0].lower()
        message_content+=f"You've enquired us {work} work {year}. I humbly request you to have a look at our other services.<br>"
    
    message_content+='<br>The other <b>Products</b> dealt by us are:<br>'

    final_msg_md='''<br>
If you require any of our services, kindly call us <b>(8807 311 417)</b><br>
Our representative will visit your place at your <b>CONVENIENT</b> date and time<br><br>
I've attached some <b>photos</b> of our services. I would be grateful if you could take a look at them.<br><br>
Please refer our company if any of your friends or relatives require our services<br><br>
<b>CHENNAI SERVICE</b><br>
59 / 117, strahans road, pattalam, chennai - 600 012<br>
<b>8807 311 417 / 7418 699 683 /98400 32488</b><br><br>
Regards<br>
Truly yours<br>
For Chennai Service<br>
R.Rosalind Devotta'''

    table_html='''<table style="border: 1px solid black; border-collapse: collapse;">
<thead>
<tr style="border: 1px solid black; padding: 10px;">
<th style="border: 1px solid black; padding: 10px; text-align: center;">S.No</th>
<th style="border: 1px solid black; padding: 10px; text-align: center;">Products</th>
<th style="border: 1px solid black; padding: 10px; text-align: center;">Types</th>
</tr>
</thead>
<tbody>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">1</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>Mosquito Nets</b> for windows</td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">Velcro type, window type, pleated type, mosquito net door</td>
</tr>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">2</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>Curtains</b> and <b>Rods</b></td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">-</td>
</tr>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">3</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>Blinds</b></td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">Roman, vertical, roller, PVC, Bamboo, Honey comb blinds (A/ C prevention)</td>
</tr>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">4</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>Sofa Relining</b></td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">foam changing, fabric changing, sofa top covers, dining chairs relining</td>
</tr>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">5</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>PVC Cupboard Work</b></td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">-</td>
</tr>
<tr style="border: 1px solid black; padding: 10px;">
<td style="border: 1px solid black; padding: 10px; text-align: center;">6</td>
<td style="border: 1px solid black; padding: 10px; text-align: left;"><b>Sun Control films</b></td>
<td style="border: 1px solid black; padding: 10px; text-align: center;">-</td>
</tr>
</tbody>
</table>'''

    font_style='''<style>
           p {
               font-family: "Calibri", sans-serif;
               font-size: 16px;
               font-style: normal;
           }
       </style>'''

    initial_msg=markdown.markdown(message_content)
    final_msg=markdown.markdown(final_msg_md)

    message_content=font_style + initial_msg + table_html + final_msg

    msg=MIMEMultipart()
    msg['To']=cust_dict['email']
    msg['From']=From_address
    msg['Subject']='CHENNAI SERVICE - Reg Services Rendered'

    body=MIMEText(message_content,'html')
    #msg.add_header('Content-Type','text/html')
    #msg.set_payload(message_content)
    msg.attach(body)

    files=os.listdir(img_path)
    for img in files:
        with open(f'{img_path}{img}','rb') as file:
            msg.attach(MIMEApplication(file.read(),name=os.path.basename(f'{img_path}{img}')))
    message=None
    try:
        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        message = {"raw": encoded_message}
    except UnicodeEncodeError:
        print(f'Error:{cust_dict['Cust_Name']}')
    return message


# obsolete:
#table='''|S.No| Products                         |      Types            |
#|:--:| :------                         |:--------:        |
#| 1  | <b>Mosquito Nets</b> for windows|Velcro type, window type, pleated type, mosquito net door |
#| 2  | <b>Curtains</b> and <b>Rods</b> |-                  |
#| 3  | <b>Blinds</b>|Roman, vertical, roller, PVC, Bamboo Honey comb blinds (A/ C prevention) |
#| 4 | <b>Sofa Relining</b>|foam changing, fabric changing, sofa top covers, dining chairs relining|
#| 5 | <b>PVC Cupboard Work</b>|-|
#| 6 | <b>Sun Control films</b>|-|'''