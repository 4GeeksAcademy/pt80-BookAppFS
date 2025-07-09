"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from typing import List
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    get_current_user, jwt_required
)

from api.models import db, User, Book, Author, Genre
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route("/signup", methods=["POST"])
def signup():
    user = User(**request.json)
    db.session.add(user)
    db.session.commit()
    return "", 204


@api.route("/token", methods=["POST"])
def login():
    user = db.session.scalars(
        db.select(User)
        .filter_by(username=request.json["username"])
    ).one_or_none()

    if not user:
        return jsonify(msg="Incorrect credentials."), 401

    if not user.check_password_hash(request.json["password"]):
        return jsonify(msg="Incorrect credentials."), 401

    return jsonify(token=create_access_token(user))


@api.route("/secret", methods=["GET"])
@jwt_required()
def super_secret():
    return jsonify(
        msg="*super obvious whispering.*",
        user=get_jwt_identity()
    ), 200


@api.route("/library", methods=["POST"])
def create_book():
    new_book = Book(**request.json)
    # Book(**request.json) is roughly equivalent to:
    # Book(
    #     title=request.json["title"],
    #     have_read=request.json["have_read"],
    #     ...
    # )

    # We stage the data:
    db.session.add(new_book)
    # Write it to the database:
    db.session.commit()
    # Update our object with the ID et. al.
    db.session.refresh(new_book)
    return jsonify(new_book.serialize()), 200


@api.route("/library", methods=["GET"])
def read_books() -> tuple[str, int]:
    books: List[Book] = db.session.scalars(
        db.select(Book)
    ).all()

    print(books)

    return jsonify(
        books=[book.serialize(include_rel=True) for book in books],
        total=len(books), offset=0, count=len(books)
    ), 200


@api.route("/library/<int:id>", methods=["GET"])
def read_book(id: int) -> tuple[str, int]:
    book = db.session.scalars(
        db.select(Book).filter_by(id=id)
    ).one_or_none()

    if book is None:
        return jsonify(msg=f"Book {id} not found"), 404

    return jsonify(book.serialize(include_rel=True)), 200


@api.route("/library/<int:id>", methods=["PUT"])
def update_book(id: int) -> tuple[str, int]:
    book = db.session.scalars(
        db.select(Book).filter_by(id=id)
    ).one_or_none()

    if book is None:
        return jsonify(msg=f"Book {id} not found"), 404

    for key, value in request.json.items():
        setattr(
            book,
            key,
            value
        )

    db.session.merge(book)
    db.session.commit()
    db.session.refresh(book)

    return jsonify(book.serialize(include_rel=True)), 200


@api.route(
    "/library/<int:book_id>/addauthor/<int:author_id>",
    methods=["POST", "PUT"]
)
def add_author(book_id: int, author_id: int):
    # get the book from the db
    book = db.session.scalars(
        db.select(Book).filter_by(id=book_id)
    ).one_or_none()

    # get the author from the db
    author = db.session.scalars(
        db.select(Author).filter_by(id=author_id)
    ).one_or_none()

    if not all([book, author]):
        return jsonify(
            msg=f"Book {book_id} or Author {author_id} not found"
        ), 404

    # relate those two objects
    # This method is easy (but unsafe):
    # book.author_id = author_id

    # Adding book to author:
    book.author = author

    # write the change to the db
    db.session.merge(book)
    db.session.commit()
    db.session.refresh(book)

    return jsonify(book.serialize(include_rel=True)), 200


@api.route("/library/<int:id>", methods=["DELETE"])
def delete_book(id: int) -> tuple[str, int]:
    book = db.session.get(Book, id)
    db.session.delete(book)
    db.session.commit()

    return "", 204


@api.route("/author", methods=["POST"])
def create_author():
    new_author = Author(**request.json)
    db.session.add(new_author)
    db.session.commit()
    db.session.refresh(new_author)
    return jsonify(new_author.serialize()), 200
