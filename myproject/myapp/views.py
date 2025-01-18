from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .models import UserProfile





def home(request):
    return render(request, "home.html")


# In your views.py

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Both fields are required.")
            return redirect('login')

        try:
            # Find user by email, assuming email is unique
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard after successful login
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')  # Render login page for GET requests



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from myapp.models import UserProfile
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'POST':
        # Get data from the form
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_picture = request.FILES.get('profile_picture')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Check if the user already has a profile (preventing the IntegrityError)
        if not UserProfile.objects.filter(user=user).exists():
            # Create a new user profile
            user_profile = UserProfile(user=user, profile_picture=profile_picture)
            user_profile.save()

        # Log the user in automatically after successful signup
        #user = authenticate(request, username=email, password=password)
        #if user is not None:
           # login(request, user)

        # Redirect to the login page after successful signup
        return redirect('login')  # Redirect to the login page after signup

    return render(request, 'signup.html')

    


def Custom_logout(request):
    logout(request)  # Django's built-in logout function
    messages.info(request, "You have been logged out.")
    return redirect('home')  # Redirect to the login page after logout

with open("myapp/models/trek_recommendation_model.pkl", "rb") as model_file:
    similarity_matrix, scaler, trek_data = pickle.load(model_file)



def recommend_treks(user_cost, user_time, top_n=6):
    # Normalize user input
    user_input = scaler.transform([[user_cost, user_time]])
    # Compute similarity
    user_similarity = cosine_similarity(user_input, scaler.transform(trek_data[["Cost", "Time"]]))[0]
    # Find top N most similar treks
    recommended_indices = user_similarity.argsort()[-top_n * 2:][::-1]  # Get more entries initially
    recommendations = trek_data.iloc[recommended_indices]
    # Drop duplicates by Trek name
    unique_recommendations = recommendations.drop_duplicates(subset="Trek").head(top_n)
    return unique_recommendations

# View to handle recommendation requests
def recommendations(request):
    recommendations = []  # Initialize recommendations as an empty list
    if request.method == "POST":
        try:
            user_cost = int(request.POST.get("cost", 0))
            user_time = int(request.POST.get("time", 0))
            recommendations = recommend_treks(user_cost, user_time).to_dict("records")
        except Exception as e:
            print(f"Error: {e}")
            recommendations = []
    return render(request, "recommendations.html", {"recommendations": recommendations})
#userprofile
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
@login_required
def profile(request):
    # Retrieve user profile using the user associated with the logged-in user
    user_profile = UserProfile.objects.get(user=request.user)

    # Pass the user and profile data to the template
    return render(request, 'profile.html', {
        'user': request.user,        # Contains all the user fields (e.g., email, first_name)
        'profile': user_profile,     # Contains additional profile data (e.g., bio, profile_picture)
    })

from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile  # Access the user profile through OneToOneField
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('profile')  # Redirect to the profile view after saving
    else:
        form = UserProfileForm(instance=user_profile)  # Pre-fill the form with current profile data

    return render(request, 'edit_profile.html', {'form': form})

