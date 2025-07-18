import os
import json
import argparse
from datetime import datetime

# File di storage
DATA_FILE = os.path.expanduser('~/.finance_tracker.json')

# Configurazione iniziale se non esiste
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({'profile': {}, 'incomes': [], 'expenses': [], 'deductibles': []}, f, indent=4)


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def cmd_profile(args):
    """
    Imposta o mostra il profilo personale
    """
    data = load_data()
    if args.set:
        # Parametri da settare: chiave=valore
        for kv in args.set:
            key, val = kv.split('=', 1)
            # prova a convertire numeri
            try:
                val = float(val) if '.' in val else int(val)
            except:
                pass
            data['profile'][key] = val
        save_data(data)
        print("Profilo aggiornato.")
    else:
        print("Profilo corrente:")
        for k, v in data['profile'].items():
            print(f"- {k}: {v}")


def cmd_add_income(args):
    """
    Aggiunge un'entrata
    """
    data = load_data()
    income = {
        'amount': args.amount,
        'source': args.source,
        'date': args.date or datetime.now().strftime('%Y-%m-%d')
    }
    data['incomes'].append(income)
    save_data(data)
    print("Entrata registrata.")


def cmd_add_expense(args):
    """
    Aggiunge una spesa
    """
    data = load_data()
    expense = {
        'amount': args.amount,
        'category': args.category,
        'date': args.date or datetime.now().strftime('%Y-%m-%d'),
        'deductible': args.deductible,
        'notes': args.notes
    }
    data['expenses'].append(expense)
    if args.deductible:
        data['deductibles'].append(expense)
    save_data(data)
    print("Spesa registrata.")


def cmd_list(args):
    """
    Lista di entrate/spese/deduzioni
    """
    data = load_data()
    items = data.get(args.type)
    print(f"--- {args.type.capitalize()} ---")
    total = 0
    for item in items:
        print(item)
        total += item.get('amount', 0)
    print(f"Totale {args.type}: {total}")


def cmd_summary(args):
    """
    Riepilogo finanziario
    """
    data = load_data()
    total_inc = sum(i['amount'] for i in data['incomes'])
    total_exp = sum(e['amount'] for e in data['expenses'])
    total_ded = sum(d['amount'] for d in data['deductibles'])
    print("=== Riepilogo finanziario ===")
    print(f"Entrate totali: {total_inc}")
    print(f"Uscite totali: {total_exp}")
    print(f"Deduzioni totali: {total_ded}")
    print(f"Saldo netto: {total_inc - total_exp}")


def main():
    parser = argparse.ArgumentParser(description="CLI per gestione finanze personali e profilo fiscale")
    sub = parser.add_subparsers(dest='command')

    # Profile
    p_prof = sub.add_parser('profile', help='Mostra o imposta parametri personali')
    p_prof.add_argument('--set', nargs='+', help='Chiavi da impostare, es: eta=27 isee=19000')
    p_prof.set_defaults(func=cmd_profile)

    # Add income
    p_inc = sub.add_parser('add-income', help='Aggiunge una entrata fissa o straordinaria')
    p_inc.add_argument('amount', type=float, help='Importo in euro')
    p_inc.add_argument('source', help='Fonte dell\'entrata')
    p_inc.add_argument('--date', help='Data nel formato YYYY-MM-DD')
    p_inc.set_defaults(func=cmd_add_income)

    # Add expense
    p_exp = sub.add_parser('add-expense', help='Aggiunge una spesa')
    p_exp.add_argument('amount', type=float, help='Importo in euro')
    p_exp.add_argument('category', help='Categoria es: affitto, mutuo, assicurazione')
    p_exp.add_argument('--date', help='Data nel formato YYYY-MM-DD')
    p_exp.add_argument('--deductible', action='store_true', help='Se la spesa è fiscalmente deducibile')
    p_exp.add_argument('--notes', default='', help='Note aggiuntive')
    p_exp.set_defaults(func=cmd_add_expense)

    # List
    p_list = sub.add_parser('list', help='Lista di items')
    p_list.add_argument('type', choices=['incomes', 'expenses', 'deductibles'], help='Tipo di lista')
    p_list.set_defaults(func=cmd_list)

    # Summary
    p_sum = sub.add_parser('summary', help='Riepilogo finanziario')
    p_sum.set_defaults(func=cmd_summary)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
