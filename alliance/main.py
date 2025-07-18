import typer
from models.income import Income
from models.expense import Expense
from storage.json_store import JSONStorage
from services.tracker import FinanceTracker

app = typer.Typer()
storage = JSONStorage()
tracker = FinanceTracker(storage)


@app.command()
def profile(
    eta: int = typer.Option(None, help="Età dell'utente"),
    isee: float = typer.Option(None, help="ISEE corrente"),
    regione: str = typer.Option(None, help="Regione di residenza")
):
    """
    Mostra o aggiorna il profilo utente.
    """
    updates = {}
    if eta is not None:
        updates["eta"] = eta
    if isee is not None:
        updates["isee"] = isee
    if regione is not None:
        updates["regione"] = regione

    if updates:
        tracker.update_profile(updates)
        typer.echo("Profilo aggiornato.")
    else:
        typer.echo("Profilo corrente:")
        for k, v in tracker.user.to_dict().items():
            typer.echo(f"- {k}: {v}")


@app.command()
def add_income(
    amount: float = typer.Argument(..., help="Importo in euro"),
    source: str = typer.Argument(..., help="Fonte dell'entrata"),
    date: str = typer.Option(None, help="Data nel formato YYYY-MM-DD"),
):
    """
    Aggiunge una nuova entrata.
    """
    inc = Income(amount=amount, source=source, date=date)
    tracker.add_income(inc)
    typer.echo("Entrata registrata.")


@app.command()
def add_expense(
    amount: float = typer.Argument(..., help="Importo in euro"),
    category: str = typer.Argument(..., help="Categoria della spesa"),
    date: str = typer.Option(None, help="Data nel formato YYYY-MM-DD"),
    deductible: bool = typer.Option(False, help="Spesa fiscalmente deducibile"),
    notes: str = typer.Option("", help="Note opzionali"),
):
    """
    Aggiunge una nuova spesa.
    """
    exp = Expense(amount=amount, category=category, date=date, deductible=deductible, notes=notes)
    tracker.add_expense(exp)
    typer.echo("Spesa registrata.")


@app.command()
def list_items(type: str = typer.Argument(..., help="Tipo: incomes, expenses, o deductibles")):
    """
    Elenca elementi salvati (incomes, expenses, deductibles)
    """
    valid_types = ['incomes', 'expenses', 'deductibles']
    if type not in valid_types:
        typer.echo(f"Tipo non valido. Scegli tra: {', '.join(valid_types)}")
        raise typer.Exit(code=1)

    items = tracker.list_items(type)
    total = 0
    typer.echo(f"--- {type.capitalize()} ---")
    for item in items:
        typer.echo(str(item))
        total += item.get("amount", 0)
    typer.echo(f"Totale: {total} €")


@app.command()
def summary():
    """
    Mostra un riepilogo finanziario completo.
    """
    s = tracker.get_summary()
    typer.echo("=== Riepilogo Finanziario ===")
    typer.echo(f"Entrate totali:     {s['total_income']} €")
    typer.echo(f"Uscite totali:      {s['total_expense']} €")
    typer.echo(f"Deduzioni totali:   {s['total_deductibles']} €")
    typer.echo(f"Saldo netto:        {s['net_balance']} €")


if __name__ == "__main__":
    app()
