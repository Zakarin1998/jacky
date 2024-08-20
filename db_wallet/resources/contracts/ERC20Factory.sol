// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/Clones.sol";
import "@openzeppelin/contracts/token/ERC20/presets/ERC20PresetMinterPauser.sol";

contract ERC20Factory {
    address public immutable implementation;
    address[] public allTokens;

    event TokenCreated(address indexed tokenAddress);

    constructor() {
        implementation = address(new ERC20PresetMinterPauser("Template", "TKN"));
    }

    function createToken(string memory name, string memory symbol) external returns (address) {
        address clone = Clones.clone(implementation);
        ERC20PresetMinterPauser(clone).initialize(name, symbol);
        allTokens.push(clone);
        emit TokenCreated(clone);
        return clone;
    }
}
