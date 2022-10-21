
from email.headerregistry import Address
from email.message import EmailMessage
import smtplib


class Mailer:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    root = None

    def __init__(self, predictions):
        self.predictions = predictions

    def send_mail_2(self, mail_login, mail_pwd, mail_to, subject):
        self.root = EmailMessage()
        user, domain = mail_login.split("@")
        self.root['Subject'] = subject
        self.root['From'] = Address("Laundry Prediction", user, domain)
        self.root['To'] = Address(mail_to, user, domain)
        self.root.set_content("""Your next booking should be """)
        self.add_body_text()

        # Send the message via local SMTP server.
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as s:
            s.starttls()
            s.login(mail_login, mail_pwd)
            s.send_message(self.root)

    def add_body_text(self):
        body = "<h1> Hello </h1>"
        date = self.predictions.iloc[0].date
        body += f"Your next booking should be at {date} calculated with probability {self.predictions.iloc[0].prediction * 100 : 0.2f}%.\n\n"
        # make list of predictions
        body += "<h2> Predictions </h2>"
        body += self.predictions.to_html(classes="table table-striped")
        self.root.add_alternative(body, subtype='html')

