from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from pymongo import MongoClient

client = MongoClient()
carPricingDB = client.carPricing
firstOffersCollection = carPricingDB.firstOffers

################################
#     /\    |---\   |---\
#   /   \   |    \  |    \  PRICE
#  /-----\  |    /  |    /  PRICE :D
# /       \ |---/   |---/
################################

def extractPriceFeatures(html_string):
    dictOfFeatures = {}
    dictOfFeatures["price"] = {""};
    dictOfFeatures["price_currency"] = {""};
    dictOfFeatures["price_details"] = {""};

    try:
        soup = BeautifulSoup(html_string, 'html.parser')
        price = soup.find("span", {"class": "offer-price__number"}).text
        dictOfFeatures["price"] = {price.strip()}
        price_currency = soup.find("span", {"class": "offer-price__currency"}).text
        dictOfFeatures["price_currency"] = {price_currency.strip()}
        price_details = soup.find("span", {"class": "offer-price__details"}).text
        dictOfFeatures["price_details"] = {price_details.strip()}
        return dictOfFeatures
    except Exception as e:
        return dictOfFeatures
        print("Some funny error")

def extractIDandUptadetd(html_string):
    try:
        updated = ""
        offer_ID = ""

        soup = BeautifulSoup(html_string, 'html.parser')
        updated = soup.find("meta", {"property": "og:updated_time"}).findNext("span", {"class": "offer-meta__value"}).text

        offer_ID = soup.find("meta", {"property": "og:updated_time"}).findNext("span", {"class": "offer-meta__label"}).findNext("span", {"class": "offer-meta__value"}).text
        return offer_ID, updated
    except Exception as e:
        return offer_ID, updated
        print("Some funny error")


cwd = os.getcwd()
directory = cwd + "/../rsc/"

for filename in os.listdir(directory):
    print(filename + " at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))    # filename = e.g. slaskie
    for file in os.listdir(directory + filename + "/"):
        features_directory = directory + filename + "/" + file + "/features/"
        # os.makedirs(features_directory, exist_ok=True)
        currentDir = directory + filename + "/" + file + "/offers/"
        try:
            for item in os.listdir(currentDir):
                currentFilePath = currentDir + item
                html = open(currentFilePath, "r").read()

                price_json = extractPriceFeatures(html)
                price = price_json["price"].pop()
                price_currency = price_json["price_currency"].pop()
                price_details = price_json["price_details"].pop()

                offer_ID, updated = extractIDandUptadetd(html)
                #  teraz aktualizujemy mongo ;-)
                firstOffersCollection.update_one({"offer_ID": offer_ID, "updated": updated}, {"$set": {"price": price, "price_currency": price_currency, "price_details": price_details}}, upsert=False)

        except (FileNotFoundError):
            continue