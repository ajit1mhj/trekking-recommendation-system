from django.shortcuts import render
import joblib
import pandas as pd

# Load the trained model and scaler
rf_model = joblib.load("myapp/models/random_forest_model.pkl")
scaler = joblib.load("myapp/models/scaler.pkl")
df = joblib.load("myapp/models/destination_data.pkl")  # Ensure your CSV file is accessible

def preprocess_user_input(cost, time):
    # Normalize the user input (Cost and Time)
    user_input_scaled = scaler.transform([[cost, time]])
    return user_input_scaled

def recommendations(request):
    recommendations = None
    if request.method == "POST":
        # Get user input from the form
        user_cost = float(request.POST.get("cost"))
        user_time = int(request.POST.get("time"))
        
        # Preprocess the input (scale the user cost and time)
        user_input_scaled = preprocess_user_input(user_cost, user_time)
        
        # Predict the difficulty using the Random Forest model
        predicted_difficulty = rf_model.predict(user_input_scaled)
        
        # Get the predicted difficulty
        user_difficulty = predicted_difficulty[0]
        
        # Filter and recommend treks based on the predicted difficulty
        recommendations = df[df["Difficulty"] == user_difficulty]

        # Check if there are no recommendations
        if recommendations.empty:
            recommendations = None

    return render(request, "recommendations.html", {"recommendations": recommendations})
