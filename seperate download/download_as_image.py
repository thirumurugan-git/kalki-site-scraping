import requests
import os
import json

path = ""

proxy = {
    "https": 'https://165.22.33.53:8080'
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}



def download_as_image():

    error_images = ""

    s = requests.Session()

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
        
        print("completed-------", data[keys])
    
    with open("error_images.txt",'w') as f:
        f.write(error_images)

    print("========== over all completed ===========")


if __name__ == "__main__":
    download_as_image()