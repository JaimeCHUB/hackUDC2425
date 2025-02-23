from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum

import customSearch
import indetex

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class BrandName(str, Enum):
    zara = "zara"
    zara_home = "zara_home"
    stradivarius = "stradivarius"
    pull_and_bear = "pull_and_bear"
    oysho = "oysho"
    massimo_dutti = "massimo_dutti"
    lefties = "lefties"

def add_image(product):
    image = customSearch.get_google_image(f"{product.get("name")} {product.get("brand")}")
    product["image"] = image
    return product

#Interfaz de la API

@app.get("/products/text")
async def get_items(query: str, brand: BrandName | None = None, page: int | None = None, perPage: int | None = None):
    products = indetex.get_products(query, None if brand == None else brand.value, page, perPage)
    for product in products: add_image(product)
    return products

@app.get("/products/image")
async def get_items_by_image(image: str, page: int | None = None, perPage:int | None = None):
    products = indetex.get_products_by_image(image, page, perPage)
    for product in products: add_image(product)
    return products