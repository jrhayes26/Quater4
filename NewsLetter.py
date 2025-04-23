# newsletter.py

import requests
import openai
import smtplib
from dotenv import load_dotenv
import os

# === Load Secrets ===
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

openai.api_key = OPENAI_API_KEY

# === Step 1: Fetch Real Book News from NYT ===
def fetch_nyt_book_news():
    url = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
    params = {"api-key": NYT_API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        top_books = []
        for list_info in data["results"]["lists"][:3]:  # Limit to 3 book lists
            book = list_info["books"][0]  # Take first book from each list
            top_books.append({
                "title": book["title"],
                "author": book["author"],
                "description": book["description"],
                "url": book["amazon_product_url"]
            })
        return top_books
    except Exception as e:
        print("Error fetching NYT data:", e)
        return []

# === Step 2: Summarize Each Book Description with OpenAI ===
def summarize_book(book):
    prompt = (
        f"Summarize this book for a newsletter:\n\n"
        f"Title: {book['title']}\n"
        f"Author: {book['author']}\n"
        f"Description: {book['description']}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You write email newsletter summaries about books."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Error summarizing: {e}]"

# === Step 3: Format the Email ===
def format_email(summaries):
    subject = "📚 NYT Book Highlights – Curated for You"
    body = f"Subject: {subject}\n\nHere are today’s top books from The New York Times:\n\n"
    for i, summary in enumerate(summaries, 1):
        body += f"{i}. {summary}\n\n"
    return body

# === Step 4: Send the Email ===
def send_email(body):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, body)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# === Main Program ===
def run_newsletter():
    books = fetch_nyt_book_news()

    if not books:
        print("No books retrieved.")
        return

    summaries = [summarize_book(book) for book in books]
    email_body = format_email(summaries)
    send_email(email_body)

if __name__ == "__main__":
    run_newsletter()
