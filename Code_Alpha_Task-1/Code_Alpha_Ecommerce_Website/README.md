# 🛍 ShopEasy — Django E-Commerce Project

A beginner-friendly full-stack e-commerce website built with Django + SQLite.

---

## 📁 Project Structure

```
shopeasy/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created on first run
├── ecommerce/              ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/                  ← Main app
    ├── models.py           ← Product, Order, OrderItem
    ├── views.py            ← All page logic
    ├── urls.py             ← URL routes
    ├── forms.py            ← Register & Login forms
    ├── admin.py            ← Django admin setup
    ├── context_processors.py
    ├── management/
    │   └── commands/
    │       └── seed_products.py   ← Loads sample data
    └── templates/store/
        ├── base.html
        ├── home.html
        ├── product_detail.html
        ├── cart.html
        ├── checkout.html
        ├── orders.html
        ├── login.html
        └── register.html
```

---

## ⚙️ Setup & Installation

### 1. Create & activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
python manage.py migrate
```

### 4. Seed sample products (8 products loaded)

```bash
python manage.py seed_products
```

### 5. Create an admin superuser

```bash
python manage.py createsuperuser
# OR use the default one created during setup:
# Username: admin   Password: admin123
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Open in your browser

| URL | Page |
|-----|------|
| http://127.0.0.1:8000/ | Home — product listing |
| http://127.0.0.1:8000/cart/ | Shopping cart |
| http://127.0.0.1:8000/login/ | Login page |
| http://127.0.0.1:8000/register/ | Register page |
| http://127.0.0.1:8000/orders/ | My orders (login required) |
| http://127.0.0.1:8000/admin/ | Django admin panel |

---

## 🚀 Features

| Feature | Details |
|---------|---------|
| Product Listing | Grid layout with image, name, price, Add to Cart |
| Product Detail | Full description, stock status, add to cart |
| Shopping Cart | Add/remove items, adjust quantity, running total |
| Session Cart | Cart persists in browser session (no login needed to browse) |
| User Auth | Register, login, logout with Django's built-in auth system |
| Order Checkout | Logged-in users can place orders saved to the database |
| Order History | View all past orders with item breakdown |
| Django Admin | Manage products, orders, users from /admin/ |

---

## 🗄️ Database Models

### Product
| Field | Type |
|-------|------|
| name | CharField |
| description | TextField |
| price | DecimalField |
| image | ImageField (optional) |
| stock | IntegerField |

### Order
| Field | Type |
|-------|------|
| user | ForeignKey → User |
| status | pending / completed / cancelled |
| total_price | DecimalField |
| created_at | DateTimeField |

### OrderItem
| Field | Type |
|-------|------|
| order | ForeignKey → Order |
| product | ForeignKey → Product |
| quantity | IntegerField |
| price | DecimalField (price at time of purchase) |

---

## 🧪 Test the full flow

1. Open http://127.0.0.1:8000/
2. Browse products and click **Add to Cart**
3. Click **Cart** in the navbar → adjust quantities
4. Click **Proceed to Checkout** → you'll be prompted to login
5. Register a new account or use **admin / admin123**
6. Complete the checkout → order is saved
7. Visit **Orders** to see your order history

---

## 🔧 Tech Stack

- **Backend**: Django 5 (Python)
- **Database**: SQLite (default — zero config)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Auth**: Django's built-in authentication system
- **Images**: Pillow (for ImageField support)

---

*Built as an internship project. All security warnings in `--deploy` check are expected for local development and should be addressed before any production deployment.*
