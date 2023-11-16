from fastapi import APIRouter, Body, Path

router = APIRouter()


@router.post("/eventbridge/{subject}")
def eventbridge(subject: str = Path(...), body: dict = Body(...)) -> dict:
    received = {"subject": subject, "body": body}
    return received


@router.post("/sns/{topic}/{subject}")
def sns(topic: str = Path(...), subject: str = Path(...), body: dict = Body(...)) -> dict:
    received = {"topic": topic, "subject": subject, "body": body}
    return received


@router.post("/sqs/{subject}")
def sqs(subject: str = Path(...), body: dict = Body(...)) -> dict:
    received = {"subject": subject, "body": body}
    return received
