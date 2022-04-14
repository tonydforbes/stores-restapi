from db import db

class StoreModel(db.Model):

    #SQLAlchemy mappings
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key = True)
    store_name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self,store_name):
        self.store_name = store_name
        print(f"Store name: {store_name}")

    def json(self):
        return {"id":self.id,"store_name":self.store_name,"items":[item.json() for item in self.items.all()]}

    @classmethod
    def look_for_store_in_db(cls, store_name):
        return cls.query.filter_by(store_name=store_name).first()

    def save_to_db(self):
        print(f"About to save the store {self.store_name}")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
