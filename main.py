import mail_retriever
from predictor import Predictor
import logging
import argparse

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

    if args.cache == 1:
        mr = mail_retriever.MailRetriever(use_cache=True)
    else:
        if args.username is None or args.password is None:
            logging.error("Username and password must be provided if cache is not used. Else use -c flag.")
            parser.print_help()
            exit(1)
        mail_login = args.username
        mail_pwd = args.password
        mr = mail_retriever.MailRetriever(mail_login, mail_pwd, use_cache=args.cache, retrieve_after=False)
    mr.get_mails()

    # Temp hack until interpolation is implemented
    if args.subset:
        predictor = Predictor(use_data_after_date="2022-05-11")
    else:
        predictor = Predictor()

    predictor.parse_bookings()
    print(predictor.data.head(-5))
    predictor.fit_model()
    predictor.predict(args.threshold)
    logging.info(predictor.predictions)
    logging.info(predictor.metrics)
    logging.info("Done")
