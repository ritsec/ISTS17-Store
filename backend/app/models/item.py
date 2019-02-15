"""
    Document to represent an item in the store
"""
from app import DB

class Item(DB.Model):
    """
    Represents a item

    :param uuid: the id of the item
    :param price: how much the item is worth
    """

    __tablename__ = 'items'
    uuid = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(128))
    price = DB.Column(DB.Integer)

    def __init__(self, name=None, price=None):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Item uuid={} name={} price={}>'.format(self.uuid, self.name, self.price)
