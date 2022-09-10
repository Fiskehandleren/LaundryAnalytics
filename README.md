# LaundryAnalytics
## Current distribution
<img src="current_predictions.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />

## How?
- Parsing receipts for laundry bookings from the digital owner's association management tool [Probo](https://www.prosedo.dk).
- Parsing my Gmail using `imaplib` for email confirmations for laundry slots. Only mails NOT deleted (not archived) will be retrieved. 
- Currently classifies a laundry-session as a binary event. (Future work would be playing around with the length of the sessions.)
- Fitting a logistic regression model on the data to obtain the probabilities for a laundry session to take place $k$ days after the last session. 

## Future work
- [ ] Find methods to interpolate gap in data from my semester abroad (January 22' to May 22').
- [ ] Make script to trigger some action, once $\mathbb{P}(booking_i) >= treshhold$
- [ ] Make Github Actions run this script with a given frequency
- [ ] Make script alert by sending an email 
