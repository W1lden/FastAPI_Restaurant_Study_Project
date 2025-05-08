import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uvicorn
from fastapi import FastAPI

from .routers import admin, customer

def restaurant_app():
    app = FastAPI()

    app.include_router(customer.router)
    app.include_router(admin.router)

    return app

app = restaurant_app()

if __name__ == "__main__":
    uvicorn.run(
        app="src.restaurant.main:app",
        reload=True
    )
