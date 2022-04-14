from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, Users
from resources.item import Items, Item
from resources.store import Store, Stores
from db import db

# Set up some variables
app = Flask(__name__)
app.secret_key = "p1e9r6l6e0m7o0e4n"
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Dont need this, SQLAlchemy has own tracking function
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()

# Add resources (or end points)
api.add_resource(Item, '/item/<string:item_name>')
api.add_resource(Users, '/users')
api.add_resource(Items, '/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:store_name>')
api.add_resource(Stores,'/stores')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000)
