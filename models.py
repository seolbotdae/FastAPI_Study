import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Book(BaseModel):
    # Pydantic의 Field 함수는 Pydantic 모델에서 필드의 기본값, 유효성 검사, 메타데이터를 설정하는 데 사용됩니다.
    # Field를 사용하면 모델 필드에 대해 추가적인 제약 조건이나 설명을 지정할 수 있습니다.
    # default_factory를 사용하여 기본값을 만들고, alias로 _id로 부를 수 있게 하였음.
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

    # ...은 pydantic 에서 해당 객체가 필수로 제공되어야 함을 의미함.
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    class Config:
        # 현재 alias를 id에 걸어뒀는데, id로 인스턴스를 만들수도 있고, _id로 인스턴스를 만들 수도 있음.
        allow_population_by_field_name = True
        # 예제 데이터 제공
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }

class User(BaseModel):
    id: str = Field(...)
    pwd: str = Field(...)
    nickname: str = Field(...)

    class Config:
        scheme_extra = {
            "example": {
                "id": "UserID",
                "pwd": "password",
                "nickname": "nickname"
            }
        }