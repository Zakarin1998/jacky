from datetime import datetime

class Income:
    def __init__(self, amount: float, source: str, date: str = None):
        self.amount = amount
        self.source = source
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'amount': self.amount,
            'source': self.source,
            'date': self.date
        }
