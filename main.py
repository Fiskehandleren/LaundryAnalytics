import mail_retriever
from mailer import Mailer
from predictor import Predictor
import logging
import argparse


def setup_logging():
    """Setup logging in both console and file."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s: %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M',
        filename='mails.log',
        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    # Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
    parser.add_argument("-c", "--cache", help="use cached data", action="store_true", default=False)
    parser.add_argument("-p", "--password", help="password for email account", type=str, default=None)
    parser.add_argument("-u", "--username", help="username for email account", type=str, default=None)
    parser.add_argument("-s", "--subset", help="subset of data to use", action="store_true", default=True)
    parser.add_argument("-t", "--threshold", help="threshold for model to classify event", type=float, default=0.8)

    args = parser.parse_args()
    setup_logging()

    if args.username is None or args.password is None:
        if args.cache is False:
            logging.error("Username and password must be provided if cache is not used. Else use -c flag.")
            parser.print_help()
            exit(1)
        else:
            logging.warning("No email will be sent if no email credentials are provided.")
            mail_login = None
            mail_pwd = None

    mail_login = args.username
    mail_pwd = args.password

    if args.cache == 1:
        mr = mail_retriever.MailRetriever(use_cache=True)
    else:
        mr = mail_retriever.MailRetriever(mail_login, mail_pwd, use_cache=args.cache, retrieve_after=False)
    mr.get_mails()

    # Temp hack until interpolation is implemented
    if args.subset:
        predictor = Predictor(use_data_after_date="2022-05-11")
    else:
        predictor = Predictor()

    predictor.parse_bookings()
    predictor.fit_model()
    predictor.predict(args.threshold)
    logging.info(predictor.metrics)
    if predictor and len(predictor.predictions) > 0:
        logging.debug(predictor.predictions)
        # index into first key
        logging.info(f"Laundry slot should be booked at {predictor.predictions.iloc[0]}")
        if mail_login and mail_pwd:
            mailer = Mailer(predictor.predictions).send_mail_2(mail_login, mail_pwd, mail_login, "Laundry slot prediction")
            logging.info("Email sent.")

    logging.info("Done")
