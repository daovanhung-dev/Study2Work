from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiscussionAuthor(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    avatar_url: str | None = None


class DiscussionComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    discussion_id: int
    content: str
    author: DiscussionAuthor
    created_at: datetime


class Discussion(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str
    author: DiscussionAuthor
    status: str
    comments: list[DiscussionComment] = Field(default_factory=list)


class Pagination(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


class DiscussionPage(BaseModel):
    items: list[Discussion]
    pagination: Pagination
