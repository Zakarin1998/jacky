-- Complete SQL schema setup

-- Drop existing tables if they exist
DROP TABLE IF EXISTS deposit_addresses;
DROP TABLE IF EXISTS wallet_types;
DROP TABLE IF EXISTS chains;
DROP TABLE IF EXISTS providers;

-- Create table for exchanges (providers)
CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create table for blockchain networks (chains)
CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create table for wallet types (e.g., margin, funding, exchange)
CREATE TABLE wallet_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create table for deposit addresses
CREATE TABLE deposit_addresses (
    id SERIAL PRIMARY KEY,
    provider_id INT NOT NULL,
    chain_id INT NOT NULL,
    wallet_type_id INT NOT NULL,
    address TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (provider_id) REFERENCES providers(id) ON DELETE CASCADE,
    FOREIGN KEY (chain_id) REFERENCES chains(id) ON DELETE CASCADE,
    FOREIGN KEY (wallet_type_id) REFERENCES wallet_types(id) ON DELETE CASCADE
);

-- Indexes for faster lookups
CREATE INDEX idx_provider ON deposit_addresses(provider_id);
CREATE INDEX idx_chain ON deposit_addresses(chain_id);
CREATE INDEX idx_wallet_type ON deposit_addresses(wallet_type_id);
CREATE INDEX idx_address ON deposit_addresses(address);
