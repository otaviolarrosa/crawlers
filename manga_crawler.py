import os
import shutil
from os import walk
import urllib3
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

WORKING_DIRECTORY = f'/home/otaviolarrosa/dev/test/'
PDF_NAME = 'bleach-chapter-2'
URL = f'https://mangareader.cc/chapter/{PDF_NAME}'
IMG_ELEMENT_ID_PREFIX = 'page'


def download():
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    browser.get(URL)
    page = 1
    browser.find_element(By.XPATH,
                         '//*[@id="content"]/div/div/article/div[2]/div[3]/div[1]/div/select/option[2]').click()
    a = browser.find_element(By.CLASS_NAME, 'comic_wraCon')
    files = []
    imgs = a.find_elements(By.TAG_NAME, 'img')
    for img in imgs:
        files.append(page)
        http = urllib3.PoolManager()
        r = http.request('GET', img.get_attribute('src'), preload_content=False)
        with open(f'{WORKING_DIRECTORY}{page}', 'wb') as out:
            shutil.copyfileobj(r, out)
        r.release_conn()
        page += 1
        print(img.get_attribute('src'))
    browser.close()

    save_pdf(files)
    delete_images()


def delete_images():
    files = next(walk(f'{WORKING_DIRECTORY}'), (None, None, []))[2]
    files.remove(f'{PDF_NAME}.pdf')
    for file in files:
        print(f'deleting file {file}')
        os.remove(f'{WORKING_DIRECTORY}{file}')


def save_pdf(filenames):
    images = [
        Image.open(f'{WORKING_DIRECTORY}{f}')
        for f in filenames
    ]

    pdf_path = f'{WORKING_DIRECTORY}{PDF_NAME}.pdf'
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
    shutil.move(f'{pdf_path}', f'{WORKING_DIRECTORY}/compiled/{PDF_NAME}.pdf')


def get_element(browser, page):
    return browser.find_element(By.ID, IMG_ELEMENT_ID_PREFIX + str(page))


if __name__ == '__main__':
    try:
        download()
    except Exception as e:
        files = next(walk(f'{WORKING_DIRECTORY}'), (None, None, []))[2]
        for file in files:
            os.remove(f'{WORKING_DIRECTORY}{file}')
