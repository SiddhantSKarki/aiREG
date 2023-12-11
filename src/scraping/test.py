import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    print(is_available(mapping, ['19743']))






