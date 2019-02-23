"""
    Create our database and fill it with items
"""
import yaml
from app import DB
from app.models.transaction import Transaction
from app.models.item import Item
DB.create_all()

with open("items.yml") as fil:
    ITEMS = yaml.load(fil)

print('Adding items...')
for item in ITEMS:
    new_item = Item(name=item['name'], price=item['price'],
                    image=item['image'], description=item['description'])
    print(item)
    DB.session.add(new_item)

print('Done')
DB.session.commit()
