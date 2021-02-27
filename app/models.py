from app import db
from datetime import datetime
import requests
import json


class TelegramUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exchange_data = db.Column(db.Text())
    exchange_data_saved_at = db.Column(db.DateTime, index=True)

    def exchange_rates(self):
        #  if user has saved exchange data that contains less than 10 minutes
        if self.exchange_data_saved_at and not time_elapsed(10, self.exchange_data_saved_at.timestamp(),
                                                            datetime.utcnow().timestamp()):
            rates = json.loads(self.exchange_data).get('rates')
        else:
            response = requests.get(url="https://api.exchangeratesapi.io/latest", params={'base': 'USD'})
            if not response:
                return None
            self.exchange_data = response.text  # store json as text in a database
            self.exchange_data_saved_at = datetime.utcnow()
            db.session.add(self)
            db.session.commit()
            rates = response.json().get('rates')
        return rates

    def __repr__(self):
        return '<TelegramUser {}>'.format(self.id)


def time_elapsed(minutes, timestamp1, timestamp2):
    print((timestamp2-timestamp1)/60.0)
    if (timestamp2-timestamp1)/60.0 < minutes:
        return False
    return True

