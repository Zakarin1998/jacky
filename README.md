# Jacky Chan Dollar - Public Repository


## $JCD Frontend Original Website - Context about the project

This repository contains the original $JCD Website (html, css, images).
This allows others to make their own versions or help maintenence.

## 🥳 Web2Update - Staking coming soon!
After long time, this project is almost ready to the next phase.
Uniswap V4 allows for higher rewards due to gas optimization and $JCD will have soon a strategy running around

Website Update -> updated React-Vite Interface + express server

## 🥳 Web3  Update - Uniswap V3-v4 JCD Report

Segue un report dettagliato per chiarire i concetti di base di Uniswap V3, il “rate” (prezzo), market cap, e cosa è successo con il presunto “dump” su JCD/ETH:

---

## 🔍 1. Fondamentali: rate, prezzo, market cap

* **Rate = prezzo spot** nel pool, cioè quanti token ETH ottieni in cambio di 1 JCD (o viceversa). In Uniswap V3, questo è calcolato come riserva\_token1 / riserva\_token0, esattamente come nei modelli tradizionali *constant product* ([mixbytes.io][1]).
* **Market cap** è semplicemente (supply\_totale × prezzo\_market). Se il prezzo scende — a causa di vendite — pure il market cap cala di conseguenza.

---

## 📉 2. Uniswap V3: “concentrated liquidity” e ticks

* In Uniswap V2, la liquidità era distribuita uniformemente tra prezzo 0 e ∞. In V3, invece, i fornitori possono scegliere un **intervallo di prezzo** — ad esempio da 100 a 150 000 JCD/ETH — e concentrare lì la loro liquidità ([uniswapv3book.com][2]).
* Questi intervalli sono gestiti tramite **ticks**, ognuno corrisponde a uno step di \~0,01% nel prezzo ([mixbytes.io][1]).
* La liquidità è “attiva” solo se il prezzo è **all’interno** dell’intervallo. Se il prezzo esce, il LP resta con **solo uno** dei due token — prevista una specie di “limit order passivo” ([docs.uniswap.org][3]).

---

## 3. 🧮 Calcoli della matematica di base

* Il pool mantiene una costante $x \cdot y = k$, dove $x$ e $y$ sono riserve dei due token. La **liquidità L** è correlata alla **radice quadrata** di queste riserve ([mixbytes.io][1]).
* Gli LP devono calcolare quanta quantità di token depositare per un intervallo:

  * Dentro l’intervallo: i depositi dipendono da √$P$ (prezzo) e tick bounds ([blog.uniswap.org][4]).
  * Fuori intervallo: il pool si trasforma in una sola riserva (solo JCD o solo ETH a seconda della direzione).
* Formule concrete: vedi equazioni nel paper “LIQUIDITY MATH IN UNISWAP V3” ([atiselsts.github.io][5]).

---

## 4. 🏦 Minting, fees, impermanent loss

* LP guadagnano solo **se il prezzo rimane nel loro intervallo** — ci guadagnano fee swap. Se il prezzo esce, i guadagni cessano .
* Riposizionamenti o aggiustamenti di intervallo richiedono **gas fee**, e il rischio di **impermanent loss** aumenta in intervalli stretti ([arxiv.org][6]).

---

## 5. Cosa è successo su JCD/ETH? Il “dump”

### 📉 Vendite massive (“dump”)

* Gruppi di utenti (i cosiddetti “dumpster”) hanno venduto una grossa quantità di JCD in cambio di ETH, causando un calo del rate JCD/ETH da \~2 ETH a \~1.31 ETH. Questo ha spostato il prezzo fuori dagli intervalli di molti LP, generando disattivazione delle loro posizioni e meno fee generate.

### 🧑‍💼 Ritiro LP & fee

* Il “tizio che ha tolto LP e fees” ha probabilmente:

  1. Aggiunto liquidità in un intervallo preciso (es. 1.8–2.2 ETH per JCD).
  2. Guaragnato molte fee di swap mentre il prezzo era ancora in intervallo.
  3. Subito dopo un grosso dump (o lo ha causato), quando il prezzo si è spostato a \~1.31, ha rimosso la sua posizione (prelevando sia JCD che ETH più le fee).&#x20;
* Questo tipo di strategia è un esempio di **range trading, raccolta fee, e uscita strategica** al cambio intervallo.

---

## 6. 🧩 Conclusione strategica

| Fattore                 | Impatto                                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Intervallo scelto**   | Più è stretto → più fee potenziali, ma alta probabilità che il prezzo lo superi.                                             |
| **Dump improvviso**     | Sposta prezzo fuori range → LP non guadagnano più fee.                                                                       |
| **Tempismo nel ritiro** | Chi ritira dopo il calo incassa fee e residuo token. Può risultare profittevole rispetto a chi resta nel range e subisce IL. |

LP avanzati bilanciano **fee potenziali**, **gas per riposizionamento**, e **rischio di IL**, che studi accademici dettagliano bene .

---

### ✅ In sintesi

* **Rate** = prezzo JCD/ETH nel pool.
* In Uniswap V3, la liquidità può essere **concentrata** in range price-specifici tramite ticks.
* I LP guadagnano **fee solo se il prezzo resta in range**; altrimenti l’investimento diventa one-token e non produce fee.
* I dump massivi possono **abbattere il prezzo**, facendo uscire il prezzo dal range e che chi ritira al momento giusto incassa più degli altri.

Se vuoi posso mostrarti esempi concreti di calcoli su JCD usando sqrtPriceX96, o simulare l’anno di fee contro impermanent loss su vari range. Fammi sapere!

[1]: https://mixbytes.io/blog/uniswap-v3-ticks-dive-into-concentrated-liquidity?utm_source=chatgpt.com "Uniswap V3 ticks - dive into concentrated liquidity - MixBytes"
[2]: https://uniswapv3book.com/milestone_0/uniswap-v3.html?utm_source=chatgpt.com "Uniswap V3 Development Book"
[3]: https://docs.uniswap.org/concepts/protocol/concentrated-liquidity?utm_source=chatgpt.com "Concentrated Liquidity - Uniswap Docs"
[4]: https://blog.uniswap.org/uniswap-v3-math-primer-2?utm_source=chatgpt.com "A Primer on Uniswap v3 Math Part 2: Stay Awake by Reading it Aloud"
[5]: https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf?utm_source=chatgpt.com "[PDF] LIQUIDITY MATH IN UNISWAP V3 - Atis Elsts"
[6]: https://arxiv.org/abs/2111.09192?utm_source=chatgpt.com "Impermanent Loss in Uniswap v3"


## Uniswap Library

There are some Python snippets in "uni_v1" folder. 
That code is really useful to interact to Uniswap protocol up to V3 version.

Happy coding!

## Background

Certainly! Here is the translation of the previously provided information into English:

The **Jacky Chan Dollar (JCD)** is a cryptocurrency token that holds historical significance in the decentralized finance (DeFi) ecosystem. Launched in 2018, it was the first token swapped on the Uniswap V1 protocol, developed by Jacky Chan, the engineer responsible for building Uniswap's user interface.

**Key Features of JCD:**

- **Historical Origins:** JCD was created in 2018 as part of the initial tests for the Uniswap V1 protocol, marking a significant step towards autonomy from centralized exchanges.

- **Complete Decentralization:** After its launch, Jacky Chan sold all his JCD tokens and relinquished control of the contract, rendering the project entirely decentralized and community-driven.

- **Tokenomics:**
  - **Total Supply:** 19,860,225 JCD.
  - **Circulating Supply:** 11,060,225 JCD.
  - **Community Liquidity:** The liquidity pool is managed by the community.
  - **No Transaction Taxation:** No taxes are applied to transactions (0/0).

- **Contract Security:** The token's contract has been verified and made immutable (renounced), ensuring transparency and security for users.

- **Revival in 2023:** After years of inactivity, JCD was rediscovered in 2023, sparking renewed interest as a historical relic of DeFi, comparable to CryptoPunks and Etheria Tiles.

For further details and insights, you can visit the project's official website

```markdown
- [J Chan Dollar (JCD) ICO Rating and Details | ICOholder](https://icoholder.com/en/j-chan-dollar-1064170)
- [J Chan Dollar (JCD) Token Tracker | Etherscan](https://etherscan.io/token/0x0ed024d39d55e486573ee32e583bc37eb5a6271f)
- [Join the Rebirth of Uniswap’s First Swapped Token Jacky Chan Dollar $JCD in 2023](https://medium.com/@JackyChanDollar/join-the-rebirth-of-uniswaps-first-swapped-token-jacky-chan-dollar-jcd-in-2023-beyond-memes-9e12556632d1)
- [J Chan Dollar (JCD) Price Data | Mobula](https://mobula.io/asset/j-chan-dollar)
- [J Chan Dollar (JCD) Price on Uniswap V3 | GeckoTerminal](https://www.geckoterminal.com/eth/pools/0xaa857f5d0ae092a504fa76ce94cb3d3df5e1a145)
- [J Chan Dollar Token Holders Chart | Etherscan](https://etherscan.io/token/tokenholderchart/0x0Ed024d39d55e486573EE32e583bC37Eb5A6271f)
- [J Chan Dollar / WETH on Ethereum / Uniswap | DEX Screener](https://dexscreener.com/ethereum/0xc894e4a50ed7ffa9ad73da51f8f8233b787f200e)
- [J Chan Dollar Price - JCD to USD | CoinBrain](https://coinbrain.com/coins/eth-0x0ed024d39d55e486573ee32e583bc37eb5a6271f)
- [J Chan Dollar Price on Uniswap V2 | GeckoTerminal](https://www.geckoterminal.com/it/eth/pools/0xc894e4a50ed7ffa9ad73da51f8f8233b787f200e)
- [J Chan Dollar (JCD) Price Today | Moralis](https://moralis.com/chain/ethereum/token/price/j-chan-dollar)
- [J Chan Dollar - $0.008061 (JCD / WETH) on Ethereum / UniswapV3 | DexScout](https://dexscout.app/eth/0x1f123bd9e55f7ef7d3653688cf2248ef4d7f8394)
- [J Chan Dollar Price - JCD Live Chart & Trading Tools | CoinScan](https://www.coinscan.com/tokens/eth/0x1f123bd9e55f7ef7d3653688cf2248ef4d7f8394)
- [J Chan Dollar ICO Rating, Reviews and Details | ICOholder](https://icoholder.com/en/j-chan-dollar-1064170)
- [J Chan Dollar Token Information | Ethplorer](https://ethplorer.io/address/0x0ed024d39d55e486573ee32e583bc37eb5a6271f)
- [Jacky Chan Dollar $JCD - Medium](https://medium.com/@JackyChanDollar)
```

I hope this information is helpful! 

## Cronologia (italiano)
Il **Jacky Chan Dollar (JCD)** è un token crittografico che riveste un'importanza storica nell'ecosistema della finanza decentralizzata (DeFi). Lanciato nel 2018, è stato il primo token scambiato sul protocollo Uniswap V1, sviluppato da Jacky Chan, l'ingegnere responsabile della creazione dell'interfaccia utente di Uniswap.

**Caratteristiche fondamentali del JCD:**

- **Origini Storiche:** Il JCD è stato creato nel 2018 come parte dei test iniziali per il protocollo Uniswap V1, rappresentando un passo significativo verso l'autonomia dagli exchange centralizzati.

- **Decentralizzazione Completa:** Dopo il lancio, Jacky Chan ha venduto tutti i suoi token JCD e ha rinunciato al controllo del contratto, rendendo il progetto completamente decentralizzato e gestito dalla comunità.

- **Tokenomics:**
  - **Offerta Totale:** 19.860.225 JCD.
  - **Offerta Circolante:** 11.060.225 JCD.
  - **Liquidità della Comunità:** Il pool di liquidità è gestito dalla comunità, con il 44% dei token bruciati per sostenere il valore.
  - **Nessuna Tassazione:** Non sono applicate tasse sulle transazioni (0/0).

- **Sicurezza del Contratto:** Il contratto del token è stato verificato e reso immutabile (renounced), garantendo trasparenza e sicurezza per gli utenti.

- **Rinascita nel 2023:** Dopo anni di inattività, il JCD è stato riscoperto nel 2023, suscitando un rinnovato interesse come reliquia storica della DeFi, paragonabile a CryptoPunks ed Etheria Tiles. 

## Prossimi step di sviluppo

# Piano di Sviluppo per l'Ecosistema $JCD

## 1. Executive Summary

Il nostro obiettivo è sfruttare le potenzialità di DAO come StakeDAO per boostare una memecoin basata su Ethereum, in particolare il token $JCD. Attraverso la creazione di una pool su Curve, l’implementazione di una strategia factory per l’autocompound dei rewards e l’offerta di incentivi per i liquidity provider (LP), intendiamo ottenere un APY nativo sulla memecoin. In una seconda fase, svilupperemo una semplice applicazione che permetta agli utenti di:
- Swappare ETH per $JCD, integrando Metamask per l’autenticazione e la gestione dei wallet.
- Interagire con una “strategia di staking” che, in realtà, sarà un’interfaccia wrapper verso la strategia di StakeDAO.

## 2. Obiettivi di Business e Tecnici

- **Business:** Incrementare il marketcap di $JCD, attirando investitori e community grazie a meccanismi di incentivazione e strategie di yield farming.
- **Tecnico:** Sviluppare una soluzione decentralizzata e modulare che sfrutti protocolli DeFi esistenti (Curve, StakeDAO) per garantire liquidità e rewards, e una interfaccia utente semplice per agevolare l’adozione.

## 3. Architettura di Sistema

### 3.1 Componenti principali
- **Pool su Curve:** 
  - Creazione e gestione di una pool per garantire liquidità e facilitare il trading tra $JCD e altri asset.
- **Strategia Factory su StakeDAO:** 
  - Implementazione di contratti intelligenti che compongono il meccanismo di autocompound per i rewards.
  - Integrazione con le librerie open source di StakeDAO per semplificare la gestione dei rewards.
- **App Base (Frontend):**
  - Interfaccia per lo swap ETH <> $JCD, con connessione a Metamask.
  - Modulo di “staking” che funzioni da wrapper, mostrando in maniera trasparente le operazioni reali eseguite dai contratti di StakeDAO.

### 3.2 Flusso Operativo
1. **Fase 1 – Creazione Pool e Strategia**
   - Deploy della pool su Curve.
   - Implementazione della strategia di autocompound su StakeDAO.
   - Configurazione degli incentivi per i LP (reward token, distribuzioni, ecc.).
2. **Fase 2 – Sviluppo App Base**
   - Integrazione del wallet (Metamask) e interfaccia utente per lo swap.
   - Implementazione del modulo di staking come interfaccia wrapper verso la strategia su StakeDAO.
   - Testing e validazione dell’MVP.

## 4. Specifiche Tecniche

### 4.1 Tecnologie e Librerie Consigliate
- **Smart Contract Development:**
  - Linguaggio: Solidity (versione 0.8.x o superiore)
  - Framework di sviluppo: Hardhat o Truffle
  - Librerie utili: OpenZeppelin per standard di sicurezza e best practice.
- **Integrazione DeFi:**
  - Curve: Documentazione ufficiale per la creazione di pool.
  - StakeDAO: Utilizzo delle loro API e librerie open source per strategie di autocompound.
- **Frontend e App Base:**
  - Framework: ReactJS o Next.js
  - Libreria Web3: Ethers.js o Web3.js per interazioni con la blockchain.
  - Integrazione Wallet: Metamask SDK.

### 4.2 Specifiche dei Contratti Smart

#### Pool su Curve
- **Funzionalità:**
  - Gestione della liquidità e swap tra asset.
  - Integrazione con sistemi di reward per LP.
- **Considerazioni di Sicurezza:**
  - Verifica dei contratti tramite audit esterni.
  - Implementazione di meccanismi di upgradeability (se necessario) tramite proxy patterns.

#### Strategia Factory su StakeDAO
- **Funzionalità:**
  - Autocompound dei rewards generati dalla pool.
  - Distribuzione periodica dei rewards agli utenti.
- **Considerazioni di Sicurezza:**
  - Utilizzo di librerie standard (OpenZeppelin) per evitare vulnerabilità.
  - Testing approfondito su testnet prima del deploy on-chain.

### 4.3 Bozzetti di Codice

#### Esempio: Contratto Base per il Pool su Curve (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CurvePoolJCD {
    IERC20 public jcdToken;
    IERC20 public otherAsset;
    
    mapping(address => uint256) public liquidityProvided;

    event LiquidityAdded(address indexed provider, uint256 jcdAmount, uint256 otherAssetAmount);
    event LiquidityRemoved(address indexed provider, uint256 jcdAmount, uint256 otherAssetAmount);

    constructor(IERC20 _jcdToken, IERC20 _otherAsset) {
        jcdToken = _jcdToken;
        otherAsset = _otherAsset;
    }

    function addLiquidity(uint256 jcdAmount, uint256 otherAssetAmount) external {
        // Logica per il trasferimento e l'aggiornamento della liquidità
        require(jcdToken.transferFrom(msg.sender, address(this), jcdAmount), "Transfer JCD failed");
        require(otherAsset.transferFrom(msg.sender, address(this), otherAssetAmount), "Transfer asset failed");
        liquidityProvided[msg.sender] += jcdAmount; // semplificato
        emit LiquidityAdded(msg.sender, jcdAmount, otherAssetAmount);
    }
    
    // Funzioni addizionali per lo swap e la rimozione della liquidità
}
```

---
