# Curve Swap App

## Project Overview

This project is a React-based Single Page Application (SPA) with the following core features:

1. **Navbar** – Top-level navigation component.
2. **Home** – Main landing page.
3. **Hero** – Section on the Home page containing the Swap UI.
4. **Swap Component** – Allows selecting two ERC‑20 tokens and swapping them via Web3 & Curve SDK.

Focusing on an MVP:

* **Clean architecture**: clear separation of concerns and component responsibilities.
* **Performance-minded**: minimal re-renders, lazy-loading, and code splitting.
* **Scalable**: easily extendable for future gas optimizations and advanced features.

---

## Tech Stack & Dependencies

* **Framework**: Next.js (React) with TypeScript
* **Styling**: Tailwind CSS (configured in `src/styles/globals.css`)
* **Web3 Layer**: ethers.js
* **Curve Integration**: @curvefi/sdk
* **Yearn Integration**: @yearn-finance/sdk
* **State Management**: React Context API (or Zustand in future)

### Linting & Formatting

We’ve opted in to **ESLint** plus **Prettier** to maintain code quality and consistency. The baseline setup uses the built‑in ESLint integration in Next.js, extended with plugins:

```bash
npm install -D eslint prettier eslint-plugin-react eslint-plugin-jsx-a11y eslint-plugin-import eslint-config-prettier eslint-plugin-prettier
```

Include a root `.eslintrc.js` at the project root:

```js
module.exports = {
  root: true,
  extends: [
    'next/core-web-vitals',
    'plugin:react/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:prettier/recommended'
  ],
  rules: {
    // custom rule overrides here
  }
};
```

### Testing

* **Unit & Integration**: React Testing Library + Jest
* **Unit & Integration**: React Testing Library + Jest
  :

```json
{
  "name": "curve-swap-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "ethers": "^6.0.0",
    "@curvefi/sdk": "^1.0.0",
    "tailwindcss": "^3.0.0"
  },
  "devDependencies": {
    "vite": "^4.0.0",
    "typescript": "^4.9.0",
    "eslint": "^8.0.0",
    "prettier": "^2.0.0"
  }
}
```

---

## Project Structure

```
curve-swap-app/
├── public/
│   └── favicon.ico, images...
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── Swap.tsx
│   │   └── TokenSelector.tsx
│   ├── context/
│   │   └── Web3Context.tsx
│   ├── hooks/
│   │   └── useCurveSwap.ts
│   ├── pages/
│   │   ├── index.tsx    # Home
│   │   └── _app.tsx     # wraps Web3Provider and globals
│   ├── styles/
│   │   └── globals.css  # Tailwind entrypoints
│   ├── utils/          # helper functions (optional)
│   └── types/          # shared TS types (optional)
├── .eslintrc.js
├── tailwind.config.js
├── next.config.js
├── package.json
└── tsconfig.json
```

```
curve-swap-app/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── Swap.tsx
│   │   └── TokenSelector.tsx
│   ├── pages/
│   │   └── Home.tsx
│   ├── context/
│   │   └── Web3Context.tsx
│   ├── hooks/
│   │   └── useCurveSwap.ts
│   ├── styles/
│   │   └── index.css
│   ├── App.tsx
│   └── main.tsx
├── .eslintrc.js
├── tailwind.config.js
└── vite.config.ts

```

---

## Key Components

### 1. `Web3Context`
Provides a Web3 Provider (ethers.js) across the app.
```tsx
import { createContext, useContext, useEffect, useState } from 'react';
import { ethers } from 'ethers';

interface Web3ContextProps {
  provider?: ethers.providers.Web3Provider;
  signer?: ethers.Signer;
}

const Web3Context = createContext<Web3ContextProps>({});

export const Web3Provider: React.FC = ({ children }) => {
  const [provider, setProvider] = useState<ethers.providers.Web3Provider>();
  const [signer, setSigner] = useState<ethers.Signer>();

  useEffect(() => {
    if (window.ethereum) {
      const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
      setProvider(web3Provider);
      web3Provider.getSigner().then(setSigner);
    }
  }, []);

  return (
    <Web3Context.Provider value={{ provider, signer }}>
      {children}
    </Web3Context.Provider>
  );
};

export const useWeb3 = () => useContext(Web3Context);
```

### 2. `Swap` Hook & Component

#### `useCurveSwap.ts` (Hook)

```ts
import { useWeb3 } from '../context/Web3Context';
import { Curve } from '@curvefi/sdk';
import { useCallback } from 'react';

export const useCurveSwap = () => {
  const { signer } = useWeb3();
  const sdk = new Curve({ signer }); // MVP: default pool

  const swap = useCallback(async (tokenIn, tokenOut, amount) => {
    if (!signer) throw new Error('Wallet not connected');
    // Simplified: fetch quote & perform swap
    const quote = await sdk.getQuote({ tokenIn, tokenOut, amount });
    const tx = await sdk.swap({ ...quote });
    return tx.wait();
  }, [signer]);

  return { swap };
};
```

#### `Swap.tsx`

```tsx
import { useState } from 'react';
import { useCurveSwap } from '../hooks/useCurveSwap';
import TokenSelector from './TokenSelector';

const Swap: React.FC = () => {
  const [tokenIn, setTokenIn] = useState('');
  const [tokenOut, setTokenOut] = useState('');
  const [amount, setAmount] = useState('');
  const { swap } = useCurveSwap();

  const handleSwap = async () => {
    await swap(tokenIn, tokenOut, amount);
    // TODO: success/error handling & gas optimizations
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <TokenSelector value={tokenIn} onChange={setTokenIn} />
      <TokenSelector value={tokenOut} onChange={setTokenOut} />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        className="border p-2 my-2 w-full"
      />
      <button onClick={handleSwap} className="btn-primary w-full">
        Swap
      </button>
    </div>
  );
};

export default Swap;
```

### 3. Other UI Components

#### `Navbar.tsx`

```tsx
const Navbar: React.FC = () => (
  <nav className="w-full p-4 bg-gray-800 text-white">
    <div className="container mx-auto flex justify-between">
      <span className="font-bold">CurveSwap</span>
      <div className="space-x-4">
        <a href="#home">Home</a>
        <a href="#swap">Swap</a>
      </div>
    </div>
  </nav>
);

export default Navbar;
```

#### `Hero.tsx`

```tsx
import Swap from './Swap';

const Hero: React.FC = () => (
  <section id="swap" className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-400 to-purple-600">
    <div className="container mx-auto p-6 text-center">
      <h1 className="text-4xl font-bold text-white mb-4">Swap Tokens Effortlessly</h1>
      <Swap />
    </div>
  </section>
);

export default Hero;
```

#### `Home.tsx`

```tsx
import Hero from '../components/Hero';

const Home: React.FC = () => (
  <main>
    <Hero />
    {/* future sections... */}
  </main>
);

export default Home;
```

### 4. Entry Point

#### `App.tsx`

```tsx
import Navbar from './components/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <>
      <Navbar />
      <Home />
    </>
  );
}

export default App;
```

#### `main.tsx`

```ts
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { Web3Provider } from './context/Web3Context';
import './styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Web3Provider>
    <App />
  </Web3Provider>
);
```

---

## CLI & Setup Guide

Below are the essential npm (or yarn) commands to bootstrap and work with this project:

```bash
# 1. Create a Next.js TypeScript project
npx create-next-app@latest curve-swap-app --typescript

# 2. Navigate into project directory
cd curve-swap-app

# 3. Install core dependencies
npm install react react-dom ethers @curvefi/sdk @yearn-finance/sdk tailwindcss

# 4. Install dev dependencies
npm install -D eslint prettier jest @testing-library/react @testing-library/jest-dom vite typescript

# 5. Initialize Tailwind CSS
npx tailwindcss init -p

# 6. Start development server
npm run dev

# 7. Build for production
npm run build

# 8. Lint and format code
npm run lint
npm run format

# 9. Run tests
npm test
```

You can substitute `npm` with `yarn` or `pnpm` as needed for your workflow.

## Next Steps & Optimizations

* **Gas Optimizations**: Batch calls, use multicall, prefetch quotes off-chain.
* **Advanced State Management**: Integrate Zustand or Redux for global swap state.
* **Pool Selection**: Dynamically fetch & display available Curve pools.
* **Error Handling & UX**: Toast notifications, loading spinners, form validation.
* **Security**: Audit input values, integrate Etherscan links for transactions.
* **Testing**: Unit tests for hooks & components, integration tests for swap flows.

This setup provides a solid MVP focusing on clean code, modular components, and easy extensibility for advanced features later.
