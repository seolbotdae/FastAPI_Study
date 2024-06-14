from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Book, BookUpdate

# 라우터 설정
router = APIRouter()

# reponse_model을 Book으로 지정하였기 대문에 응답 데이터가 일관된 형식으로 반환됨
@router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    # python 객체를 JSON으로 변환함. mongodb에 넣기 위해서는 JSON형식으로 변경해야 하기 때문
    book = jsonable_encoder(book)

    print("request 출력")
    print(request)

    # request의 Request타입은 ASGI(비동기 웹)프레임워크인 starlette에서 지원하며, 
    # request.app은 starlette가 작동하는 어플리케이션 인스턴스를 나타냄
    new_book = request.app.database["books"].insert_one(book)

    # 만들어낸 책에 대해 query함. 사용자에게 response를 다시 주기 위해서
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book


@router.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    # 다수를 받아오면 pymongo.cursor.Cursor object로 받아옴.

    # pymongo: MongoDB와 상호작용하기 위한 Python 라이브러리.
    # pymongo.cursor: 커서 관련 기능을 제공하는 모듈.
    # pymongo.cursor.Cursor: 커서의 구체적인 구현을 담당하는 클래스.

    # pymongo.cursor.Cursor는 메모리에 바로 로드하지 않고, 해당 객체가 읽힐때 하나씩 가져옵니다.
    # 현재 pymongo.cursor.Cursor object를 즉시 list로 변경하는데, 이럴 경우 메모리 사용량이 한번에 증가함
    print(request.app.database["books"].find(limit=100).next())
    books = list(request.app.database["books"].find(limit=100))
    return books


@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    # Walrus Operator는 값의 할당과 평가를 동시에 할 수 있는 연산자임
    # book에 query결과를 받아오고, 그것이 None이 아님을 동시에 검사하여 book을 return함
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    # HTTPException은 FastAPI에서 제공하는 예외 클래스
    # HTTP 상태 코드와 오류 메시지를 지정하여 클라이언트에게 특정한 HTTP 오류를 반환할 수 있음.
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.put("/{id}", response_description="Update a book", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    # 딕셔너리 컴프리헨션을 통해 객체를 만듬
    book = {k: v for k, v in book.dict().items() if v is not None}

    if len(book) >= 1:
        # update_one 함수의 반환값은 pymongo.results.UpdateResult 객체임

        # UpdateResult 객체의 프로퍼티는 다음과 같다.
        # matched_count: 업데이트 조건에 일치하는 문서의 수.
        # modified_count: 실제로 업데이트된 문서의 수.
        # upserted_id: 만약 upsert 옵션이 True이고 새로운 문서가 삽입된 경우, 삽입된 문서의 _id.
        update_result = request.app.database["books"].update_one(
            {"_id": id}, {"$set": book}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    # update랑 마찬가지로, delete_one 함수는 pymongo.results.DeleteResult 객체를 반환함

    # DeleteResult 객체의 프로퍼티는 다음과 같다.
    # deleted_count: 삭제된 문서의 수를 반환함.
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
