from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from django.http import JsonResponse
from .models import *
from .models import UserProfile
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import Booking
from datetime import datetime
from django.http import HttpResponseBadRequest


def home(request):
    return render(request, "home.html")


# In your views.py

def login_view(request):
    """Handle user login with email."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Both fields are required.")
            return redirect('login')

        try:
            # Use filter to handle potential duplicate emails
            users = User.objects.filter(email=email)
            user = users.first()
            if user is None:
                messages.error(request, "No account found with this email.")
                return redirect('login')
                
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid password")
                return redirect('login')
                
        except Exception as e:
            messages.error(request, "An error occurred during login.")
            return redirect('login')

    return render(request, 'login.html')




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

        # Redirect to the login page after successful signup
        return redirect('login')  # Redirect to the login page after signup

    return render(request, 'signup.html')

    


def Custom_logout(request):
    logout(request)  # Django's built-in logout function
    messages.info(request, "You have been logged out.")
    return redirect('home')  # Redirect to the login page after logout


#recomendation

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
            # Get cost and time values from the POST request
            user_cost = int(request.POST.get("cost", 0))
            user_time = int(request.POST.get("time", 0))

            # Server-side validation for cost and time
            if user_cost < 60000 or user_cost > 380000:
                return HttpResponseBadRequest("Budget must be between 60,000 and 380,000 NPR.")
            if user_time < 5 or user_time > 27:
                return HttpResponseBadRequest("Time must be between 5 and 27 days.")
            
            # If validation passes, proceed to recommend treks
            recommendations = recommend_treks(user_cost, user_time).to_dict("records")
        
        except Exception as e:
            # Catch any other exceptions and log the error
            print(f"Error: {e}")
            recommendations = []

    # Render the recommendations page with the recommendations data
    return render(request, "recommendations.html", {"recommendations": recommendations})



@login_required
def profile(request):
    """Display user profile and booking history."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
        return render(request, 'profile.html', {
            'user_profile': user_profile,
            'user_bookings': user_bookings
        })
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('home')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile  # Ensure this object exists!
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect after successful form submission
    else:  # Handle GET request
        form = UserProfileForm(instance=user_profile)

    # Render the form (whether GET request or invalid POST request)
    return render(request, 'edit_profile.html', {'form': form})

def booking(request):
    """Handle trek booking."""
    if request.method == 'POST':
        trek_name = request.POST.get('trek_name')
        cost = request.POST.get('cost')
        time = request.POST.get('time')
        
        # Validate inputs
        if not all([trek_name, cost, time]):
            messages.error(request, "Missing required booking information.")
            return redirect('recommendations')
            
        try:
            cost = float(cost)
            time = int(time)
        except ValueError:
            messages.error(request, "Invalid cost or time value.")
            return redirect('recommendations')
            
        return render(request, 'booking.html', {
            'trek_name': trek_name,
            'cost': cost,
            'time': time
        })
    return redirect('recommendations')


@login_required
def confirm_booking(request):
    """Process trek booking confirmation."""
    if request.method == 'POST':
        try:
            trek_name = request.POST.get('trek_name')
            cost = request.POST.get('cost')
            duration = request.POST.get('duration')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Validate required fields
            if not all([trek_name, cost, duration, start_date, end_date]):
                messages.error(request, "All fields are required.")
                return redirect('booking')

            # Parse and validate dates
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date_obj >= end_date_obj:
                messages.error(request, "End date must be after start date.")
                return redirect('booking')

            if start_date_obj < datetime.now().date():
                messages.error(request, "Start date cannot be in the past.")
                return redirect('booking')

            # Create booking
            Booking.objects.create(
                user=request.user,
                trek_name=trek_name,
                cost=float(cost),
                duration=int(duration),
                start_date=start_date_obj,
                end_date=end_date_obj
            )

            messages.success(request, f'Booking confirmed for {trek_name} from {start_date} to {end_date}!')
            return redirect('profile')

        except ValueError as e:
            messages.error(request, f"Invalid date format or numeric values: {str(e)}")
            return redirect('booking')
        except Exception as e:
            messages.error(request, f"Error processing booking: {str(e)}")
            return redirect('booking')

    return redirect('home')


