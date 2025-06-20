import requests
import subprocess
import time

while True:
    try:
        r=requests.get('https://www.google.com/')
        subprocess.call(['python','main.py'])
        subprocess.call(['python','report_gen.py'])
        break
    except requests.exceptions.ConnectionError:
        print("No Internet: Retrying after One Minute")
        time.sleep(60)
        continue