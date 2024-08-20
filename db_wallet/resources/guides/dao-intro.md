# DAO FROM AN EXISTING ERC-20

## Steps to obtain this response
1. Pass this prompt to get a generic response, that contains generally many options and paths available.

```text
Please write a complete guide on how to create a DAO from any ERC-20 coin.
```

The response in this case starts generically, with a guide that starts from the creation of the ERC20 in the case there's no token deployed. 

In this case, we notice that we can specialize the response and avoid the passage of token creation, because we got one already deployed. 


2. Modify the first message of this conversation and use a more specific prompt, for example using constraints

```text
Please write a complete guide on how to create a DAO from any ERC-20 coin.

Constraints are:
- it's an already created ERC-20 from 2018, safe with ownership renounced
```

This way, we force GPT-4o to focus on decentralization values. This model took the decision to deploy the DAO using an opensource library, avoiding any other external tool or DAO.
Seems reasonable because we explicitly focused on safety on the constraints.

Chances are that different ways of expressing constraints could've lead to slightly different results, for example is it not specified clearly if the "ownership renounced" is referred to the ERC-20 contract or the DAO contracts and mechanisms.
### Decentralized Autonomous Organizations are

DAO vote casting and politics differ from one to the other and the topic is really complex and with many choices. 

### Semantica and Linguistica Research on Prompting Could Lead To Improve Results  (Linguistica)
It's important to consider semantic considerations into prompting, because further research and proper ways of expressing tasks could lead to a major improvement in IA generation.

TODO : 

- test different conversations with different ways of expressing tasks and contraints
- document the best practices based on results

MORE COMPLEX TOOLS:
- develop some sort of RAG, where you can change more programatilly parameters like this, because this will allow to test generations more easily. 


Creating a Decentralized Autonomous Organization (DAO) using an existing ERC-20 token is an exciting way to empower a community to make decisions through on-chain voting. Since you are working with a pre-existing ERC-20 token, whose contract was created in 2018 and with renounced ownership (meaning no central party controls the contract), there are some specific considerations to keep in mind.

This guide will walk you through the entire process, from setting up the necessary tools to deploying the DAO and configuring its voting and treasury management mechanisms.

### Overview of the Process

1. **Understand Key Concepts**
   - What is a DAO?
   - Why Use an Existing ERC-20 Token?
   - Core Components of a DAO

2. **Pre-requisites**
   - Tools & Libraries Required
   - Setting Up Development Environment

3. **Creating a DAO Smart Contract**
   - Using OpenZeppelin Contracts
   - Governance Token Integration
   - Deploying the Governance Contract

4. **Setting Up the Governance Structure**
   - Proposals, Voting, and Quorum
   - Timelock Contract for Proposal Execution

5. **Deploying and Launching the DAO**
   - Configuring the DAO with Your ERC-20 Token
   - Setting Initial Parameters (e.g., quorum percentage)
   - Initializing the DAO and Inviting Members

6. **Managing the DAO**
   - Creating Proposals
   - Voting and Execution of Proposals
   - Managing Treasury

---

## 1. Understand Key Concepts

### What is a DAO?
A Decentralized Autonomous Organization (DAO) is an on-chain entity that allows token holders to make decisions through proposals and voting mechanisms. DAOs are often used for community-driven governance, treasury management, and decentralized project management.

### Why Use an Existing ERC-20 Token?
Since you are using an ERC-20 token from 2018 with renounced ownership:
   - **No Control Over Supply**: The total supply is fixed, which can create scarcity and thus make token distribution valuable.
   - **Security & Trust**: Renounced ownership implies that no one has control over the token contract itself, making it more trustable for the community.
   - **Governance**: The existing ERC-20 token can be used as a governance token, meaning the holders will vote on decisions.

### Core Components of a DAO
- **Governance Contract**: Handles voting and proposal creation.
- **Timelock Contract**: Delays the execution of approved proposals to give time for any last-minute objections.
- **Treasury**: The smart contract that holds and manages DAO funds.

---

## 2. Pre-requisites

### Tools & Libraries Required
- **Node.js & npm**: For managing dependencies.
- **Hardhat**: Ethereum development environment for compiling and deploying smart contracts.
- **OpenZeppelin Contracts**: A library of secure smart contract components.
- **Metamask**: Browser wallet for interacting with the Ethereum network.
- **Infura or Alchemy**: For deploying on Ethereum mainnet or testnets.

### Setting Up Development Environment
1. **Install Node.js & npm**:
   ```bash
   sudo apt install nodejs npm
   ```
2. **Create a Hardhat Project**:
   ```bash
   npx hardhat
   ```
   Choose "Create a basic sample project".

3. **Install OpenZeppelin Contracts**:
   ```bash
   npm install @openzeppelin/contracts
   ```

4. **Configure Hardhat for Deployment**:
   Set up `hardhat.config.js` to include the networks you plan to use (e.g., Ethereum Mainnet or testnets like Goerli).

---

## 3. Creating a DAO Smart Contract

### Using OpenZeppelin Contracts
We will leverage OpenZeppelin’s `Governor` contract, which is designed for creating a DAO.

1. **Install OpenZeppelin's Governance Package**:
   ```bash
   npm install @openzeppelin/contracts-upgradeable
   ```

2. **Create a New Governance Contract**:
   Create a new file, e.g., `MyDAO.sol`, in the `contracts` directory:
   ```solidity
   // SPDX-License-Identifier: MIT
   pragma solidity ^0.8.0;

   import "@openzeppelin/contracts/governance/Governor.sol";
   import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
   import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
   import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";
   import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
   import "@openzeppelin/contracts/governance/TimelockController.sol";

   contract MyDAO is Governor, GovernorVotes, GovernorVotesQuorumFraction, GovernorTimelockControl {
       constructor(
           ERC20Votes _token,
           TimelockController _timelock
       )
           Governor("MyDAO")
           GovernorVotes(_token)
           GovernorVotesQuorumFraction(4) // e.g., 4% quorum
           GovernorTimelockControl(_timelock)
       {}

       function votingDelay() public pure override returns (uint256) {
           return 1; // 1 block delay before voting starts
       }

       function votingPeriod() public pure override returns (uint256) {
           return 45818; // ~1 week voting period (1 block = 13.2 seconds)
       }

       function proposalThreshold() public pure override returns (uint256) {
           return 1000 * 10**18; // 1000 tokens required to submit a proposal
       }
   }
   ```

### Governance Token Integration
Since you already have an ERC-20 token, integrate it by importing the existing token contract’s address in the constructor.

### Deploying the Governance Contract
Compile the contracts:
```bash
npx hardhat compile
```
Deploy with a Hardhat script (e.g., `deploy.js`) that initializes the governor with the ERC-20 token and a timelock.

---

## 4. Setting Up the Governance Structure

### Proposals, Voting, and Quorum
- **Proposal Creation**: Define who can create proposals, often setting a minimum number of tokens required.
- **Quorum**: Set a percentage of total token supply required to pass a vote.
- **Timelock**: Use OpenZeppelin’s `TimelockController` for executing approved proposals after a delay.

Example `TimelockController`:
```solidity
contract MyTimelock is TimelockController {
    constructor(
        uint256 minDelay,
        address[] memory proposers,
        address[] memory executors
    )
        TimelockController(minDelay, proposers, executors)
    {}
}
```

### Deploying the Timelock
Deploy the timelock with a delay (e.g., 2 days) and set the governor contract as the only proposer.

---

## 5. Deploying and Launching the DAO

### Configuring the DAO with Your ERC-20 Token
Deploy the DAO contract and pass in the existing ERC-20 token’s address and the timelock’s address.

### Setting Initial Parameters
Decide on parameters like:
- **Quorum percentage** (e.g., 4%)
- **Proposal threshold** (e.g., 1000 tokens)

### Initializing the DAO and Inviting Members
- Announce the launch on your community channels.
- Explain how members can use their tokens to vote and submit proposals.

---

## 6. Managing the DAO

### Creating Proposals
Token holders can create proposals using the DAO’s smart contract functions. This typically involves specifying the action, target addresses, and calldata for execution.

### Voting and Execution of Proposals
- Members vote by calling the `castVote` or `castVoteWithReason` functions.
- Once a proposal passes and the timelock expires, the action is executed automatically.

### Managing Treasury
The DAO’s treasury can be managed by deploying a simple contract where only the DAO can move funds. Example:
```solidity
contract DAOTreasury {
    address public governor;

    constructor(address _governor) {
        governor = _governor;
    }

    function withdraw(address token, uint256 amount, address recipient) external {
        require(msg.sender == governor, "Only DAO can withdraw");
        IERC20(token).transfer(recipient, amount);
    }
}
```

---

### Conclusion

By following this guide, you can successfully create a DAO using an existing ERC-20 token. The DAO will enable your community to make decisions on-chain, ensuring transparency and collective control over the project's future. Be sure to test everything thoroughly on a testnet before deploying on the mainnet to avoid any unforeseen issues. Happy DAO building!