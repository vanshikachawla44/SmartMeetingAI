from rag.query_engine import ask_rag
from pydantic import BaseModel
from fastapi import FastAPI

from agents.extraction_agent import extract_meeting_details
from agents.meeting_scheduler_agent import schedule_meeting
from agents.slot_finder_agent import find_best_slot
from agents.calendar_agent import get_available_slots
from agents.intent_agent import detect_intent
from agents.logger_agent import save_meeting

from workflows.meeting_workflow import run_workflow
from services.history_service import get_all_meetings

app = FastAPI()


class EmailRequest(BaseModel):
    email_text: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "project": "SmartMeetingAI",
        "status": "Running"
    }


@app.get("/test-meeting")
def test_meeting():

    email = """
    Let's schedule a meeting next week
    """

    intent = detect_intent(email)

    return {
        "email": email,
        "intent": intent
    }


@app.get("/available-slots")
def available_slots():

    slots = get_available_slots()

    return {
        "available_slots": slots
    }


@app.get("/best-slot")
def best_slot():

    slots = get_available_slots()

    best = find_best_slot(slots)

    return {
        "best_slot": best
    }


@app.get("/extract")
def extract():

    email = """
    Let's schedule a project discussion next Tuesday at 2 PM with John and Sarah.
    """

    return {
        "details": extract_meeting_details(email)
    }


@app.post("/workflow")
def workflow(request: EmailRequest):

    return run_workflow(request.email_text)


@app.get("/meetings")
def get_meetings():

    meetings = get_all_meetings()

    return {
        "total_meetings": len(meetings),
        "meetings": meetings
    }


@app.get("/add-test-meeting")
def add_test_meeting():

    save_meeting({
        "intent": "meeting",
        "best_slot": "Tuesday 2:00 PM",
        "participants": ["John", "Sarah"]
    })

    return {
        "message": "Test meeting added successfully"
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = ask_rag(request.question)

    return {
        "question": request.question,
        "answer": answer
    }