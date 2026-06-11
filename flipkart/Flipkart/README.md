# Flipkart E-Commerce Application

A fully-featured Django e-commerce application with user authentication, product catalog, shopping cart, and order management.

## Features

### ✅ User Authentication
- **Register**: Create new user accounts
- **Login**: Secure user login
- **Logout**: User session management
- Password hashing and validation

### 🛍️ Product Management
- Display all products with descriptions and prices
- Product stock tracking
- Product images support

### 🛒 Shopping Cart
- Add products to cart
- Update item quantities
- Remove items from cart
- Real-time cart total calculation
- Cart item count display

### 💳 Checkout & Orders
- Secure checkout process with address collection
- Order creation from cart items
- Order confirmation
- Order history tracking
- Detailed order view with status

### 📊 Order Management
- Order status tracking (Pending, Confirmed, Shipped, Delivered, Cancelled)
- Order history view
- Order details view
- Automatic cart clearing after order placement

## Project Structure

```
flipkart/
├── Flipkart/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── GFlipkart/               # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Django forms
│   ├── urls.py             # App URL patterns
│   ├── admin.py            # Admin configuration
│   └── migrations/
├── templates/              # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   ├── order_history.html
│   └── order_detail.html
├── statics/               # Static files (CSS, JS, images)
├── manage.py
└── db.sqlite3            # Database file
```

## Models

### Product
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `image`: Product image (optional)
- `stock`: Available quantity
- `created_at`: Creation timestamp

### Cart
- `user`: FK to User
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- Methods: `get_total()`, `get_item_count()`

### CartItem
- `cart`: FK to Cart
- `product`: FK to Product
- `quantity`: Item quantity
- Method: `get_total()`

### Order
- `user`: FK to User
- `order_date`: Creation timestamp
- `delivery_date`: Expected delivery date (optional)
- `status`: Order status (choices: pending, confirmed, shipped, delivered, cancelled)
- `total_amount`: Total order amount
- `shipping_address`: Delivery address

### OrderItem
- `order`: FK to Order
- `product`: FK to Product
- `quantity`: Item quantity
- `price`: Price at time of order
- Method: `get_total()`

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install django pillow
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Add Sample Products (Admin Panel)
- Go to http://localhost:8000/admin/
- Login with superuser credentials
- Add products in the "Products" section

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | home | Product listing |
| `/register/` | register | User registration |
| `/login/` | user_login | User login |
| `/logout/` | user_logout | User logout |
| `/add-to-cart/<id>/` | add_to_cart | Add product to cart |
| `/cart/` | view_cart | View shopping cart |
| `/cart/update/<id>/` | update_cart | Update cart item quantity |
| `/cart/remove/<id>/` | remove_from_cart | Remove item from cart |
| `/checkout/` | checkout | Checkout process |
| `/order-confirmation/<id>/` | order_confirmation | Order confirmation page |
| `/order-history/` | order_history | View all orders |
| `/order-detail/<id>/` | order_detail | View order details |

## Authentication

- **Login Required**: Cart operations, checkout, order views
- **Auto Login**: User logged in after successful registration
- **Session Management**: Django sessions handling

## Admin Panel Features

Access admin panel at `/admin/`:
- Manage products (create, edit, delete)
- View/manage carts
- View/manage orders
- View/manage cart items and order items
- Filter and search functionality

## Forms

### RegisterForm
- First name, Last name
- Email, Username
- Password with validation

### LoginForm
- Username
- Password

### CheckoutForm
- Shipping address
- City, Postal code, Country

## Styling

- Bootstrap 5 framework
- Responsive design
- Gradient navbar
- Card-based layouts
- Modal-like modals

## Future Enhancements

- Payment gateway integration
- Product reviews and ratings
- Wishlist functionality
- Email notifications
- Inventory management
- Admin dashboard
- Search and filtering
- Product categories
- Discount codes
- Shipping options

## Troubleshooting

**Issue**: Media files not loading
- Set up `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Create media folder in project root

**Issue**: Database errors
- Run `python manage.py migrate`
- Delete db.sqlite3 and migrations (except __init__.py) then remigrate

**Issue**: Static files not loading
- Run `python manage.py collectstatic`

## Support

For issues or questions, please create an issue in the project repository.

---

**Author**: Flipkart Development Team
**License**: MIT
