#!/usr/bin/env bash

# Script: rebalance_lp.sh
# Esegue il calcolo e aggiorna la LP V4 su base giornaliera

# 1) Esegui Python per ottenere tick
python3 compute_ticks.py > ticks.json

# ticks.json format:
# {"tickLower": 123456, "tickUpper": 234567}

# 2) Rimuovi vecchia LP (es. via Hardhat script)
npx hardhat run scripts/remove_lp.js --network mainnet

# 3) Aggiungi nuova LP con i tick calcolati
tickLower=$(jq .tickLower ticks.json)
tickUpper=$(jq .tickUpper ticks.json)

npx hardhat run scripts/mint_lp.js --network mainnet \
  --tickLower $tickLower --tickUpper $tickUpper \
  --amount0 1000000 --amount1 1

# 4) Aggiorna hook sigma via tx
echo "Updating sigma hook..."
npx hardhat run scripts/update_sigma.js --network mainnet \
  --sigmaBps $(jq .sigmaBasisPoints ticks.json)