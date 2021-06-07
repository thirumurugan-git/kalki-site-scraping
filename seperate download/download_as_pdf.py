import requests
import os
import json
import img2pdf
from PyPDF2 import PdfFileMerger
import io

path = ""

directory_name = ['kalki', 'mangayar_malar', 'gokulam_tamil', 'gokulam_english', 'diwali_malar']

proxy = {
    "https": 'https://165.22.33.53:8080'
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}



def get_storing_path(stripped_url):
    
    needed_string = stripped_url
    
    magazine = int(needed_string[0])
    
    first_path = os.path.join(path, directory_name[magazine - 1])
    
    original_path = os.path.join(first_path, needed_string[2:] + ".pdf")
    
    return original_path



def download_as_pdf():

    s = requests.Session()

    try:
        for name in directory_name:
            joined_path = os.path.join(path, name)
            os.mkdir(joined_path)
    except:
        pass

    try:
        with open("kalki_images_url.json",'r') as f:
            data = json.load(f)
    except:
        print("json problem")
        return

    replace_path = "https://www.kalkionline.com/imagegallery/archiveimages/"

    for keys in data.keys():
        for url_for_img in data[keys]:
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

            image_bytes = img2pdf.convert(img.content)
            io_bytes = io.BytesIO(image_bytes)
            merge.append(io_bytes)

        path_to_store = get_storing_path(keys)    
        
        merge.write(path_to_store)
        
        print("completed-------", data[keys])
    print("========== over all completed ===========")


if __name__ == "__main__":
    download_as_pdf()