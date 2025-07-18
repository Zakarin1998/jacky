import matplotlib.pyplot as plt

def simula_investimento(
    capitale_iniziale=40000,
    rendimento_percentuale=1,
    durata_anni=1,
    capitalizzazione_mensile=True
):
    # Parametri base
    periodo = durata_anni * 12 if capitalizzazione_mensile else durata_anni
    frequenza = "Mensile" if capitalizzazione_mensile else "Annuale"
    tasso = rendimento_percentuale / 100

    if capitalizzazione_mensile:
        tasso_periodico = tasso
    else:
        tasso_periodico = tasso

    capitale = capitale_iniziale
    valori = [capitale]
    mesi = [0]

    # Simulazione
    for i in range(1, periodo + 1):
        capitale *= (1 + tasso_periodico)
        valori.append(capitale)
        mesi.append(i)

    # Output finale
    print(f"📈 Dopo {durata_anni} anni ({frequenza}), da {capitale_iniziale:.2f}€ arrivi a {capitale:.2f}€")
    print(f"💰 Guadagno: {capitale - capitale_iniziale:.2f}€")

    # Grafico
    plt.figure(figsize=(10, 5))
    plt.plot(mesi, valori, marker='o', linestyle='-', color='green')
    plt.title(f'Crescita Capitale ({frequenza}) - Rendimento {rendimento_percentuale}%')
    plt.xlabel('Periodo (mesi)' if capitalizzazione_mensile else 'Periodo (anni)')
    plt.ylabel('Capitale (€)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 🔧 ESEMPIO DI USO
simula_investimento(
    capitale_iniziale=40000,
    rendimento_percentuale=1,  # rendimento mensile
    durata_anni=1,
    capitalizzazione_mensile=True
)
