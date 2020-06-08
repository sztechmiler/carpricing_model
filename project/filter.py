from bs4 import BeautifulSoup
import os
import json


################################
#     /\    |---\   |---\
#   /   \   |    \  |    \  PRICE
#  /-----\  |    /  |    /  PRICE :D
# /       \ |---/   |---/
################################


def extractFeatures(html_string):
    dictOfFeatures = {}
    try:
        soup = BeautifulSoup(html_string, 'html.parser')
        title = soup.find('title').text
        dictOfFeatures["title"] = {title.strip()}
        if("Przerwa" in title):
            return dictOfFeatures
        href = soup.find('link', {'rel': 'canonical'}).get("href")
        dictOfFeatures["href"] = {href}
        updated = soup.find("meta", {"property": "og:updated_time"}).findNext("span", {"class": "offer-meta__value"}).text
        dictOfFeatures["updated"] = {updated.strip()}
        offer_ID = soup.find("meta", {"property": "og:updated_time"}).findNext("span", {"class": "offer-meta__label"}).findNext("span", {"class": "offer-meta__value"}).text
        dictOfFeatures["offer_ID"] = {offer_ID.strip()}
        seller_address = soup.find("span", {"class": "seller-box__seller-address__label"}).text
        dictOfFeatures["seller_address"] = {seller_address.strip()}
        for parameter in soup.find_all("li", class_='offer-params__item'):
            label = (parameter.find("span", {"class": "offer-params__label"}).text).strip()
            feature = parameter.find("div", {"class": "offer-params__value"}).text.strip()
            dictOfFeatures[label] = {feature}
        feature_index = 0
        for feature in soup.find_all("li", class_='offer-features__item'):
            dictOfFeatures[str(feature_index)] = {feature.text.strip()}
            feature_index =+ 1
            # print(cos.text.strip())
        description = soup.find("div", {"class": "offer-description__description"}).text.strip()
        dictOfFeatures["description"] = {description}
        return dictOfFeatures
    except Exception as e:
        return dictOfFeatures


cwd = os.getcwd()
directory = cwd + "/../rsc/"

for filename in os.listdir(directory):
    i = 0
    if (filename == "kujawsko-pomorskie"):
        continue
    #  filename = e.g. slaskie
    for file in os.listdir(directory + filename + "/"):
        # file = e.g. 1
        features_directory = directory + filename + "/" + file + "/features/"
        os.makedirs(features_directory, exist_ok=True)
        currentDir = directory + filename + "/" + file + "/offers/"
        i += 1
        print(currentDir + " number: " + str(i))
        try:
            for item in os.listdir(currentDir):
                currentFilePath = currentDir + item
                html = open(currentFilePath, "r").read()
                if(os.path.isfile(features_directory + item)):
                    continue
                else:
                    features_json = extractFeatures(html)
                    with open(features_directory + item, 'w') as outfile:
                        json_str = str(features_json)
                        outfile.write(json_str)
        except (FileNotFoundError):
            continue

                # pickle.dump(features_json, outfile)

# print(description)

# print(cathegory)