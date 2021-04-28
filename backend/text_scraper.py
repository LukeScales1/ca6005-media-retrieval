import pickle
import time

import urllib.parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import webscraper
from classifier import Classifier

image_classifier = Classifier()
options = Options()
options.add_argument('--headless')


def store_results(label_index, img_index, img_results):
    with open("results.p", "rb") as f:
        data = pickle.load(f)
    data[str(label_index)]["images"][img_index]["text"] = img_results
    with open("results.p", "wb") as f:
        pickle.dump(data, f)


def get_image_array(index):
    with open("results.p", "rb") as f:
        data = pickle.load(f)
    return data[str(index)]["images"]


if __name__ == "__main__":
    # image_classifier = Classifier()
    start_from = 270  # to continue scraping from a certain index if execution fails
    img_start = False  # to continue scraping from certain image in class if execution fails
    # img_start = False
    labels = image_classifier.labels
    for i, label in enumerate(labels):
        print(f"{i}: {label}")
        if i < start_from:
            continue
        image_data = get_image_array(i)
        for img_idx, img in enumerate(image_data):
            print(f"Image {img_idx} of {len(image_data)}")
            if img_start is not False:
                if img_idx < img_start:
                    continue
            if img["relevance"] > 1:
                # Update: took 12 hrs to scrape 238 classes worth of relevance < 10, only scraping matches e.g rel = 1
                # webscraper_test.ipynb shows we have 43501 images in total so only scraping text from relevant entries
                continue
            driver = webdriver.Chrome(options=options)
            print(img["src"])
            page = webscraper.get_pinterest_pin_page(pin_href=img["href"], driver=driver)
            text_and_tags = webscraper.get_text_and_tags(page)
            print(text_and_tags)
            store_results(label_index=i, img_index=img_idx, img_results=text_and_tags)
            driver.close()
            img_start = False  # reset img_start after class has completed after failed execution
            # time.sleep(0.2)
        print("----------------")
