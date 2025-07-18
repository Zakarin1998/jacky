from datetime import datetime

class Expense:
    def __init__(self, amount: float, category: str, date: str = None, deductible: bool = False, notes: str = ''):
        self.amount = amount
        self.category = category
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.deductible = deductible
        self.notes = notes

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'deductible': self.deductible,
            'notes': self.notes
        }
