from pymongo import MongoClient


client = MongoClient()

# carPricingDB = client["carPricing"]
# firstOffersCollection = carPricingDB.create_collection("firstOffers")
# firstOffersCollection.insert_one({"item":"initialone"})


carPricingDB = client.carPricing
firstOffersCollection = carPricingDB.firstOffers
firstOffersCollection.insert_one(
    {"item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {"h": 28, "w": 35.5, "uom": "cm"}})

coss = firstOffersCollection.find({"item":"canvas"})[0]

print(coss)