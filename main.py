from services.gmail_service import get_gmail_service, fetch_today_emails, get_email_content
from services.summarizer_service import summarize_content
from utils.cleaner import clean_text

def main():
    service = get_gmail_service()
    messages = fetch_today_emails(service)

    if not messages:
        print("📭 No new emails today.")
        return

    summaries = []
    for msg in messages:
        sender, subject, body = get_email_content(service, msg['id'])
        clean_body = clean_text(body)
        full_content = f"From: {sender}\nSubject: {subject}\n\n{clean_body}"

        print("📩 EMAIL:\n", full_content[:300], "...")

        summary = summarize_content(full_content)
        summaries.append(f"\n🧠 SUMMARY of {subject}:\n{summary}")

    print("\n📚 DAILY SUMMARY REPORT")
    for s in summaries:
        print(s)

if __name__ == "__main__":
    main()
