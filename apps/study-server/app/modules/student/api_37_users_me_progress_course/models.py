from pydantic import BaseModel


class CourseProgress(BaseModel):
    course_id: int
    completed_lessons: int
    total_lessons: int
    progress_percent: int
    has_content: bool
