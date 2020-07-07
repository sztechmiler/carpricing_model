import sys

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
    brands = DBManager.get_unique_brands()
    for brand in brands:
        models = DBManager.get_unique_modles(brand)
        for model in models:
            try:
                cars = DBManager.get_cars(brand, model)
                if(len(cars) > 50):
                    pricing_model = PricingModels.PricingModel(cars)
                    parameters = pricing_model.getModelParameters()
                    DBManager.insert_db_pricing_model_poly3_allfeatures(brand=brand, model=model, model_parameters=parameters)
            except:
                print("Error", sys.exc_info()[0])
    

