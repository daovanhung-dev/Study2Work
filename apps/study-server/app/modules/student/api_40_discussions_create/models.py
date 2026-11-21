from pydantic import BaseModel


class CreateDiscussionRequest(BaseModel):
    course_id: int
    title: str
    content: str
