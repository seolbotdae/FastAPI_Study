from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import User

router = APIRouter()

@router.post("/", response_description="Sign up new user", status_code=status.HTTP_201_CREATED)
def sign_up_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)

    print(request.body)
    print(user)

    return "hello"