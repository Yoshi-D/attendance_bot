import imaplib
import email
import re
from password import password_extraction

EMAIL = '2023UMA0239@iitjammu.ac.in'
PASSWORD = password_extraction("mail_password")

def fetch_otp():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    for e_id in email_ids[:-5:-1]:  # Check last 5 unread emails
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1].decode("utf-8")

        msg = email.message_from_string(raw_email)
        subject = msg["Subject"]

        if 'OTP' in subject:
            body = msg.get_payload(decode=True).decode("utf-8")
            pattern = r"\b\d{6}\b"
            matches = re.findall(pattern, body)
            mail.logout()
            if matches:
                return matches[0]
        fetch_otp()
    mail.logout()
    print("OTP Not Found")
    return None
