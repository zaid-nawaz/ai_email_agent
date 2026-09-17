import time

from app.config import SEND_DELAY_SECONDS
from app.csv_reader import read_leads
from app.agent import generate_email
from app.email_sender import send_email


CSV_FILE = "data/leads.csv"


def main():

    print("Starting AI Email Agent...")
    print()

    leads = read_leads(CSV_FILE)

    print(f"Loaded {len(leads)} leads.")
    print()

    total = len(leads)

    for index, lead in enumerate(leads, start=1):

        print(
            f"[{index}/{total}] "
            f"Processing {lead['name']}..."
        )

        try:

            # -----------------------------
            # 1. Generate personalized email
            # -----------------------------

            print(
                "  → Generating personalized email..."
            )

            email = generate_email(lead)

            print(
                f"  → Subject: {email['subject']}"
            )

            # -----------------------------
            # 2. Send email
            # -----------------------------

            print(
                f"  → Sending to {lead['email']}..."
            )

            send_email(
                recipient=lead["email"],
                subject=email["subject"],
                body=email["body"]
            )

            print(
                "  ✓ Sent successfully"
            )

        except Exception as e:

            print(
                f"  ✗ Failed: {str(e)}"
            )

        # -----------------------------
        # 3. Wait before next email
        # -----------------------------

        if index < total:

            print(
                f"  Waiting "
                f"{SEND_DELAY_SECONDS} seconds..."
            )

            time.sleep(
                SEND_DELAY_SECONDS
            )

        print()

    print("Campaign completed.")


if __name__ == "__main__":
    main()