# Fashion E-Commerce Web Application

A Django-based fashion e-commerce web application featuring product browsing, user authentication, cart management, and checkout workflow.

## Features
- User registration and login
- Product listing and product detail pages
- Shopping cart functionality
- Cart quantity management
- Checkout and order history
- Admin dashboard support
- Pagination for product listings

## Technologies Used
- Python
- Django
- MySQL
- HTML/CSS
- Bootstrap

## Project Structure
- `views.py` – Handles application logic and workflows
- `models.py` – Database models for products, carts, and orders
- `forms.py` – User registration, login, and checkout forms
- `templates/` – Frontend HTML templates
- `static/` – CSS, images, and static assets


## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Configure MySQL database settings in settings.py
4. Run migrations:
   ```bash
   python manage.py migrate
5. Start the development server:
   ```bash
   python manage.py runserver


## Note
Product data and images were imported separately for development purposes.
