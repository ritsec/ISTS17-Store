"""
    Create our database and fill it with items
"""
from app import DB
from app.models.transaction import Transaction
from app.models.item import Item
from app.config import ITEMS
DB.create_all()

print 'Adding items...'
for item in ITEMS:
    new_item = Item(name=item['name'], price=item['price'])
    DB.session.add(new_item)

print 'Done'
DB.session.commit()
