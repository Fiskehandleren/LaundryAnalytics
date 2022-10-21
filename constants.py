from enum import auto, Flag


class Metrics(Flag):
    F1_SCORE = auto()
    ACCURACY = auto()


# Mail
LAUNDRY_CONFIRMATION_EMAIL = "noreply@noreply.prosedo.dk"
GMAIL_IMAP = "imap.gmail.com"
GMAIL_FOLDER_QUERY = '"[Gmail]/Alle mails"'
BOOKING_DATE_REGEX = r"([0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:(30|00))"

# Data
DATA_PATH = "bookings.csv"
