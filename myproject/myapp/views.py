from django.shortcuts import render
from .recommend import recommend_destinations
# Create your views here.
def home(request):
    return render(request, "home.html")

def login_view(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def recommendations(request):
    recommendations = None 
    if request.method == "POST":
        
        user_cost = float(request.POST.get("cost"))
        user_time = int(request.POST.get("time"))
        user_difficulty = request.POST.get("difficulty")
        
        recommendations = recommend_destinations(user_cost, user_time, user_difficulty, top_n=5)
    
    return render(request, "recommendations.html", {"recommendations": recommendations})
