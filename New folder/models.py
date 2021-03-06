
from datetime import datetime
from software import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"Author('{self.first_name}', '{self.last_name}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    #publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    stock_level = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#If you want your cart to be stored in db, specify a model for it here, e.g.
# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     etc. ....
