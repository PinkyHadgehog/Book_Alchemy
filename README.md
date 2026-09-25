# 📚 Book Alchemy

Book Alchemy is a Flask-based web application for managing a personal book collection.

The project was built as part of my backend development training and focuses on working with relational databases, SQLAlchemy ORM, Flask routing, templates, and external book data.

## Features

- Add and manage authors
- Add books with ISBN, title, publication year, and rating
- Connect books to their authors using relational database models
- Search and sort the book collection
- Display book covers using ISBN data
- View detailed information about books and authors
- Delete books and authors
- Rate books
- Generate book recommendations
- Responsive web interface built with Flask templates and CSS

## Tech Stack

- **Python**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **HTML / CSS**
- **Jinja2**
- **Open Library API**

## Project Structure

Book_Alchemy/
│
├── data/                # Local database files
├── static/              # CSS and other static assets
├── templates/           # Jinja2 HTML templates
│
├── app.py               # Flask application and routes
├── data_models.py       # SQLAlchemy database models
├── main.py              # Additional application entry / setup
├── requirements.txt     # Python dependencies
└── README.md
