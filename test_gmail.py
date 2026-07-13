from services.gmail_service import get_email_text
from workflows.meeting_workflow import run_workflow

print("Checking Gmail...")

email = get_email_text()

print("\nEMAIL RECEIVED:\n")
print(email)

print("\nRUNNING AI AGENT...\n")

result = run_workflow(email)

print(result)