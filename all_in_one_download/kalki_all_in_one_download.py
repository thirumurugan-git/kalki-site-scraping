import requests

import os

import img2pdf

from PyPDF2 import PdfFileMerger

import json

import io

from bs4 import BeautifulSoup as bs

path = ""

directory_name = ['kalki', 'mangayar_malar', 'gokulam_tamil', 'gokulam_english', 'diwali_malar']

base_url = "https://www.kalkionline.com"

proxy = {
    "https": 'https://165.22.33.53:8080'
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}





def download_as_image():

    error_images = ""

    s = requests.Session()

    replace_path = "https://www.kalkionline.com/imagegallery/archiveimages/"

    start_from = str(input("Enter From which URL want to start (n for do all else type the URL): "))

    s = requests.Session()
    
    try:
        with open("json_sites.json") as f:
            data = json.load(f)
    except:
        print("json_sites.json does not exist!")
        return
    
    sites_list = data['sites']
    
    flag = True
    
    if start_from == 'n':
        flag = False
    
    for url in sites_list:
        
        if flag:
            if start_from == url:
                flag = False
            else:
                continue
        
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

        
        for tag in all_img:
            url_for_img = base_url + tag['src']
            print("------" + url_for_img)
            max_try_img = 5
            while(True):
                try:
                    img = s.get(url_for_img, headers = headers, proxies = proxy)
                    break
                except:
                    max_try_img -= 1
                    print("cannot get responst for image")
                    if max_try_img == 0:
                        user_inp = str(input("maximum trying for image reached do you want to continue [y/n]: "))
                        if user_inp == 'n':
                            print("last site: "+url)
                            quit()
                        max_try_img = 5
            removed_path = url_for_img.replace(replace_path,'')
            storing_path = os.path.join(path, removed_path)

            if not os.path.exists(os.path.dirname(storing_path)):
                try:
                    os.makedirs(os.path.dirname(storing_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            try:
                with open(storing_path, 'wb') as f:
                    f.write(img.content)
            except:
                print("########### " + url_for_img)
                error_images += url_for_img + "\n"

        print("completed", url)

    with open('error_images.txt', 'w') as f:
        f.write(error_images)

    print('================== over all completed =====================')

def get_storing_path(url):
    
    needed_string = url[-12:]
    
    magazine = int(needed_string[0])
    
    first_path = os.path.join(path, directory_name[magazine - 1])
    
    original_path = os.path.join(first_path, needed_string[2:] + ".pdf")
    
    return original_path


def download_as_pdf():
    

    error_images = ""

    start_from = str(input("Enter From which URL want to start (n for do all else type the URL): "))
    
    try:
        for name in directory_name:
            joined_path = os.path.join(path, name)
            os.mkdir(joined_path)
    except:
        pass

    s = requests.Session()
    
    try:
        with open("json_sites.json") as f:
            data = json.load(f)
    except:
        print("json_sites.json does not exist!")
        return
    
    sites_list = data['sites']
    
    flag = True
    
    if start_from == 'n':
        flag = False
    
    for url in sites_list:
        
        if flag:
            if start_from == url:
                flag = False
            else:
                continue
        
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

        merge = PdfFileMerger()

        
        for tag in all_img:
            url_for_img = base_url + tag['src']
            print("------" + url_for_img)
            max_try_img = 5
            while(True):
                try:
                    img = s.get(url_for_img, headers = headers, proxies = proxy)
                    break
                except:
                    max_try_img -= 1
                    if max_try_img == 0:
                        user_inp = str(input("maximum trying for image reached do you want to continue [y/n]: "))
                        if user_inp == 'n':
                            print("last site: "+url)
                            quit()
                        max_try_img = 5
            try:
                image_bytes = img2pdf.convert(img.content)
                io_bytes = io.BytesIO(image_bytes)
                merge.append(io_bytes)
            except:
                print("########### " + url_for_img)
                error_images += url_for_img + "\n"

        path_to_store = get_storing_path(url)    
        
        merge.write(path_to_store)
    
        print("================completed=============== " + path_to_store)
    

    with open("error_images.txt",'w') as f:
        f.write(error_images)


    print('================== over all completed =====================')

if __name__ == "__main__":

    print("select download option!")
    print("1. download as pdf (may be slow)")
    print("2. download as image (fast)")

    option = int(input('choose your option (1 or 2):'))
    
    if option == 1:
        download_as_pdf()
    elif option == 2:
        download_as_image()
    else:
        print("This is not a option")
        print("quiting...")
