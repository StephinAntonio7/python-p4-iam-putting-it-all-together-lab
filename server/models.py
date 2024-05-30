from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt, app

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-recipes.user', '-_password_hash',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column (db.String, unique = True, nullable=False)
    _password_hash = db.Column (db.String)
    image_url = db.Column (db.String)
    bio = db.Column (db.String)
    
    recipes = db.relationship('Recipe', backref='user')
    
    # new_recipe = Recipe(title="Sample Recipe", instructions = "This is a sample recipe with enough length to meet the 50 character requirement.", minutes_to_complete=30, user_id=1)
    # db.session.add(new_recipe)
    # db.session.commit()
    
    @hybrid_property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')
    
    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')
        
    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column (db.String, nullable=False),
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column (db. Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@validates('title')
def validate_title(self, key, value):
    if not value:
        raise ValueError('Title cannot be empty.')
    return value

@validates('instructions')
def validate_instructions(self, key, value):
    if len(value) < 50:
        raise ValueError('Instructions must be at least 50 characters long.')
    return value   