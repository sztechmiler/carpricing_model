from bs4 import BeautifulSoup
import os
import json
from pymongo import MongoClient
from datetime import datetime
import pandas as pd


client = MongoClient()
carPricingDB = client.carPricing
firstOffersCollection = carPricingDB.firstOffers



cwd = os.getcwd()
directory = cwd + "/../rsc/"
noOfSkipedItems = 0

for filename in os.listdir(directory):
    print(filename + " at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    #  filename = e.g. slaskie
    for file in os.listdir(directory + filename + "/"):
        # file = e.g. 1

        features_directory = directory + filename + "/" + file + "/features/"
        for item in os.listdir(features_directory):
            currentFilePath = features_directory + item
            html = open(currentFilePath, "r").read()
            # print(html)
            for i in range(0,50):
                html = html.replace("}, %s: {" %(str(i)), "}, \'%s\': {" %(str(i)))
            # print(html)
            html = html.replace("{\"", "{\'") # replace {" to {'
            # print(html)
            html = html.replace("\"}", "\'}") # replace "} to '}
            # print(html)

            html = html.replace("\"", "") # replace all " quotes to nothing
            # print(html)
            html = html.replace("\\n", " ") # replace next line to space
            # print(html)

            # no time to get rid of incorect quotes
            html = html.replace(" {\'"," {\"") #  replace >> {'<< to >> {"<< i.e. general case
            # print(html)
            html = html.replace("\'},","\"},") #  replace >>'},<< to >>"},<< i.e. general case
            # print(html)

            html = html.replace("}, \'", "}, \"") #  replace >>'},<< to >>"},<< i.e. general case - changed
            # print(html)

            html = html.replace("\': {", "\": {") #  replace >>'},<< to >>"},<< i.e. general case
            # print(html)

            #html = html.replace("{\'href", "\"href") # } replace begining i.e. href
            html = html.replace("{\'", "\"") # } replace begining i.e. href
            # print(html)
            html = html.replace("\'}}", "\"") #
            # print(html)

            html = html.replace("}", "") # { to nothing
            # print(html)
            html = html.replace("{", "") # } to nothing
            # print(html)

            html = html.replace("\\", "") # replace all escape characters to nothing
            # print(html)

            # html = html.replace("\": ", " ")

            html = "{" + html + "}"
            # print(html)

            # html = '{"href": "https://www.otomoto.pl/oferta/opel-zafira-1-6-benzyna-super-stan-z-niemiec-7-mio-osobowy-ID6CDYeu.html", "title": "Używane Opel Zafira - 6 990 PLN, 225 000 km, 2004  - otomoto.pl", "updated": "07:43, 9 grudnia 2019", "offer_ID": "6067824090", "seller_address": "Bydgoszcz, Kujawsko-pomorskie", "Oferta od": "Osoby prywatnej", "Kategoria": "Osobowe", "Marka pojazdu": "Opel", "Model pojazdu": "Zafira", "Wersja": "A (1999-2005)", "Rok produkcji": "2004", "Przebieg": "225 000 km", "Pojemność skokowa": "1 600 cm3", "Rodzaj paliwa": "Benzyna", "Moc": "101 KM", "Skrzynia biegów": "Manualna", "Napęd": "Na przednie koła", "Typ": "Minivan", "Liczba drzwi": "5", "Liczba miejsc": "7", "Kolor": "Srebrny", "Kraj pochodzenia": "Niemcy", "Bezwypadkowy": "Tak", "Stan": "Używane", 0: "ABS"}'
            try:
                dict = json.loads(html)

                currentOfferID = dict["offer_ID"]
                currentOfferUpdatedTimeStamp = dict["updated"]

                itemIsNew = (firstOffersCollection.find({"offer_ID": currentOfferID, "updated": currentOfferUpdatedTimeStamp}).limit(1).count() == 0)
                # des_key = '2'
                # des_val = 'Światła'
                # firstOffersCollection.update_one({"offer_ID": currentOfferID, "updated": currentOfferUpdatedTimeStamp}, {"$set":{des_key: des_val}}, upsert=False)
                # ehh = firstOffersCollection.find({"offer_ID": currentOfferID, "updated": currentOfferUpdatedTimeStamp})[0]
                if(itemIsNew):
                    firstOffersCollection.insert_one(dict) # I guess I insert one item (dictionary) to mongoDB
            except Exception as e:
                print(str(e))
                noOfSkipedItems =+ 1

print(noOfSkipedItems)
# with open(directory + "final_database.txt", 'w') as outfile:
#     json_str = str(final_database)
#     outfile.write(json_str)
            # features_json = extractFeatures(html)
            # with open(features_directory + item, 'w') as outfile:
            #     json_str = str(features_json)
            #     outfile.write(json_str)
