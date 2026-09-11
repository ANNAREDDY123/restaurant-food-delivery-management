# 🍽️ Restaurant & Food Delivery Management System

A backend REST API for managing restaurants, customers, food menus, orders, payments, delivery partners, order tracking, cancellations, refunds, reviews, dashboards, and analytics.

The project is built using **FastAPI**, **SQLAlchemy**, **Pydantic**, and **SQLite**.

---

## 🚀 Features

### 🔐 Authentication

- User registration
- User login
- JWT authentication
- Refresh token support
- Get current user details
- Change password

### 🏪 Restaurant Management

- Create restaurant
- View restaurants
- Get restaurant by ID
- Update restaurant
- Delete restaurant
- Restaurant filtering and management

### 🍔 Menu Management

- Create food items
- View food items
- Get food item by ID
- Update food items
- Delete food items

### 👤 Customer Management

- Create customers
- View customers
- Get customer details
- Update customers
- Customer search and filtering

### 📍 Address Management

- Create customer addresses
- View customer addresses
- Update addresses
- Delete addresses

### 🛒 Cart Management

- Add items to cart
- View cart
- Update cart items
- Delete cart items
- Clear cart

### 🎟️ Coupon Management

- Create coupons
- View coupons
- Apply coupons to orders
- Coupon validation and discount calculation

### 📦 Order Management

- Create orders
- View orders
- Get order by ID
- Search and filter orders
- Pagination
- Sorting
- Update order status

### 🚚 Delivery Partner Management

- Create delivery partners
- View delivery partners
- Update delivery partner status
- Assign delivery partners to orders

### 📍 Order Tracking

- Add order tracking updates
- View order tracking history

### 💳 Payment Management

- Create payments
- Get payment details
- Update payment status
- Payment status tracking

### ❌ Cancellation & Refund

- Cancel orders
- Store cancellation reasons
- Process refunds
- Get refund details
- Prevent duplicate refunds

### ⭐ Reviews

- Add reviews
- Restaurant reviews
- Food item reviews
- Rating management

### 📊 Restaurant Dashboard

Provides restaurant-level analytics including:

- Today's orders
- Pending orders
- Completed orders
- Cancelled orders
- Today's revenue
- Monthly revenue
- Most ordered food
- Average rating
- Total customers

### 📈 Admin Analytics

Provides system-wide analytics including:

- Total restaurants
- Total customers
- Total orders
- Total revenue
- Total refunds
- Active delivery partners
- Top restaurants
- Top food items
- Most popular cuisine
- Daily orders
- Monthly revenue
- Cancellation rate

### 🔔 Notifications

Background notifications for:

- Order placement
- Order status updates
- Refund processing

---

# 🛠️ Technology Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT Authentication
- Pytest
- Uvicorn

---

# 📂 Project Structure

```text
restaurant-food-delivery-management/
│
├── app/
│   ├── models/          # SQLAlchemy database models
│   ├── routes/          # API routes
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── tests/           # Pytest test files
│   └── utils/           # Utility functions
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/ANNAREDDY123/restaurant-food-delivery-management.git
2. Navigate to the Project Folder
cd restaurant-food-delivery-management
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
6. Configure Environment Variables

Create a .env file using .env.example as a reference.

Example:

DATABASE_URL=sqlite:///./restaurant.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
▶️ Run the Application

Start the FastAPI server:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000
📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc
🧪 Testing

The project uses Pytest for automated testing.

Run all tests:

pytest -q

Current test status:

159 passed

Test coverage includes:

Authentication
Restaurants
Customers
Addresses
Cart
Coupons
Orders
Delivery partners
Order tracking
Payments
Cancellation and refunds
Reviews
Dashboard
Admin analytics
Database connection
Model relationships
📡 Main API Modules
Module	Endpoint
Authentication	/auth
Restaurants	/restaurants
Menu	/menu/items
Customers	/customers
Addresses	/addresses
Cart	/cart
Coupons	/coupons
Orders	/orders
Delivery Partners	/delivery-partners
Order Tracking	/orders/{order_id}/tracking
Payments	/payments
Cancellation & Refund	/orders/{order_id}/cancel
Reviews	/reviews
Restaurant Dashboard	/dashboard/restaurants/{restaurant_id}
Admin Analytics	/admin/analytics
🔒 Security Features
Password hashing
JWT authentication
Access token support
Refresh token support
Protected API endpoints
Password change functionality
📊 API Testing

The APIs can be tested using:

Swagger UI
Postman
Pytest automated tests
🚀 Future Improvements

Possible future enhancements include:

Role-based access control
Real-time notifications
Email notifications
SMS notifications
Online payment gateway integration
Docker support
PostgreSQL/MySQL deployment
Redis caching
Advanced analytics
Admin dashboard frontend
Restaurant frontend
Customer frontend
👨‍💻 Author

ANNAREDDY JAGADESWAR REDDY
