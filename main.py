import mail_retriever
from predictor import Predictor
import logging 

if __name__ == "__main__":

    caching = int(input("Use cache? (0/1): "))
    if caching == 1:
        mr = mail_retriever.MailRetriever(use_cache=True)
    else:
        mail_login = input("Mail login: ")
        mail_pwd = input("Mail password: ")
        mr = mail_retriever.MailRetriever(mail_login, mail_pwd, use_cache=caching, retrieve_after=False)
    mr.get_mails()

    # Temp hack until interpolation is implemented
    if int(input("Enable post NUS exchange data only? (0/1): ")):
        predictor = Predictor(use_data_after_date="2022-05-11")
    else:
        predictor = Predictor()

    predictor.parse_bookings()
    print(predictor.data.head(-5))
    predictor.fit_model()
    predictor.predict()

    logging.info("Done")