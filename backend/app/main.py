import os
import time
from threading import Lock

from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware

from app.agent import generate_email
from app.config import SEND_DELAY_SECONDS
from app.csv_reader import read_leads
from app.email_sender import send_email


app = FastAPI(
    title="AI Email Agent",
    description="AI-powered personalized email outreach system",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


campaign_state = {
    "status": "idle",
    "total": 0,
    "processed": 0,
    "sent": 0,
    "failed": 0,
    "current_lead": None,
    "error": None,
}

campaign_lock = Lock()

uploaded_file_path = "data/leads.csv"



@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/campaign/upload")
async def upload_csv(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported",
        )

    contents = await file.read()

    os.makedirs(
        "data",
        exist_ok=True,
    )

    with open(
        uploaded_file_path,
        "wb",
    ) as output_file:

        output_file.write(contents)

    try:
        leads = read_leads(
            uploaded_file_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    with campaign_lock:

        campaign_state["status"] = "ready"
        campaign_state["total"] = len(leads)
        campaign_state["processed"] = 0
        campaign_state["sent"] = 0
        campaign_state["failed"] = 0
        campaign_state["current_lead"] = None
        campaign_state["error"] = None

    return {
        "message": "CSV uploaded successfully",
        "filename": file.filename,
        "total_leads": len(leads),
    }



def process_campaign():

    try:

        leads = read_leads(
            uploaded_file_path
        )

        for index, lead in enumerate(
            leads,
            start=1,
        ):

            with campaign_lock:

                campaign_state[
                    "current_lead"
                ] = lead["name"]

            try:

                print(
                    f"[{index}/{len(leads)}] "
                    f"Processing {lead['name']}"
                )

                # --------------------------------
                # Generate personalized email
                # --------------------------------

                email = generate_email(
                    lead
                )
                
                print("=" * 60)
                print("LEAD BEING PROCESSED")
                print(f"Name: {lead['name']}")
                print(f"Email: {lead['email']}")
                print(f"Company: {lead['company']}")
                print(f"Role: {lead['role']}")

                print("\nGENERATED EMAIL")
                print(f"Subject: {email['subject']}")
                print(f"Body:\n{email['body']}")

                print("\nSENDING TO")
                print(lead["email"])
                print("=" * 60)

                print(
                    f"Generated: "
                    f"{email['subject']}"
                )


                send_email(
                    recipient=lead["email"],
                    subject=email["subject"],
                    body=email["body"],
                )

                print(
                    f"Sent to {lead['email']}"
                )

                with campaign_lock:

                    campaign_state[
                        "sent"
                    ] += 1

            except Exception as error:

                print(
                    f"Failed for "
                    f"{lead['email']}: {error}"
                )

                with campaign_lock:

                    campaign_state[
                        "failed"
                    ] += 1

            finally:

                with campaign_lock:

                    campaign_state[
                        "processed"
                    ] += 1


            if index < len(leads):

                time.sleep(
                    SEND_DELAY_SECONDS
                )

        with campaign_lock:

            campaign_state[
                "status"
            ] = "completed"

            campaign_state[
                "current_lead"
            ] = None

    except Exception as error:

        with campaign_lock:

            campaign_state[
                "status"
            ] = "failed"

            campaign_state[
                "error"
            ] = str(error)



@app.post("/api/campaign/start")
def start_campaign(
    background_tasks: BackgroundTasks,
):

    with campaign_lock:

        if campaign_state["status"] == "running":

            raise HTTPException(
                status_code=400,
                detail="Campaign is already running",
            )

        if campaign_state["total"] == 0:

            raise HTTPException(
                status_code=400,
                detail="Upload a CSV first",
            )

        campaign_state[
            "status"
        ] = "running"

        campaign_state[
            "processed"
        ] = 0

        campaign_state[
            "sent"
        ] = 0

        campaign_state[
            "failed"
        ] = 0

        campaign_state[
            "error"
        ] = None

    background_tasks.add_task(
        process_campaign
    )

    return {
        "message": "Campaign started"
    }



@app.get("/api/campaign/status")
def get_campaign_status():

    with campaign_lock:

        return campaign_state.copy()