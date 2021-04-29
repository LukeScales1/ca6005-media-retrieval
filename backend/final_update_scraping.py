import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import webscraper
from classifier import Classifier


options = Options()
options.add_argument('--headless')


def store_results(label_index, results):
    with open("results.p", "rb") as f:
        data = pickle.load(f)
    data[str(label_index)] = results
    with open("results.p", "wb") as f:
        pickle.dump(data, f)


def get_entry(index):
    with open("results.p", "rb") as f:
        data = pickle.load(f)
    return data[str(index)]


if __name__ == "__main__":
    """Scraping images and text of classes with no matches using updated labels."""
    image_classifier = Classifier()
    # update to get matching samples with updated labels
    no_matches = [20, 21, 27, 52, 60, 68, 74, 75, 112, 168, 312, 321, 391, 395, 456, 480, 542, 581, 602, 677, 690, 713,
                  737, 810, 830, 865, 867, 908, 998]
    updated_labels = {
        "ear": "corn cob",
        "wing": "jet wing",
        "trailer truck": "semi truck",
        "toyshop": "toy store",
        "stretcher": "emergency stretcher",
        "space bar": "spacebar keyboard",
        "pop bottle": "glass soda pop bottle",
        "photocopier": "office scanner printer",
        "oxcart": "ox cart",
        "nail": "galvanized nail",
        "horizontal bar": "gymnast horizontal bar",
        "grille": "car grill",
        "drumstick": "drum stick",
        "cash machine": "atm machine",
        "bow": "bow weapon",
        "gar": "gar fish",
        "coho": "coho salmon fishing",
        "admiral": "admiral butterfly",
        "cricket": "cricket bug",
        "redbone": "redbone dog",
        "conch": "conch shell",
        "black widow": "black widow spider",
        "garden spider": "araneus diadematus",
        "sidewinder": "horned rattlesnake",
        "night snake": "Hypsiglena torquata",
        "thunder snake": "Carphophis amoenus",
        "eft": "eft newt",
        "kite": "kite hawk",
        "water ouzel": "dipper bird",
    }
    image_classifier.labels = image_classifier.fetch_labels(labels_to_fix=updated_labels)
    for i in no_matches:
        label = image_classifier.labels[i]
        print(label)
        driver = webdriver.Chrome(options=options)

        current_entry = get_entry(i)
        print(current_entry)
        urls = [img["src"] for img in current_entry["images"]]
        page = webscraper.get_pinterest_search_results(search=label, driver=driver)
        img_divs = webscraper.get_img_divs(page)
        if not len(img_divs):
            raise IndexError(f"No results returned for {i} - {label} -- possible API rate limit reached")
        for div in img_divs:
            print(f"Fetching img {img_divs.index(div)} of {len(img_divs)}")
            # purposefully assigning variables to slow down scraping
            href = div.a.get("href")
            src = div.img.get("src")
            alt = div.img.get("alt")
            print(src)
            if src in urls:
                print("already scraped, skipping...")
                continue  # don't download and check the same image twice
            relevance = image_classifier.get_relevance_score(label, webscraper.encode_url(src))
            print(f"Relevance: {relevance}")
            if relevance < 10:
                print("Fetching text..")
                current_entry["relevant_count"] += 1
                # get text data for image if relevant
                page = webscraper.get_pinterest_pin_page(pin_href=href, driver=driver)
                text_and_tags = webscraper.get_text_and_tags(page)
                # purposefully re-retrieving data to slow down scraping
                current_entry["images"].append({
                    "href": div.a.get("href"),
                    "src": div.img.get("src"),
                    "alt": div.img.get("alt"),
                    "relevance": relevance,
                    "text": text_and_tags
                })
            else:
                print("Skipping text")
                current_entry["images"].append({
                    "href": div.a.get("href"),
                    "src": div.img.get("src"),
                    "alt": div.img.get("alt"),
                    "relevance": relevance,
                })

            urls.append(src)
            store_results(i, current_entry)
            print("---")
        print(f"Class complete - {current_entry['relevant_count']} relevant images, "
              f"{len([i for i in current_entry['images'] if i['relevance'] == 1])} matches")
        print("------------------------------")
