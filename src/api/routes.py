"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from werkzeug.http import HTTP_STATUS_CODES

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

books = [
    {
        "num_pages": 293,
        "year_published": 1997,
        "author": "Ray Bradbury",
        "isbn10": "0-380-72940-7",
        "have_read": True,
        "cover": "https://pictures.abebooks.com/isbn/9780553136951-us.jpg",
        "title": "Something Wicked This Way Comes",
        "isbn13": "978-0-380-72940-1",
        "is_awesome": True,
        "id": 2,
    },
    {
        "num_pages": 383,
        "year_published": 1970,
        "author": "Gabriel Garcia Marquez",
        "isbn10": "0-380-01503-X",
        "have_read": True,
        "cover": "https://m.media-amazon.com/images/I/81dy4cfPGuL._SY522_.jpg",
        "title": "One Hundred Years of Solitude",
        "isbn13": None,
        "is_awesome": True,
        "id": 3,
    },
    {
        "num_pages": 470,
        "year_published": 1992,
        "author": "Neal Stephenson",
        "isbn10": None,
        "have_read": False,
        "cover": "https://i5.walmartimages.com/seo/Snow-Crash-Hardcover-9780613361620_f11eea3c-5e60-4a1b-936b-67c9c4455e27_1.0a9c061d4600a35fb739ad85e9e9aa06.jpeg",
        "title": "Snow Crash",
        "isbn13": "978-061336162",
        "is_awesome": True,
        "id": 4,
    },
    {
        "num_pages": 815,
        "year_published": 2002,
        "author": "Douglas Adams",
        "isbn10": None,
        "have_read": False,
        "cover": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1404613595i/13.jpg",
        "title": "The Ultimate Hitchiker's Guide To The Galaxy",
        "isbn13": "978-0-645-45374-7",
        "is_awesome": True,
        "id": 5,
    },
]


@api.route("/library", methods=["GET"])
def get_books() -> tuple[str, int]:
    return jsonify(
        books=books, total=len(books),
        offset=0, count=len(books)
    ), 200


@api.route("/library/<int:id>", methods=["GET"])
def get_book(id: int) -> tuple[str, int]:
    book = next(filter(
        lambda x: id == x["id"],
        books
    ), None)

    if book is None:
        return jsonify(msg=f"Book {id} not found"), 404

    return jsonify(book), 200
