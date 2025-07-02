
import os
from flask_admin import Admin
from .models import db, User, Book, Author, Genre
from flask_admin.contrib.sqla import ModelView


class BookView(ModelView):
    column_list = [
        'id', 'title', 'author', 'num_pages',
        'date_published', 'cover', 'is_awesome'
    ]


class AuthorView(ModelView):
    column_list = [
        'id', 'name', 'dob', 'gender', 'books'
    ]


class GenreView(ModelView):
    column_list = [
        'id', 'name', 'books'
    ]


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap4')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(AuthorView(Author, db.session))
    admin.add_view(BookView(Book, db.session))
    admin.add_view(GenreView(Genre, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
