# Scrapper tool for kalkionline.com

This is a tool to scrape website kalkionline.com

# How to start

Initially we need to run Initializing_file_to_get_all_url_for_each_book.py

This file is exports json_sites.json. This json file collects all of the url that is responsible for each book. We can use this to get all books.

You don't need to run this script. Because, I already collected this file. 

# Two option to download

# Download through single code 

In 'all_in_one_download' directory, there will be kalki_all_in_one_download.py file. run this script

you will be asked to download as pdf or image. Give input as 1 if pdf else 2

Then you will be asked to enter, from which url you need to start download. this is because, if the code quites we can use the last site visited to start from. If you want from start you can use 'n' as input. 

**Note: I already downloaded sites_json.json you don't need to get this file by running initial file

# Download seperatly

There is a another option, to download seperately. use 'seperate download' directory to download seperately. Run first kalki_image_url_to_json, this will produce 'kalki_images_url.json'. Using this we can get the order of images in kalki books.

Then if you want to download as pdf, use 'download_as_pdf' script else use 'download_as_image'.

***Note Download through single code is preferred.
