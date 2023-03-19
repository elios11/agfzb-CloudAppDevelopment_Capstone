from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.decorators import login_required
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pwd"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.META.get("HTTP_REFERER", "/"))
        context["login_error"] = "Invalid username or password. Try again or register if you don't already have an account."
        return render(request, "djangoapp/login.html", context)
    return render(request, "djangoapp/login.html", context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "POST":
        logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        try:
            User.objects.get(username=username)
            username_in_use = True
            context["message"] = "The username is already in use"
        except:
            logger.debug(f"{username} is not in use")
        if not username_in_use:
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            redirect("djangoapp:index")
    return render(request, "djangoapp/registration.html", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/1fb30bdc-da8e-4040-b8c5-b86d07927bc0/dealership-package/get-dealership"
        try:
            state = request.GET["state"]
            dealership = get_dealer_by_state(url, state)
            return HttpResponse(dealership)
        except:
            # Get dealers from the URL
            dealerships = get_dealers_from_cf(url)
            context["dealerships"] = dealerships
        return render(request, "djangoapp/index.html", context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/1fb30bdc-da8e-4040-b8c5-b86d07927bc0/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "reviews": reviews,
            "dealer_id": dealer_id
        }
    return render(request, "djangoapp/dealer_details.html", context)

# Create a `add_review` view to submit a review
@login_required(login_url="/djangoapp/login.html/")
def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = { "cars": cars, "dealer_id": dealer_id }
        return render(request, "djangoapp/add_review.html", context)
    
    if request.method == "POST":
        carId = request.POST.get("car")
        car = CarModel.objects.get(id=carId)
        purchase = "false"
        if request.POST.get("purchasecheck") == "on":
            purchase = "true"
        review_data = request.POST
        print(car.make)
        review = {"review": {}}
        review["review"]["time"] = datetime.utcnow().isoformat()
        review["review"]["dealership"] = dealer_id
        review["review"]["review"] = review_data.get("content", "")
        review["review"]["name"] = request.user.first_name
        review["review"]["purchase"] = purchase
        review["review"]["purchase_date"] = review_data.get("purchasedate", "")
        review["review"]["car_make"] = car.make.name
        review["review"]["car_model"] = car.name
        review["review"]["car_year"] = car.year.strftime("%Y")
        print(review)
        response = post_request(
            "https://us-south.functions.appdomain.cloud/api/v1/web/1fb30bdc-da8e-4040-b8c5-b86d07927bc0/dealership-package/post-review",
            review,
            dealerId=dealer_id
        )
        if response.status_code == 200:
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        context = { "message" : "Something went wrong with your submission :("}
        return render(request, "djangoapp/add_review.html", context)
    return HttpResponse("Couldn't fulfill your request.", status=400)
