import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


df = joblib.load("myapp/models/destination_data.pkl") 
vectorizer = joblib.load("myapp/models/vectorizer.pkl")
similarity_matrix = joblib.load("myapp/models/similarity_matrix.pkl")

def preprocess_user_input(cost, time, difficulty):
    
    cost_normalized = (cost - df["Cost"].min()) / (df["Cost"].max() - df["Cost"].min())
    time_normalized = (time - df["Time"].min()) / (df["Time"].max() - df["Time"].min())
    
    # Convert difficulty to vector using the saved vectorizer
    difficulty_vector = vectorizer.transform([difficulty]).toarray().flatten()
    
    # concatnate user input
    user_input_vector = difficulty_vector.tolist() + [cost_normalized, time_normalized]
    
    # making sure the user input vector matches the dimensions of the similarity matrix
    if len(user_input_vector) < similarity_matrix.shape[1]:
        padding_needed = similarity_matrix.shape[1] - len(user_input_vector)
        user_input_vector.extend([0] * padding_needed)

    return user_input_vector

def recommend_destinations(user_cost, user_time, user_difficulty, top_n=5):

    user_input = preprocess_user_input(user_cost, user_time, user_difficulty)
    
    # Compute cosine similarity between the user input and all destinations
    user_similarity = cosine_similarity([user_input], similarity_matrix)
    similar_indices = user_similarity[0].argsort()[::-1]
    
    # Retrieve unique destinations to avoid duplicates
    seen_destinations = set()
    recommended_indices = []

    for idx in similar_indices:
        destination_name = df.iloc[idx]["Trek"]
        if destination_name not in seen_destinations:
            recommended_indices.append(idx)
            seen_destinations.add(destination_name)
        if len(recommended_indices) == top_n:
            break

    return df.iloc[recommended_indices][["Trek", "Cost", "Time", "Difficulty", "Max Altitude", "Best Travel Time"]].to_dict(orient="records")
