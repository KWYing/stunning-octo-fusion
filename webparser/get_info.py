import os
import requests
from bs4 import BeautifulSoup as bs


def get_video_info(sku):
    base_url = os.getenv("WIKI")
    # Requests html content
    response = requests.get(f"{base_url}/{sku}/")
    # Soupify
    soup = bs(response.content, 'html.parser')
    # Get Meta data
    meta_data = soup.find('meta', attrs={'name': 'keywords'})
    keywords = meta_data['content'].split(',')
    # Get release date
    release_date = soup.find('meta', attrs={'property': 'video:release_date'})[
        'content'].split('T')[0]
    # Get video duration in minutes
    duration = soup.find('meta', attrs={'property': 'video:duration'})[
        'content']
    return {'actress': keywords[-4],
            'studio': keywords[-2],
            'release_date': release_date,
            'duration': int(duration)}


def download_img(dir_name, file_name, img_url):
    img_data = requests.get(img_url).content
    # Check if img folder exists if not create the folder
    img_dir = os.path.join(os.getenv("IMAGE_PATH"), dir_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # Add the file_name to img folder
    img_name = os.path.join(img_dir, file_name)
    # Saving the image to disk
    with open(img_name, 'wb') as img:
        img.write(img_data)
    # Returning the path to the image
    return img_name


def split_sku(sku):
    # Splitting the sku for differnt use
    name = sku.split('.')[0]
    c, n = name.split('-')[:2]
    c = c.lower()
    return f"{c}{int(n):05d}", c, n

def get_images(sku, is_dmm=True, index=None):
    dmm_base_url = os.getenv("DMM")
    mg_base_url = os.getenv("MGSTAGE")
    # Patching the link for the cover image
    avid, c, n = split_sku(sku)

    def cover_image():
        # Function for getting cover images
        if is_dmm:
            cover_url = f"{dmm_base_url}{avid}/{avid}pl.jpg"
        else:
            cover_url = f"{mg_base_url}{c}/{n}/pb_e_{c}-{n}.jpg"
        # Download image and return the image path
        return download_img(avid, f"{avid}-cover.jpg", cover_url)

    def single_image():
        # Function for getting single images
        if is_dmm:
            image_url = f"{dmm_base_url}{avid}/{avid}jp-{index}.jpg"
        else:
            image_url = f"{mg_base_url}{c}/{n}/cap_e_{index}_{c}-{n}.jpg"
        # Download image and return the image path
        return download_img(avid, f"{avid}-{index:02d}.jpg", image_url)

    if index is None:
        return cover_image()
    return single_image()