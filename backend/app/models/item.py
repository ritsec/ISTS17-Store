"""
    Document to represent an item in the store
"""
import re
from app import DB

class Item(DB.Model):
    """
    Represents a item
    """
    __tablename__ = 'items'
    name = DB.Column(DB.String(256))
    uuid = DB.Column(DB.String(256), primary_key=True)
    description = DB.Column(DB.String(512))
    image = DB.Column(DB.String(128))
    price = DB.Column(DB.Integer)


    def __init__(self, name=None, description="", price=None, image=None):
        self.name = name
        self.description = description
        # Build UUID based on name
        self.uuid = name.lower().strip().replace(" ", "_")
        self.uuid = re.sub(r"[^A-Za-z0-9_]", "", self.uuid)
        self.price = price
        self.image = image

    def __repr__(self):
        return '<Item name={} price={} image={}>'.format(self.name, self.price, self.image)
