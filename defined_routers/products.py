from fastapi import APIRouter,Depends,HTTPException,status
from .paths import *
from sqlalchemy.orm import Session
from schemas import CreateProduct,User,UpdateProduct
from typing import Annotated,List
from utils.authenticate import get_current_user
from databases import *
from models import Products

product_router = APIRouter(tags=['products'])

#Api for prodcuct creation
@product_router.post(ADD_PRODUCT,response_model=CreateProduct)
def create_product(request : CreateProduct,current_user : Annotated[User,Depends(get_current_user)],db:Session = Depends(get_db)):
    if not request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please provide the necessary details"
        )
    name = request.name
    category = request.category
    price = request.price

    if not name or not category or not price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please provide all the details"
        )
    
    product = Products(
        name = name,
        category = category,
        price = price
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


#Api for getting all the products
@product_router.get(GET_ALL_PRODUCTS,response_model=List[CreateProduct])
def get_all_products(current_user : Annotated[User,Depends(get_current_user)],db:Session = Depends(get_db)):
    products = db.query(Products).all()
    return products

#Api for getting one product by id
@product_router.get(GET_PRODUCT_BY_ID,response_model=CreateProduct)
def get_product_by_id(product_id : int,current_user : Annotated[User,Depends(get_current_user)],db:Session = Depends(get_db)):
    product = db.query(Products).filter_by(id=product_id).first()
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        detail = "item not found"
    )

#Api for updating a product
@product_router.put(UPDATE_PRODUCT_BY_ID,response_model=CreateProduct)
def update_product_by_id(product_id : int,payload : UpdateProduct,current_user : Annotated[User,Depends(get_current_user)],db:Session = Depends(get_db)):
    product = db.query(Products).filter_by(id=product_id).first()
    updated_name = payload.name
    updated_category = payload.category
    updated_price = payload.price
    if product:
        product.name = updated_name if updated_name else product.name
        product.category = updated_category if updated_category else product.category
        product.price = updated_price if updated_price else product.price
        db.commit()
        db.refresh(product)
        return product
    raise HTTPException(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        detail="Item not found"
    )


#Api for deleting a product
@product_router.delete(DELETE_PRODUCT,response_model=CreateProduct)
def delete_product(product_id : int,current_user : Annotated[User,Depends(get_current_user)],db:Session = Depends(get_db)):
    product = db.query(Products).filter_by(id=product_id).first()

    if product:
        db.delete(product)
        db.commit()
        return product
    raise HTTPException(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        detail="Item not found"
    )