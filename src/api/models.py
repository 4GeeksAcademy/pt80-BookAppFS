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
    password: Mapped[str] = mapped_column(
        String(256), nullable=False,
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
    num_pages: Mapped[int]
    date_published: Mapped[date]
    cover: Mapped[str]
    is_awesome: Mapped[bool]
    genres: Mapped[List["Genre"]] = relationship(
        back_populates="books",
        secondary=book_to_genre,
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            # "author": self.author,
            "num_pages": self.num_pages,
            "date_published": self.date_published,
            "cover": self.cover,
            "is_awesome": self.is_awesome,
        }

    def __repr__(self):
        return f"<Book {self.title}>"


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    dob: Mapped[date]
    gender: Mapped[str]
    books: Mapped[List["Book"]] = relationship(back_populates="author")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
        }

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
