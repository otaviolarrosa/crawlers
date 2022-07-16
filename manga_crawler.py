# -*- coding:utf-8 -*-
import os, sys, argparse
import urllib.parse
from requests import get
from urllib.request import urlopen
from urllib.parse import urlparse
from PIL import Image

URL = 'https://mangareader.cc/chapter/'
HTML_START_TAG = '<p id=arraydata style=display:none>'
HTML_END_TAG = '</p>'
downloaded_files = []

def fetch(name):
    manga_url = urllib.parse.urljoin(URL, str(name))
    response = urlopen(manga_url)
    response_code = response.status
    print("Fetching file list")
    if response_code == 200:
        content = str(response.read())
        start_index = content.index(HTML_START_TAG)
        end_index = content.index(HTML_END_TAG)
        list = ''
        for idx in range(start_index + len(HTML_START_TAG), end_index):
            list = list + content[idx]
        return list.split(',')

def download(list):
    for image_url in list:
        file_path = urlparse(image_url)
        file_name = os.path.basename(file_path.path)
        print("Downloading: " + file_name)
        with open(file_name, "wb") as file:
            response = get(image_url)
            file.write(response.content)
            downloaded_files.append(file_name)

def clean_cache():
    directory_path = os.getcwd()
    for file in downloaded_files:
        os.remove(directory_path + '/' + file)

def save_pdf(filenames):
    images = []
    directory_path = os.getcwd()
    for file in filenames:
        images.append(Image.open(directory_path + '/' + file))
        
    pdf_path = directory_path + '/final.pdf' 
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, required=True)
    args = parser.parse_args()
    manga = args.name
    try:
        list = fetch(manga)
        download(list)
        save_pdf(downloaded_files)
        clean_cache()
    except Exception as e:
        print('Error! Cleaning cache.')
        print(e)
        directory_path = os.getcwd()
        for file in downloaded_files:
            os.remove(directory_path + '/' + file)

if __name__ == '__main__':
    main(sys.argv[1:])
