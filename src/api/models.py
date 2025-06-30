from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    String, Column, Table, ForeignKey
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
    author: Mapped[str]
    num_pages: Mapped[int]
    date_published: Mapped[date]
    cover: Mapped[str]
    is_awesome: Mapped[bool]

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "num_pages": self.num_pages,
            "date_published": self.date_published,
            "cover": self.cover,
            "is_awesome": self.is_awesome,
        }
