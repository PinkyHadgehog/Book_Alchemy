from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import inspect
from data_models import db, Author, Book
from datetime import datetime
from openai import OpenAI

import os

app = Flask(__name__)

client = OpenAI()

app.config["SECRET_KEY"] = "dev-secret-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)



"""
# printen namen von Tabellen und Feldern mit inspector

    print("Tables:")
    print(inspector.get_table_names())

    print("\nAuthor columns:")
    for column in inspector.get_columns("author"):
        print(column["name"], column["type"])
"""

@app.route("/")
def home():
    sort_by = request.args.get("sort", "title")
    search = request.args.get("search", "")

    query = db.select(Book)

    # Search
    if search:
        query = query.where(
            Book.title.ilike(f"%{search}%")
        )

    # Sorting by author
    if sort_by == "author":
        query = (
            query
            .join(Author, Book.author_id == Author.id)
            .order_by(Author.name)
        )


    else:

        query = query.order_by(Book.title)

    books = db.session.execute(query).scalars().all()

    return render_template(
        "home.html",
        books=books,
        search=search
    )

@app.route("/add_author", methods = ["GET", "POST"])
def add_author():
    success = False

    if request.method == "POST":
        name = request.form["name"]

        birth_date = datetime.strptime(
            request.form["birth_date"],
            "%Y-%m-%d"
        ).date()

        date_of_death_input = request.form["date_of_death"]

        if date_of_death_input:
            date_of_death = datetime.strptime(
                date_of_death_input,
                "%Y-%m-%d"
            ).date()
        else:
            date_of_death = None

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        success = True

    return render_template(
        "add_author.html",
        success=success
    )


@app.route("/add_book", methods = ["GET", "POST"])
def add_book():

    success = False

    #take authors from the author-table
    authors = db.session.execute(
        db.select(Author)
    ).scalars().all()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        publication_year = int(request.form["publication_year"])
        author_id = int(request.form["author_id"])

        new_book = Book(
            isbn = isbn,
            title = title,
            publication_year = publication_year,
            author_id = author_id
        )

        db.session.add(new_book)
        db.session.commit()

        success = True

    return render_template(
    "add_book.html",
    authors=authors,
    success = success
)

@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return "Book not found", 404

    db.session.delete(book)
    db.session.commit()

    flash("Book successfully deleted!")

    return redirect(url_for("home"))


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return "Book not found", 404

    return render_template(
        "book_detail.html",
        book=book
    )


@app.route("/author/<int:author_id>")
def author_detail(author_id):
    author = db.session.get(Author, author_id)

    if author is None:
        return "Author not found", 404

    return render_template(
        "author_detail.html",
        author=author
    )


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    author = db.session.get(Author, author_id)

    if author is None:
        return "Author not found", 404

    db.session.delete(author)
    db.session.commit()

    flash("Author and all associated books successfully deleted!")

    return redirect(url_for("home"))

@app.route("/book/<int:book_id>/rate", methods=["POST"])
def rate_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return "Book not found", 404

    rating = int(request.form["rating"])

    if rating < 1 or rating > 10:
        flash("Rating must be between 1 and 10.")
        return redirect(url_for("book_detail", book_id=book.id))

    book.rating = rating

    db.session.commit()

    flash("Rating successfully saved!")

    return redirect(url_for("book_detail", book_id=book.id))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
