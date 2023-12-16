import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import smtplib

def is_available(mapping, excep = []):
    available = []
    classes = mapping['ENROLLMENT/CAPACITY']
    for i in range(len(classes)):
        texts = classes[i].split('/')
        if int(texts[0]) < int(texts[1]):
            if mapping['CRN'][i] not in excep:
                available.append((mapping['CRN'][i], mapping['SECTION'][i]))
    if available:
        return True, available 
    else:
        return False, None

def scrape(url, form_data, headers):
    with requests.Session() as session:
        request_g = session.get(url)
        soup_g = BeautifulSoup(request_g.text, 'html.parser')
        csrf_token =  soup_g.find('input', {'name':'_token'})['value']
        form_data['_token'] = csrf_token
        cookies = session.cookies.get_dict()
        request = session.post(url, data=form_data)
        mapping = {}
        soup = BeautifulSoup(request.text, 'html.parser')
        table =  soup.find_all(['tbody', 'thead'])
        columns_h = table[0].find('tr').find_all('th')
        columns_r = table[1].find_all('tr')
        for row in columns_r:
            t_data = row.find_all('td')
            for i in range(len(t_data)):
                col_h = columns_h[i].text.strip().upper()
                col_r = t_data[i].text.strip()
                if col_h not in mapping.keys():
                    mapping[col_h] = []
                mapping[col_h].append(col_r)
        # df = pd.DataFrame(mapping)
        # df.set_index('CRN', inplace=True)
        # df.to_csv('../../raw_data/TEMP1')
        return mapping



form_data = {
    'term' : '202420',
    'campusFilter[]' : ['O'],
    'subject[]' : ['CSE'],
    'courseNumber' : '432'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url = 'https://www.apps.miamioh.edu/courselist/'
excep = ['1974']


def run(interval_sec = 5):
    i = 0
    scraped_dict = scrape(url, form_data, headers)
    while not is_available(scraped_dict,excep)[0]:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(f"Time elapsed: {(interval_sec * i)} sec / {(interval_sec * i)/60:0.5} minutes / {(interval_sec * i)/60/60:0.2} hrs")
        time.sleep(interval_sec) 
        scraped_dict = scrape(url, form_data, headers)
        i+=1
    return True, i, is_available(scraped_dict,excep)[1]

def send_mail(sender, receiver, classes):
    msg = f"Subject:CLASS FOUND\r\nFrom:{sender}\r\nTo:{receiver}\r\nClasses found are: \n"
    for i in range(len(classes)):
        msg += f"{i+1}. " + str(classes[i]) + '\n'
    server = smtplib.SMTP(host='mailfwd.miamioh.edu', port=25)
    server.set_debuglevel(1)
    server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg)
    server.quit()

def send_mail_err(sender, receiver, subject, other):
    # sender += "@miamioh.edu"
    # receiver += "@miamioh.edu"
    msg = f"Subject:{subject}\r\nFrom:{sender}\r\nTo:{receiver}\r\n{other}"
    server = smtplib.SMTP(host='mailfwd.miamioh.edu', port=25)
    server.set_debuglevel(1)
    server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg)
    server.quit()


if __name__ == '__main__':
    try:
        intervals = 60
        stat , sec, classes = run(intervals)
        if stat:
            send_mail("karkiss@miamioh.edu", "karkiss@miamioh.edu", classes)
            print(f"Class Found after {intervals * sec} seconds later")
    except Exception as e:
        send_mail_err("karkiss@miamioh.edu", 'karkiss@miamioh.edu', "ERROR - WATCH", f"ERROR HAS OCCURED IN the watch:\n{e.__cause__}")