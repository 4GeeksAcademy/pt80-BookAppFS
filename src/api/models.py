from datetime import date
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    String, Column, Table, ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    mapped_column, relationship,
)
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class Base(DeclarativeBase):
    """
    This is magic that can be ignored
    for now!  It's a special tool
    that will help us later.
    """


db = SQLAlchemy(model_class=Base)


"""
This is the old 1.4-style models:
"""
# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )
#     username = db.Column(
#         db.String(256),
#         unique=True,
#         nullable=False,
#     )
#     email = db.Column(
#         db.String(256),
#     )
#     password = db.Column(
#         db.String(256),
#         nullable=False,
#     )


book_to_genre = Table(
    "book_to_genre",
    Base.metadata,
    Column("book_id", ForeignKey("book.id")),
    Column("genre_id", ForeignKey("genre.id")),
)


# class BookToGenre(Base):
#     __tablename__ = "book_to_genre_2"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
#     genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))


class User(Base):
    """
    This is the new SQA 2.0 style:
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False,
    )
    email: Mapped[str]
    _password: Mapped[str] = mapped_column(
        String(256), nullable=False,
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password_hash(self, other):
        return check_password_hash(self.password, other)

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
        }

    def __repr__(self):
        return f"<User {self.username}>"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id"),
        nullable=True,
    )
    author: Mapped["Author"] = relationship(back_populates="books")
    num_pages: Mapped[int]
    year_published: Mapped[date]
    cover: Mapped[str]
    is_awesome: Mapped[bool]
    genres: Mapped[List["Genre"]] = relationship(
        back_populates="books",
        secondary=book_to_genre,
    )

    def serialize(self, include_rel=False) -> dict:
        book_dict = {
            "id": self.id,
            "title": self.title,
            "num_pages": self.num_pages,
            "year_published": self.year_published,
            "cover": self.cover,
            "is_awesome": self.is_awesome,
        }

        if include_rel:
            return {
                **book_dict,
                "author": self.author.serialize() if self.author else None
            }

        return book_dict

    def __repr__(self):
        return f"<Book {self.title}>"


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    dob: Mapped[date]
    gender: Mapped[str]
    books: Mapped[List["Book"]] = relationship(back_populates="author")

    def serialize(self, include_rel=False) -> dict:
        author_dict = {
            "id": self.id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
        }

        if include_rel:
            return {
                **author_dict,
                "books": [book.serialize() if book else None for book in self.books]
            }

        return author_dict

    def __repr__(self):
        return f"<Author {self.name}>"


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    books: Mapped[List["Book"]] = relationship(
        back_populates="genres",
        secondary=book_to_genre,
    )

    def __repr__(self):
        return f"<Genre {self.name}>"
