from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #creating a db object

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )


    def __str__(self):
        return (
            f"Id: {self.id}, "
            f"Name: {self.name}, "
            f"Birthdate: {self.birth_date}, "
            f"Date of Death: {self.date_of_death}"
        )

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("author.id"),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=True)

    author = db.relationship(
        "Author",
        back_populates="books"
    )

    def __str__(self):
        return (
            f"Id: {self.id}, "
            f"ISBN: {self.isbn}, "
            f"Title: {self.title}, "
            f"Publication year: {self.publication_year}, "
            f"Author id: {self.author_id}"
        )

    def __repr__(self):
        return f"Book(isbn={self.isbn}, title='{self.title}')"
