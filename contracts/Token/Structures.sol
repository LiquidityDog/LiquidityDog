// SPDX-License-Identifier: MIT
// Queue contract, will queue Shareholder's share

pragma solidity ^0.8.0;

interface Structures {
    struct Share {
        address holder;
        int256 amount;
        uint256 rewardDate;
    }
}
