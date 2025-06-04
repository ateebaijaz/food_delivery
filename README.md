---
title: "🍔 Food Delivery API"
description: |
  A backend RESTful API for a food delivery app built using FastAPI, SQLAlchemy, and PostgreSQL. 
  It supports user authentication, restaurant and menu management, order placement, delivery tracking, and ratings.

features:
  - JWT-based User Authentication
  - Restaurant & Menu Management
  - Order Placement & Assignment
  - Delivery Agent Status Updates
  - Ratings for Restaurants & Agents
  - FastAPI Swagger UI for API exploration

tech_stack:
  - FastAPI
  - SQLAlchemy (no Alembic used)
  - PostgreSQL
  - Pydantic
  - Uvicorn

getting_started:
  - step 1: "Clone the repository"
    command: |
      git clone https://github.com/yourusername/food_delivery.git
      cd food_delivery
  - step 2 : "Create virtual environment"
    command: |
      python3 -m venv food
      source food/bin/activate
  - step 3: "Install dependencies"
    command: |
      pip install -r requirements.txt
  - stepn4n: "Set environment variables"
    description: "Create a `.env` file in the root directory with these:"
    content: |
      DATABASE_URL=postgresql://postgres:password@localhost:5432/food_delivery
      JWT_SECRET_KEY=your-secret-key
  - step: "Run the server"
    command: |
      uvicorn main:app --reload
    note: "Visit http://localhost:8000/docs to access Swagger UI"

sample_endpoints:
  - "POST /api/users/register - Register a User"
  - "POST /api/users/login - Login"
  - "POST /api/restaurants/ - Create Restaurant"
  - "POST /api/restaurants/{id}/menu - Add Menu Item"
  - "POST /api/orders/ - Place Order"
  - "PUT /api/orders/{id}/assign - Assign Agent"
  - "POST /api/orders/{id}/rating - Rate Order"

license: MIT License

author:
  name: Your Name
  url: https://github.com/ateebaijaz
