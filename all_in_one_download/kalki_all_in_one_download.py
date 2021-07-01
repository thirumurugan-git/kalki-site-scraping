import requests

from csv import writer

import os

import img2pdf

from PyPDF2 import PdfFileMerger

import json

import io

from bs4 import BeautifulSoup as bs

path = ""

directory_name = ['kalki', 'mangayar_malar', 'gokulam_tamil', 'gokulam_english', 'diwali_malar']

base_url = "https://www.kalkionline.com"

#proxy = {
#    "https": 'https://165.22.33.53:8080'
#}

proxy = None


headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}


def refined(url):
    ind = url.rfind('/')
    return url[ind+1:].replace('.jpg','')


def write_in_csv(url):
    
    print("csv ------ "+url)
    ind = url.find('/')
    dir = url[:ind]
    file = url[ind+1:]
    name = file.replace(".pdf","")
    date = name.replace(dir,'')
    year = date[:4]
    month = date[5:7]

    csv_file = dir+"/"+dir+"-info.csv"
    if not os.path.isfile(csv_file):
        li = ("identifier", "title", "publisher", "creator", "file", "date", "year", "month", "language", "collection", "mediatype", "source", "subject")
        with open(csv_file, 'w') as f:
            obj = writer(f)
            obj.writerow(li)

    data = [name, dir+" magazine "+date, "", "", file, date, year, month, "tam", "ServantsOfKnowledge", "texts", "KalkiOnline", "Magazine;Tamil Magazine"]
    if dir == directory_name[-2]:
        data[8] = "eng"
        data[-1] = "Magazine;English Magazine"

    with open(csv_file, 'a') as f:
        obj = writer(f)
        obj.writerow(data)

def alpha_numeric_page_number(x):
    try:
        return int(x)
    except:
        pass

    started = False
    sending_number = ""
    for char in x:
        if char.isnumeric():
            started = True
            sending_number += char
        elif started:
            break
    return int(sending_number)

def organizingTechnic(url):
    
    x = refined(url)

    if x=="w1":
        return -2
    if x=="w2":
        return -1
    if x=="w3":
        return 10000
    if x=="w4":
        return 10001

    if "sp" in x:
        return 500+alpha_numeric_page_number(x[2:])

    if "sw" in x:
        return 1500+alpha_numeric_page_number(x[2:])

    if "p" in x:
        return alpha_numeric_page_number(x[1:])

    if "i" in x:
        return 1000+alpha_numeric_page_number(x[1:])

    print("stopped at url (undefined page):" + url)
    print("quiting.....")
    quit()

def set_img_organized(all_img):
    all_img_src = [base_url + tag['src'] for tag in all_img ]
    res = sorted(all_img_src, key = organizingTechnic)
    return res


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

        try:
            html = bs(resp.content, 'html.parser')

            all_img = html.find_all('img')
        except:
            print("error at site: " + url)
            error_images += "***** " + url
            continue
        
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
    
    original_path = os.path.join(first_path, directory_name[magazine - 1]+needed_string[2:] + ".pdf")
    
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
        try:
            html = bs(resp.content, 'html.parser')

            all_img = html.find_all('img')

            merge = PdfFileMerger()
        except:
            print("error at url: " + url)
            error_images += "***** " + url
            continue

        all_img = set_img_organized(all_img)
        
        for url_for_img in all_img:
            #url_for_img = base_url + tag['src']
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
    
        write_in_csv(path_to_store)

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