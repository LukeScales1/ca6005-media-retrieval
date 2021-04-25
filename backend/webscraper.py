import json

import selenium
import urllib.parse
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup

from classifier import Classifier


image_classifier = Classifier()

YREVAR_IMAGENET_GIST_URL = "https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/raw/" \
                           "238f720ff059c1f82f368259d1ca4ffa5dd8f9f5/imagenet1000_clsidx_to_labels.txt"


def get_yrevar_imagenet_labels():
    file = urllib.request.urlopen(YREVAR_IMAGENET_GIST_URL)
    yrevar_labels = []
    for line in file:
        decoded_line = line.decode("utf-8")
        yrevar_labels.append(decoded_line.split("'")[1])
    return yrevar_labels


def get_pinterest_search_results(search, driver=None, scroll=False):
    if driver is None:
        driver = webdriver.Chrome()
    driver.get(f"https://www.pinterest.ca/search/pins/?q={urllib.parse.quote(search)}&rs=sitelinks_searchbox")
    time.sleep(1)
    if scroll:
        # sleep and scroll to get extra examples
        driver.execute_script("window.scrollTo(0, 5000)")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 10000)")
        time.sleep(5)
    return BeautifulSoup(driver.page_source, "html.parser")


def get_pinterest_pin_page(pin_href, driver=None):
    if driver is None:
        driver = webdriver.Chrome()
    driver.get(f"https://www.pinterest.ca{pin_href}")
    return BeautifulSoup(driver.page_source, "html.parser")


def get_img_divs(parsed_page: BeautifulSoup):
    return parsed_page.findAll("div", {"class": "GrowthUnauthPinImage"})


def get_img_data(class_name, long_label, parsed_page: BeautifulSoup):
    im_divs = get_img_divs(parsed_page)
    return {
        "class": class_name,
        "long_label": long_label,
        "images": [{
            "href": div.a.get("href"),
            "src": div.img.get("src"),
            "alt": div.img.get("alt"),
            "relevance": image_classifier.get_relevance_score(class_name, div.img.get("src"))
        } for div in im_divs]
    }


def get_text_and_tags(parsed_page: BeautifulSoup):
    tags = parsed_page.findAll("a", {"class": "vaseCarousel_vaseTagLink"})
    h1 = parsed_page.findAll("h1")
    h2 = parsed_page.findAll("h2")
    return {
        "h1": h1[0].get_text(),
        "h2": h2[1].get_text(),
        "tags": [tag.get_text() for tag in tags]
    }


def store_results(index, label_results):
    with open("results.json") as f:
        data = json.load(f)
    data[index] = label_results
    with open("results.json", "w") as f:
        json.dump(data, f)


def encode_url(url):
    """Use to prevent UnicodeEncodeErrors when downloading images for classification"""
    # error caused by https://i.pinimg.com/236x/e5/00/30/e500309ec4a1aaaf0e7209af58be24e1--chim-chóc-grouse-hunting.jpg
    parts = url.split('/')
    fix_unicode_errors = urllib.parse.quote(parts[-1].split('.')[0])
    parts[-1] = f"{fix_unicode_errors}.{parts[-1].split('.')[1]}"
    return '/'.join(parts)


if __name__ == "__main__":
    import time
    # image_classifier = Classifier()
    start_from = 133  # to continue scraping from a certain index if execution fails

    labels = image_classifier.labels
    long_labels = get_yrevar_imagenet_labels()
    for i, label in enumerate(labels):
        if i < start_from:
            continue
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        print(f"{i}: {label}")
        # ensure unique urls - if long label is searched to find relevant labels don't download and classify same urls
        urls = []
        image_data = []
        relevance_count = 0
        page = get_pinterest_search_results(search=label, driver=driver)
        img_divs = get_img_divs(page)
        if not len(img_divs):
            raise IndexError(f"No results returned for {i} - {label} -- possible API rate limit reached")
        for div in img_divs:
            # purposefully assigning variables to slow down scraping
            href = div.a.get("href")
            src = div.img.get("src")
            alt = div.img.get("alt")

            relevance = image_classifier.get_relevance_score(label, encode_url(src))
            if relevance < 10:
                relevance_count += 1
            urls.append(src)
            # purposefully re-retrieving data to slow down scraping
            image_data.append({
                "href": div.a.get("href"),
                "src": div.img.get("src"),
                "alt": div.img.get("alt"),
                "relevance": relevance
            })
            time.sleep(1)
        if len([img for img in image_data if img["relevance"] < 10]) < 3:
            # try fetch some relevant images from long label
            print("No relevant results found on imagenet label - fetching more examples using yrevar's label...")
            time.sleep(5)
            page = get_pinterest_search_results(search=long_labels[i], driver=driver, scroll=True)
            img_divs = get_img_divs(page)
            if not len(img_divs):
                raise IndexError(f"No results returned for {i} - {label} -- possible API rate limit reached")
            for div in img_divs:
                # purposefully assigning variables to slow down scraping
                href = div.a.get("href")
                src = div.img.get("src")
                alt = div.img.get("alt")
                if src in urls:
                    continue  # don't download and check the same image twice
                relevance = image_classifier.get_relevance_score(label, encode_url(src))
                if relevance < 10:
                    relevance_count += 1
                urls.append(src)
                # purposefully re-retrieving data to slow down scraping
                image_data.append({
                    "href": div.a.get("href"),
                    "src": div.img.get("src"),
                    "alt": div.img.get("alt"),
                    "relevance": relevance
                })
                if relevance_count > 10:
                    print("10 relevant images scraped from long label, let's call it a day on this one...")
                    break  # no need to get an excessive amount of relevant images
                time.sleep(1)

        results = {
            "class": label,
            "long_label": long_labels[i],
            "images": image_data,
            "relevant_count": relevance_count
        }
        print(f"{len(image_data)} images scraped - {relevance_count} relevant")
        store_results(i, results)
        driver.close()
        time.sleep(10)
        print("----------------")


