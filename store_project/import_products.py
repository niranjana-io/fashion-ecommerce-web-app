import os
import django
import json
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_project.settings')
django.setup()

from store_app.models import Product

with open('store_app/templates/products.json', 'r', encoding='utf-8') as file:
    contents = json.load(file)

for product in contents:
    data = Product.objects.create(
        name=product['name'],
        price=product['price'],
        image_url=product['image_url'],
        image_path=product['image_path']
    )

print(f"Imported {len(contents)} products successfully!")
