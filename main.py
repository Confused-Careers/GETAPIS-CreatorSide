# from fastapi import FastAPI, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
# import openai
# import os
# from pydantic import BaseModel

# app = FastAPI()

# # Allow CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Sample product data
# products = [
#     {"id": 1, "name": "Product 1", "description": "Description for product 1"},
#     {"id": 2, "name": "Product 2", "description": "Description for product 2"},
#     {"id": 3, "name": "Product 3", "description": "Hi i am ml engineer"},
#     {"id": 4, "name": "Product 4", "description": "Description for product 4"},
#     {"id": 5, "name": "Product 5", "description": "Description for product 5"},
#     {"id": 6, "name": "Product 6", "description": "Description for product 6"},
#     {"id": 7, "name": "Product 7", "description": "Description for product 7"},
#     {"id": 8, "name": "Product 8", "description": "Description for product 8"},
#     {"id": 9, "name": "Product 9", "description": "Description for product 9"},
#     {"id": 10, "name": "Product 10", "description": "Description for product 10"},
# ]

# @app.get("/products")
# def get_products():
#     return products

# @app.get("/products/{product_id}")
# def get_product(product_id: int):
#     for product in products:
#         if product["id"] == product_id:
#             return product
#     raise HTTPException(status_code=404, detail="Product not found")

# openai.api_key = "sk-proj-Lcb5Fio59lVjDxixg2M5T3BlbkFJrYWRAuAIMEVjxFQZOqSY"

# class ChatRequest(BaseModel):
#     prompt: str
#     product: dict

# @app.post("/chat")
# def chat_with_gpt3(request: ChatRequest):
#     product_info = f"The product you are inquiring about is {request.product['name']} with ID {request.product['id']}. Description: {request.product['description']}."
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": product_info},
#             {"role": "user", "content": request.prompt},
#         ],
#         max_tokens=100,
#         temperature=0.7
#     )
#     return {"response": response.choices[0].message['content']}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import openai

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up MongoDB client
client = MongoClient("mongodb+srv://dppatel:Admin1234@cluster0.ugxqzd8.mongodb.net/")
db = client["users_db"]  # replace 'users_db' with your database name
collection = db["creator"]  # replace 'creator' with your collection name

class Product(BaseModel):
    id: str
    name: str
    description: str

class ChatRequest(BaseModel):
    prompt: str
    product: Product

@app.get("/products", response_model=list[Product])
def get_products():
    products = list(collection.find())
    return [Product(id=str(product["_id"]), name=product["name"], description=product["description"]) for product in products]

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(id=str(product["_id"]), name=product["name"], description=product["description"])

openai.api_key = "sk-proj-Lcb5Fio59lVjDxixg2M5T3BlbkFJrYWRAuAIMEVjxFQZOqSY"

@app.post("/chat")
def chat_with_gpt3(request: ChatRequest):
    product_info = f"The product you are inquiring about is {request.product.name} with ID {request.product.id}. Description: {request.product.description}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": product_info},
            {"role": "user", "content": request.prompt},
        ],
        max_tokens=100,
        temperature=0.7
    )
    return {"response": response.choices[0].message['content']}

