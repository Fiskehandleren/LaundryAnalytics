from datetime import datetime
import imaplib
import email
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle 

REGEX = r"([0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:(30|00))"

class Booking:
    def __init__(self, date, start_time, end_time):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.total_time_hours = (end_time-start_time).seconds/3600
    
    def __str__(self):
        return "{} {} to {}, total: {} hours ".format(self.date, self.start_time.time(), self.end_time.time(), self.total_time_hours)
    
    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_time_hours': self.total_time_hours
        }

class MailRetriever:
    def __init__(self, mail_login, mail_pwd, use_cache=False) -> None:
        self.mail_login = mail_login
        self.mail_pwd = mail_pwd
        self.imap_server = "imap.gmail.com"
        self.bookings = []
        self.use_cache = use_cache
    
    def init_imap(self):
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.mail_login, self.mail_pwd)
        self.imap.select('"[Gmail]/Alle mails"', readonly=True)

    @staticmethod
    def extract_booking_time(parsed_html):
        for i in parsed_html:
            if (result := re.findall(REGEX, i.text)) != []:
                start_time = datetime.strptime(result[0][0], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(result[1][0], "%Y-%m-%d %H:%M:%S")
                date = start_time.date()
                return Booking(date, start_time, end_time)

    def get_mails(self) -> list:
        if self.use_cache:
            try:
                f = open("bookings.pkl", "rb")
                self.bookings = pickle.load(f)
                self.consolidate_bookings()
                return
            except FileNotFoundError:
                print("No cache found. Retrieving mails...")
   
        self.init_imap()
        status, messages = self.imap.search(None, '(FROM "noreply@noreply.prosedo.dk")')
        if status != 'OK':
            raise Exception("Error searching Inbox.")

        for message_uid in messages[0].split():
            _, msg = self.imap.fetch(message_uid.decode(), "(RFC822)")
            for response in msg:
                if not isinstance(response, tuple):
                    continue

                msg = email.message_from_bytes(response[1])
                if msg.is_multipart():
                    # One laundry-session might consist of two bookings
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/html" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            parsed_html = BeautifulSoup(body, features="lxml")
                            soup = parsed_html.body.find_all('p')
                            self.bookings.append(self.extract_booking_time(soup))
                break
        self.imap.close()
        self.imap.logout()
        self.consolidate_bookings()
        self.persist_data()

    def persist_data(self):
        open_file = open("bookings.pkl", "wb")
        pickle.dump(self.bookings, open_file)
        open_file.close()

    def consolidate_bookings(self):
        df = pd.DataFrame.from_records([b.to_dict() for b in self.bookings if b is not None])
        # remove duplicates
        df.drop_duplicates(inplace=True)
        df = df.groupby('date').agg({'start_time': 'min', 'end_time': 'max', 'total_time_hours': 'sum'})
        df.to_csv("bookings.csv")