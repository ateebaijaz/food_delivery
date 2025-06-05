from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy import text
from app.routes import auth, user, restaurant, orders, delivery
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

app = FastAPI()

# Custom Swagger Bearer Token Support
security = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Food Delivery API",
        version="1.0.0",
        description="API documentation for the food delivery backend",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Main Page with DB Check and Swagger Link
@app.get("/", response_class=HTMLResponse)
def root():
    db_status = "✅ Database connected!"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "❌ Database connection failed!"
    finally:
        db.close()

    return f"""
    <html>
        <head>
            <title>Food Delivery API</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    padding: 40px;
                    text-align: center;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    font-size: 18px;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 24px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                a:hover {{
                    background-color: #0056b3;
                }}
                .status {{
                    margin-top: 10px;
                    font-weight: bold;
                    color: {"green" if "✅" in db_status else "red"};
                }}
            </style>
        </head>
        <body>
            <h1>🍽️ Welcome to the Food Delivery API</h1>
            <p class="status">{db_status}</p>
            <a href="/docs" target="_blank">🚀 Go to Swagger UI</a>
        </body>
    </html>
    """

# Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(restaurant.router)
app.include_router(orders.router)
app.include_router(delivery.router)
