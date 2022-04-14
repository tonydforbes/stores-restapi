from db import db

class ItemModel(db.Model):

    #SQLAlchemy mappings
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True)  # Why is this Id not a class attribute?
    item_name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self,item_name,price,store_id):
        self.item_name = item_name
        self.store_id = store_id
        self.price = price

    def json(self):
        return {"item_name":self.item_name,"price":self.price,"store_id":self.store_id}

    @classmethod
    def look_for_item_in_db(cls, item_name):
        return cls.query.filter_by(item_name=item_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
