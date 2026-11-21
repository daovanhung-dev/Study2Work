from pydantic import BaseModel


class CreateDiscussionCommentRequest(BaseModel):
    content: str
