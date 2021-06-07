import requests
import json
from bs4 import BeautifulSoup as bs

path = ""

directory_name = ['kalki', 'mangayar_malar', 'gokulam_tamil', 'gokulam_english', 'diwali_malar']

base_url = "https://www.kalkionline.com"

proxy = {
    "https": 'https://165.22.33.53:8080'
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}





def download_as_image():

    s = requests.Session()
    
    try:
        with open("json_sites.json") as f:
            data = json.load(f)
    except:
        print("json_sites.json does not exist!")
        return
    
    sites_list = data['sites']

    all_images = {}
    
    for url in sites_list:
        
        print(url)

        max_site_trying = 5
        
        while(True):
            try:
                resp = s.get(url, headers = headers, proxies = proxy)
                break
            except:
                print('cannot get response for ' + url)
                max_site_trying -= 1
                if max_site_trying == 0:
                    user_inp = str(input("maximum trying reached do you want to continue [y/n]: "))
                    if user_inp == 'n':
                        print("last site: "+url)
                        quit()
                    max_site_trying = 5

        html = bs(resp.content, 'html.parser')

        all_img = html.find_all('img')

        taking_url = url[-12:]

        temp = []
        
        for tag in all_img:
            url_for_img = base_url + tag['src']
            temp.append(url_for_img)
            print("------" + url_for_img)

        all_images[taking_url] = temp
    
    with open('kalki_images_url.json','w') as f:
        json.dump(all_images, f)

    print("===============completed===============")

if __name__ == "__main__":
    download_as_image()