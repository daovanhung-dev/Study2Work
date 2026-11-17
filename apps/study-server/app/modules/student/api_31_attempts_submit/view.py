from __future__ import annotations

import logging
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_31_attempts_submit.models import SubmittedAnswer, SubmittedAttempt
from app.modules.student.api_31_attempts_submit.query import (
    FINALIZE_ATTEMPT,
    LIST_ATTEMPT_ANSWERS,
    LIST_GRADED_ANSWERS,
    LIST_QUESTION_CHOICES,
    LIST_QUIZ_QUESTIONS,
    LOCK_SUBMIT_ATTEMPT,
    MARK_QUESTION_ANSWERS,
    SET_QUESTION_SCORE,
)
from app.modules.student.api_31_attempts_submit.validate import validate_submit_attempt
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def submit_attempt(*, authorization: str | None, attempt_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_submit_attempt(authorization, attempt_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, attempt_id = validated
    try:
        attempt = query_one(db, LOCK_SUBMIT_ATTEMPT, {"attempt_id": attempt_id})
        if attempt is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Attempt not found.", trace_id=trace_id)
        if attempt.get("user_id") != user_id:
            return error_response(status_code=403, business_code="DESIGN_ACCESS_DENIED", message="Access denied to this attempt.", trace_id=trace_id)
        if attempt.get("status") != "IN_PROGRESS":
            return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Attempt is already closed.", trace_id=trace_id)

        questions = query_many(db, LIST_QUIZ_QUESTIONS, {"quiz_id": attempt["quiz_id"]})
        # Kiểm tra thang điểm trước mọi UPDATE để không chấm một Quiz sai cấu hình.
        question_scores: dict[int, Decimal] = {}
        possible_points = Decimal("0")
        invalid_scoring = False
        for question in questions:
            question_id = question.get("id")
            try:
                question_score = Decimal(str(question.get("score") or 0))
            except (InvalidOperation, TypeError):
                invalid_scoring = True
                break
            if type(question_id) is not int or not question_score.is_finite() or question_score < 0:
                invalid_scoring = True
                break
            question_scores[question_id] = question_score
            possible_points += question_score
        try:
            passing_score = Decimal(str(attempt.get("passing_score")))
        except (InvalidOperation, TypeError):
            invalid_scoring = True
            passing_score = Decimal("-1")
        if (
            invalid_scoring
            or possible_points <= 0
            or not passing_score.is_finite()
            or not Decimal("0") <= passing_score <= Decimal("100")
        ):
            db.rollback()
            return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Quiz scoring configuration is invalid.", trace_id=trace_id)

        answer_rows = query_many(db, LIST_ATTEMPT_ANSWERS, {"attempt_id": attempt_id})
        selected: dict[int, set[int]] = {}
        for row in answer_rows:
            if row.get("choice_id") is not None:
                selected.setdefault(row["question_id"], set()).add(row["choice_id"])

        score_total = Decimal("0")
        for question in questions:
            question_id = question["id"]
            question_type = question.get("question_type")
            if question_type not in {"SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"}:
                db.rollback()
                return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Attempt contains an unsupported question type.", trace_id=trace_id)
            correct_rows = query_many(db, LIST_QUESTION_CHOICES, {"question_id": question_id})
            correct_ids = {row["id"] for row in correct_rows}
            selected_ids = selected.get(question_id, set())
            exact_match = bool(selected_ids) and selected_ids == correct_ids
            question_score = question_scores[question_id]
            if exact_match:
                score_total += question_score
            if selected_ids:
                db.execute(text(MARK_QUESTION_ANSWERS), {"attempt_id": attempt_id, "question_id": question_id, "is_correct": exact_match})
                if exact_match:
                    db.execute(text(SET_QUESTION_SCORE), {"attempt_id": attempt_id, "question_id": question_id, "score": question_score})

        now = datetime.now(UTC)
        final_row = query_one(db, FINALIZE_ATTEMPT, {"attempt_id": attempt_id, "user_id": user_id, "submitted_at": now, "score": score_total})
        if final_row is None:
            db.rollback()
            return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Attempt is already closed.", trace_id=trace_id)
        answer_results = query_many(db, LIST_GRADED_ANSWERS, {"attempt_id": attempt_id, "quiz_id": attempt["quiz_id"]})
        passed = score_total * Decimal("100") >= possible_points * passing_score
        response = SubmittedAttempt(
            **final_row,
            passed=passed,
            answers=[SubmittedAnswer.model_validate(row) for row in answer_results],
        )
        db.commit()
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Submit quiz attempt failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Attempt could not be submitted.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_UPDATED", message="Attempt submitted.", trace_id=trace_id, data=response.model_dump(mode="json"))
