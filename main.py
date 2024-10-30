from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

# Download NLTK data for sentiment analysis
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Load reviews from CSV into a DataFrame
def load_reviews():
    return pd.read_csv('reviews.csv')

reviews_df = load_reviews()

# Initialize FastAPI app
app = FastAPI()

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint: Analyze sentiment by reviewer name
@app.get("/sentiment-analysis/")
def sentiment_analysis(reviewer_name: str):
    # Filter reviews by reviewer name
    filtered_reviews = reviews_df[reviews_df["Reviewer Name"].str.lower() == reviewer_name.lower()]
    if not filtered_reviews.empty:
        review_text = filtered_reviews.iloc[0]["Review Text"]
        score = sia.polarity_scores(review_text)["compound"]
        sentiment = "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"
        return {"review": review_text, "sentiment": sentiment}
    else:
        return {"error": "No reviews found for the given reviewer name."}

# Endpoint: Review Retrieval by color, storage size, and verified purchase status
@app.get("/review-retrieval/")
def review_retrieval(
    color: str = Query(None, description="Filter by color"),
    storage: str = Query(None, description="Filter by storage size"),
    verified: str = Query(None, description="Filter by verified purchase status (Yes or No)")
):
    filtered_reviews = reviews_df

    # Apply color filter
    if color:
        filtered_reviews = filtered_reviews[filtered_reviews["product_color"].str.lower() == color.lower()]

    # Apply storage filter
    if storage:
        filtered_reviews = filtered_reviews[filtered_reviews["product_size"].str.lower() == storage.lower()]

    # Apply verified purchase filter, normalizing values to ensure matching
    if verified:
        filtered_reviews = filtered_reviews[filtered_reviews["Verified Purchase"].str.strip().str.lower() == verified.strip().lower()]
    
    # Handle missing or non-JSON-compliant values
    filtered_reviews = filtered_reviews.replace([np.inf, -np.inf], np.nan).fillna("N/A")

    return {"filtered_reviews": filtered_reviews.to_dict(orient="records")}

# Endpoint: Serve HTML file
@app.get("/", response_class=HTMLResponse)
def get_frontend():
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read())
