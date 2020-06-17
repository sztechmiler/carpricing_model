from pymongo import MongoClient
import pandas as pd
from Models import PricingModels
from DataBaseManager import DBManager

#to run mongodb in terminal run sudo service mongod status

if __name__ == "__main__":
    cars = DBManager.get_cars("Opel", "Zafira")

    some_model = PricingModels.PricingModel(cars)
    x = some_model.getModelParameters()



    # client = MongoClient()
    # carPricingDB = client["carPricing"]
    # firstOffersCollection = carPricingDB.firstOffers
    # cos = firstOffersCollection.find().limit(50)
    # x = pd.DataFrame(list(cos))
    # print(x.columns)

    # query_Zafiry = {"Marka pojazdu":'Opel', "Model pojazdu": 'Insignia', "Uszkodzony": { "$exists" : False }}
    # allDataAboutZafiry = firstOffersCollection.find(query_Zafiry)
    print("co jest kotku")




