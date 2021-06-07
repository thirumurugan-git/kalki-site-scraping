import requests

import sys

import time

import json

from bs4 import BeautifulSoup as bs

base_url = "https://www.kalkionline.com/archivessale/"

url = "https://www.kalkionline.com/archivessale/magdisp5.php?q="

proxy = {
    "https": 'https://165.22.33.53:8080'
    #"https": 'https://206.189.101.228:8080'
}

headers = headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}

ranges = ((1943,2010),(1981,2010),(1972,2010),(1988,2010),(1943,1967))

s = requests.Session()

json_sites = { "sites": [] }

maxi_steps = 5
def save_the_json(json_sites):
    with open("json_sites.json",'w') as f:
        json.dump(json_sites, f)


for ind,magazines_yr in enumerate(ranges):
    for j in range(magazines_yr[0], magazines_yr[1]+1):
        curr_url = url + str(ind+1) + "," + str(j)
        print("---------------------"+curr_url+"----------------------------")
        while maxi_steps > 0:
            try:
                resp = s.get(curr_url, proxies = proxy, headers = headers)
                maxi_steps = 5
                break
            except:
                print('cannot get response')
                maxi_steps -= 1
                if maxi_steps == 0:
                    flag = str(input("will you continue: "))
                    maxi_steps = 5
                    if flag == 'n':
                        save_the_json(sites)
                        print('files saved')
                        quit()              
    
        html = bs(resp.content, 'html.parser')
        all_atag = html.find_all('a')
        for tag in all_atag:
            json_sites['sites'].append(base_url + tag['href'])

save_the_json(json_sites)

try:
    with open("json_kalki.txt",'w') as f:
        f.write(str(json_sites))
except:
    print('error occures')

print("=================completed========================")
