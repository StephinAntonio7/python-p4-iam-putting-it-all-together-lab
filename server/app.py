#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        try:
            new_user = User(
                username = request.json.get('username'),
                image_url = request.json.get("image_url"),
                bio  =request.json.get("bio")
            )
            new_user.password_hash = request.json['password']
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return new_user.to_dict(), 201
        except IntegrityError:
            return {"error": "Unprocessable entity"}, 422

class CheckSession(Resource):
    def get(self):
        user = User.query.where(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(), 200
        else:
            return{"error": "Unauthorized access"}, 401

class Login(Resource):
    def post(self):
        user = User.query.where(User.username == request.json.get('username')).first()
        if user and user.authenticate(request.json.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 201
        else: 
            return{'error': 'Username or Password was invalid'}, 401
        
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id')
            return{}, 204
        else:
            return{'error': 'Unauthorized'}, 401

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return{"error": "Unauthorized access"}, 401
        
        user = User.query.get(user_id)
        if user:
            recipes = [recipe.to_dict() for recipe in user.recipes]
            return recipes, 200
        else:
            return {"error": "Unauthorized access"}, 401

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)