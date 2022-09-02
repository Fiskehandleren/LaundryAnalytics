# LaundryAnalytics
## Current distribution
<img src="current_predictions.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />

## How?
- Parsing my Gmail for email confirmations for laundry slots.
- Currently classifies a laundry-session as a binary event. (Future work would be playing around with the length of the sessions.)
- Fitting a logistic regression model on the data to obtain the probabilities for a laundry session to take place $k$ days after the last session. 

## TODO
- [ ] Find metoder til at interpolere gap i data fra da jeg var på udveksling
- [ ] Lav script til at sende alert når $\mathbb{P}(booking_i) >= treshhold$
- [ ] Få Github actions til at køre script hver dag
- [ ] Send email når relevant
