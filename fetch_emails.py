import logging
from plyer import notification
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Configure logging
logging.basicConfig(
    filename='app.log',  # Log file
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

def send_notification(title, message):
    """Send a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Duration in seconds
    )

def get_message_details(service, msg_id):
    """Fetch message details by ID."""
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    headers = message['payload']['headers']
    snippet = message.get('snippet', '')
    
    # Extract useful headers like Subject and From
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
    sender = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")
    
    return subject, sender, snippet

def list_messages():
    # Load credentials from token.json
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Fetch a list of messages
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        logging.info("No messages found.")
        print("No messages found.")
    else:
        print("Recent Emails:")
        for msg in messages:
            subject, sender, snippet = get_message_details(service, msg['id'])
            
            # Log the details
            logging.info(f"Message ID: {msg['id']} | From: {sender} | Subject: {subject}")
            
            # Print the details to console
            print(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n{'-'*50}")
            
            # Send a notification for important emails
            if "urgent" in subject.lower() or "important" in subject.lower():
                send_notification("Important Email Alert!", f"From: {sender}\nSubject: {subject}")

if __name__ == "__main__":
    list_messages()
