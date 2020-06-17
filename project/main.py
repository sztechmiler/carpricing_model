from pymongo import MongoClient
import pandas as pd
from Models import PricingModels
from DataBaseManager import DBManager

#to run mongodb in terminal run sudo service mongod status

if __name__ == "__main__":
    #todo: get list of pairs of brand and model and run whole modeling for all cars
    #todo: get list of pairs of brand and model to popualte django drop down menus
    #todo: get simples calulation possible for some cars in django -> that would require some additional
    #todo: steps e.g. connect db with sql or build simple equasion based on model in DB
    cars = DBManager.get_cars("Opel", "Zafira", limit=50)

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




