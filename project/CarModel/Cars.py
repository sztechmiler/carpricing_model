import datetime

class Car:
    def __init__(self, price, brand, model, fuel, millage, year, gearBox, capacity, power, drive, **kwargs):
        self.price = price
        self.brand = brand 
        self.model = model
        self.fuel = fuel
        self.millage = millage
        self.age = datetime.datetime.now().year - int(year)
        self.gearBox = gearBox
        self.capacity = capacity
        self.power = power
        self.drive = drive
        # self.features = features
        self.carDict = self.generateDict()
        
    def generateDict(self):
        carDict = {
            "price": self.price,
            "brand": self.brand, 
            "model": self.model, 
            "fuel": self.fuel, 
            "millage": self.millage,
            "age": self.age,
            "gearBox": self.gearBox, 
            "capacity": self.capacity,
            "power": self.power,
            "drive": self.drive,
            # "features": self.features,
        }
        return carDict




