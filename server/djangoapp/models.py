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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
#class CarDealer():
    

# <HINT> Create a plain Python class `DealerReview` to hold review data
#class DealerReview():