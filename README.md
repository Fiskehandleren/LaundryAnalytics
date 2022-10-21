# LaundryAnalytics
## Prerequisites 
- A Gmail account with archived mails from the Probo mailing system
- An app password to login to Gmail.

If you don't have above, you can simply play around by selecting to use cached data when prompted.

## Running the scripts
`> python main.py` produces the `current_predictions.png` - and overview of the probability of an event happening the next 14 days after the last event.


## How?
- Parsing receipts for laundry bookings from the digital owner's association management tool [Probo](https://www.prosedo.dk).
- Parsing my Gmail using `imaplib` for email confirmations for laundry slots. Only mails NOT deleted (not archived) will be retrieved. 
- Currently classifies a laundry-session as a binary event. (Future work would be playing around with the length of the sessions.)
- Fitting a logistic regression model on the data to obtain the probabilities for a laundry session to take place $k$ days after the last session. 

## Future work
- [ ] Find methods to interpolate gap in data from my semester abroad (January 22' to May 22').
- [ ] Lookup calendar to find best slot for laundry session.
- [ ] Play around with time series models
- [ ] Make script update cache with newer data than latest entry