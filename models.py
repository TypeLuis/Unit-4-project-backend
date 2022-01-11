from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)

    carts = db.relationship("Cart")

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "carts": [c.to_json() for c in self.carts],
        }


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_name = db.Column(db.String)
    item_price = db.Column(db.String)
    item_link = db.Column(db.String)
    checkout_date = db.Column(db.Date)
    checkedOut = db.Column(db.Boolean)

    def to_json(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "item_name": self.item_name,
            "item_price": self.item_price,
            "item_link": self.item_link,
            "checkout_date": self.checkout_date,
            "checkedOut": self.checkedOut,
        }
