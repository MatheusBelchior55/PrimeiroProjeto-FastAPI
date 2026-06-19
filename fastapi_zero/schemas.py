from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    limit: int = Field(default=10, ge=0)
    offset: int = Field(default=0, ge=0)


class TodoSchema(BaseModel):
    title: str
    description: str | None = None
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3)
    state: TodoState | None = None
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
