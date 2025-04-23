# Quater4
# 📚 NYT Book Highlights Newsletter Generator

This Python script fetches the latest top books from the New York Times bestseller lists across various genres, uses OpenAI to summarize them into newsletter-friendly blurbs, and emails a beautifully formatted HTML digest to your inbox.

---

## 🧰 Features

- Real-time data from the **New York Times Books API**
- Summarized using **OpenAI's GPT-3.5**
- Well-designed **HTML email layout** with book covers
- Organized by **genre/subtype** (Fiction, Nonfiction, YA, Business, etc.)
- No repeated books across categories

---

## ✅ Prerequisites

- Python 3.7 or higher
- An OpenAI API key
- A New York Times Developer API key
- An email account (like Gmail or iCloud) with an app-specific password

---

## 📦 Installation

1. Clone or download this project:

```bash
git clone https://github.com/yourusername/nyt-book-newsletter.git
cd nyt-book-newsletter
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

3. Install the dependencies:

```bash
pip install openai requests python-dotenv
```

---

## 🔐 Get Your API Keys

### 📘 New York Times API Key

1. Go to: [https://developer.nytimes.com](https://developer.nytimes.com)
2. Log in or create a free account.
3. Click **“Apps”** and then **“+ Create App”**.
4. Name your app (e.g., `BookDigestApp`).
5. Under **API access**, select **Books API**.
6. Click **Create**, then copy your **API Key**.

### 🧠 OpenAI API Key

1. Go to: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Log in or sign up.
3. Click **Create new secret key** and copy it.

### 📧 App-Specific Password (Email Sending)

#### For Gmail:
- Turn on **2-Step Verification** in your Google Account.
- Visit: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Choose **Other**, name it `Newsletter`, then click **Generate**.
- Copy the 16-character password.

#### For iCloud:
- Turn on **2-Factor Authentication** at [https://appleid.apple.com](https://appleid.apple.com)
- Go to **App-Specific Passwords**, generate one for `Newsletter`
- Copy and save it.

---

## 📝 Create a `.env` File

Create a file named `.env` in the project root and add:

```env
NYT_API_KEY=your_nyt_key_here
OPENAI_API_KEY=your_openai_key_here
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_specific_password_here
```

> 🔒 **Never share your `.env` file or upload it to GitHub!**

---

## 🚀 Run the Script

Simply run:

```bash
python newsletter.py
```

This will:
- Fetch real-time NYT book data
- Summarize it using OpenAI
- Format it into a styled HTML email
- Send the digest to your inbox

---

## 💡 Tips & Troubleshooting

- If your email fails to send: double-check your email and app password.
- If OpenAI throws errors: verify your API key and that your account has quota.
- If you want to run it **weekly**, use Task Scheduler (Windows) or `cron` (macOS/Linux).

---

## 👨‍💻 Author
Created by [Your Name] for educational and personal productivity use. Want to add genres, filters, or HTML flair? Fork it and go wild!
