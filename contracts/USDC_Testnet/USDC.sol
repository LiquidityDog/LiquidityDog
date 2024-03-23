// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC20.sol";

contract USDC is ERC20 {
    constructor(uint256 initialSupply) ERC20("USDC Token", "USDC") {
        _mint(msg.sender, initialSupply);
    }
}

