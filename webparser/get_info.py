"""Module for Web Parser"""
import os
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


def get_html_content(url):
    """Function to get html content from url using requrests"""
    headers = {"Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
                              AppleWebKit/537.36 (KHTML, like Gecko) \
                              Chrome/113.0.0.0 Safari/537.36"}
    return requests.get(url, headers=headers, timeout=360).content


def get_first_result(sku):
    """Function to get the first result from site"""
    url = os.getenv('URL') or "https://jav.guru/?s="
    soup = bs(get_html_content(f'{url}{sku}'), 'html.parser')
    main_site = soup.find('main')
    row = main_site.find('div', {'class': 'row'})
    return row.find('a').get('href')


def get_video_info(sku):
    """Function to get video info from site"""
    link = get_first_result(sku)
    soup = bs(get_html_content(link), 'html.parser')
    article = soup.body.find('div', {'class': 'inside-article'})
    # Empty dic
    dic = {'sku': sku}
    # english title
    dic['title'] = article.find('h1', {'class': 'titl'}).text
    # metainfo
    meta = article.find('div', {'class': 'infometa'}).find_all('li')
    # loop to find info
    for _m in meta:
        lst = _m.text.split(':')
        if len(lst) > 1:
            k = lst[0]
            # Getting info if key matches
            if k in ['Actress', 'Studio']:
                # Remove extra spaces in values
                dic[k.lower()] = lst[1].strip()
            elif k == 'Release Date':
                dic['release_date'] = datetime.strptime(
                    lst[1].strip(), "%Y-%m-%d")
    # cover image
    img_url = article.find(
        'div', {'class': 'large-screenimg'}).find('img').get('src')
    # download image
    img_path = download_img(sku, img_url.split('/')[-1], img_url)
    dic['cover_image'] = img_path
    # Create at
    dic['create_at'] = datetime.now()
    return dic


def download_img(dir_name, file_name, img_url):
    """Function for download the image"""
    img_data = get_html_content(img_url)
    # Check if img folder exists if not create the folder
    image_dir = os.getenv("IMAGE_PATH") or "images"
    img_dir = os.path.join(image_dir, dir_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # Add the file_name to img folder
    img_name = os.path.join(img_dir, file_name)
    # Saving the image to disk
    with open(img_name, 'wb') as img:
        img.write(img_data)
    # Returning the path to the image
    return img_name


if __name__ == '__main__':
    _sku = input("Enter SKU: ")
    print(get_video_info(_sku))
