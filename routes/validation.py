from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import User

router = APIRouter()

@router.post("/email-duplication", response_description="Check email duplication", status_code=status.HTTP_200_OK)
def check_email_duplication(request: Request, email: str = Body(..., embed=True)):
    print(email)
    return {"email": email}

@router.post("/nickname-duplication", response_description="Check nickname duplication", status_code=status.HTTP_200_OK)
def check_nickname_duplication(request: Request, nickname: str = Body(..., embed=True)):
    print(nickname)
    return {"nickname": nickname}
