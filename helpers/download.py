import requests # to get image from the web
import shutil # to save it locally
import os
import config as c


def save_all(photos_urls):
    remove_all()
    for url in photos_urls:
        save(url)


def save(photo_url):
    """Save an image on the server"""
    ## Set up the image URL and filename
    filename = photo_url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(photo_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        create_dl_folder()
        with open(c.DOWNLOADS_FOLDER + filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print('Image Couldn\'t be retreived')


def remove_all():
    create_dl_folder()
    for filename in os.listdir(c.DOWNLOADS_FOLDER):
        # construct full file path
        file = c.DOWNLOADS_FOLDER + filename
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)


def create_dl_folder():
    if not os.path.exists(c.DOWNLOADS_FOLDER):
        os.makedirs(c.DOWNLOADS_FOLDER)


def get_relative_paths(absolute_urls):
    relative_paths = []
    for url in absolute_urls:
        relative_paths.append(c.DOWNLOADS_FOLDER + url.split("/")[-1])
    return relative_paths
