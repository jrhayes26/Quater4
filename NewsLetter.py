import requests
import openai
import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# === Load Secrets ===
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Initialize OpenAI Client
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# === Step 1: Fetch Top Books by Distinct Sub-Genres ===
def fetch_nyt_book_news():
    url = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
    params = {"api-key": NYT_API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        categorized_books = []
        seen_titles = set()

        # Define sub-genres to filter (expandable list)
        desired_categories = [
            "Hardcover Fiction",
            "Paperback Nonfiction",
            "Young Adult Hardcover",
            "Science",
            "Paperback Trade Fiction",
            "Business Books",
            "Combined Print & E-Book Nonfiction",
            "Combined Print & E-Book Fiction",
            "Graphic Books and Manga",
            "Hardcover Nonfiction"
        ]

        for list_info in data["results"]["lists"]:
            category_name = list_info["display_name"]
            if category_name not in desired_categories:
                continue

            books = []
            for book in list_info["books"]:
                title = book["title"].strip().lower()
                if title in seen_titles:
                    continue  # Skip duplicate books across categories

                seen_titles.add(title)
                books.append({
                    "title": book["title"],
                    "author": book["author"],
                    "description": book["description"],
                    "url": book["amazon_product_url"],
                    "book_image": book["book_image"]
                })
                if len(books) == 2:  # Limit to top 2 unique books per category
                    break

            if books:
                categorized_books.append({
                    "category": category_name,
                    "books": books
                })

        return categorized_books
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You write email newsletter summaries about books."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error summarizing: {e}]"

# === Step 3: Format the HTML Email ===
def format_email(categorized_books):
    subject = "📚 NYT Book Highlights – Curated by Genre"

    html_body = f"""
    <html>
    <body style='font-family: Arial, sans-serif; padding: 20px;'>
        <h1 style='font-size: 26px; color: #333;'>📚 NYT Book Highlights – Curated by Genre</h1>
        <p style='font-size: 16px;'>Explore top picks from a wide range of literary genres from the New York Times bestseller lists.</p>
    """

    for category in categorized_books:
        html_body += f"""
        <h2 style='font-size: 20px; color: #2a2a2a; margin-top: 30px;'>{category['category']}</h2>
        <hr style='margin: 10px 0;'>
        """
        for book in category['books']:
            summary = summarize_book(book)
            html_body += f"""
            <table style='width: 100%; margin-bottom: 20px;'>
                <tr>
                    <td style='width: 150px;'>
                        <img src='{book['book_image']}' alt='Cover for {book['title']}' width='120' style='border-radius: 5px;'>
                    </td>
                    <td style='vertical-align: top; padding-left: 20px;'>
                        <h3 style='margin: 0; font-size: 18px;'>{book['title']}</h3>
                        <p style='margin: 4px 0 10px;'><strong>by {book['author']}</strong></p>
                        <p style='font-size: 14px; color: #333;'>{summary}</p>
                        <a href='{book['url']}' style='font-size: 14px; color: #1a0dab;'>📘 Buy on Amazon</a>
                    </td>
                </tr>
            </table>
            """

    html_body += "</body></html>"
    return subject, html_body

# === Step 4: Send the Email (HTML) ===
def send_email(subject, html_body):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = Header(subject, "utf-8")

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP("smtp.mail.me.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# === Main Execution ===
def run_newsletter():
    categorized_books = fetch_nyt_book_news()

    if not categorized_books:
        print("No books retrieved.")
        return

    subject, html_body = format_email(categorized_books)
    send_email(subject, html_body)

if __name__ == "__main__":
    run_newsletter()
