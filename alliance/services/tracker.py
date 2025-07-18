from models.user import User
from models.income import Income
from models.expense import Expense


class FinanceTracker:
    def __init__(self, storage):
        self.storage = storage
        self.data = self.storage.load()
        self.user = User(self.data.get('profile', {}))

    def update_profile(self, updates: dict):
        self.user.update(updates)
        self.data['profile'] = self.user.to_dict()
        self.storage.save(self.data)

    def add_income(self, income: Income):
        self.data['incomes'].append(income.to_dict())
        self.storage.save(self.data)

    def add_expense(self, expense: Expense):
        self.data['expenses'].append(expense.to_dict())
        self.storage.save(self.data)

    def get_summary(self):
        total_inc = sum(i['amount'] for i in self.data.get('incomes', []))
        total_exp = sum(e['amount'] for e in self.data.get('expenses', []))
        total_ded = sum(e['amount'] for e in self.data.get('expenses', []) if e.get('deductible'))
        return {
            'total_income': total_inc,
            'total_expense': total_exp,
            'total_deductibles': total_ded,
            'net_balance': total_inc - total_exp
        }

    def list_items(self, item_type: str):
        return self.data.get(item_type, [])