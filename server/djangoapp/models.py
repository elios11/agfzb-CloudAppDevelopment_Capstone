from django.db import models
from django.utils.timezone import now

# Create your models here.

# Create a CarMake model class
class CarMake(models.Model):
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "Name: {}, Description: {}".format(self.name, self.description)

# Create a Car Model model with many-to-one relationship to CarMake
class CarModel(models.Model):
    name = models.CharField(max_length=20, null=False)
    year = models.DateField()
    dealer_id = models.IntegerField()

    SUV = "SUV"
    SEDAN = "Sedan"
    WAGON = "Wagon"
    CONVERTIBLE = "Convertible"
    COUPE = "Coupe"
    SPORTS = "Sports"
    HATCHBACK = "Hatchback"
    TYPE_CHOICES = [
        (SUV, "SUV"),
        (SEDAN, "Sedan"),
        (WAGON, "Wagon"),
        (CONVERTIBLE, "Convertible"),
        (COUPE, "Coupe"),
        (SPORTS, "Sports"),
        (HATCHBACK, "Hatchback"),
    ]
    car_type = models.CharField(choices=TYPE_CHOICES, max_length=20, default=SEDAN)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Car: - Make{} \
                     - Year: {} \
                     - Type: {}".format(self.make, self.year, self.car_type)

# Create a simple Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
    

# Create a plain Python class `DealerReview` to hold review data
class DealerReview():
    def __init__(self, dealership, name, purchase, id, review, purchase_date, car_make, car_model, car_year, sentiment):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Dealership review: {}\
                Review sentiment: {}".format(self.review, self.sentiment)