// SPDX-License-Identifier: MIT
// Queue contract, will queue Shareholder's share

pragma solidity ^0.8.0;

import "./Structures.sol";

contract Queue is Structures {

    mapping(uint256 => Share) queue;
    uint256 first = 1;
    uint256 last = 0;

    address distributor;

    constructor() {
        distributor = msg.sender;
    }

    modifier onlyDistributor(){
        require(msg.sender == distributor, "Caller must be Distributor");
        _;
    }

    function enqueue(Share memory data) external onlyDistributor {
        last += 1;
        queue[last] = data;
    }

    function dequeue() external onlyDistributor returns (Share memory data) {
        require(last >= first);  // non-empty queue

        data  = queue[first];

        delete queue[first];
        first += 1;
    }

    function getFirst() external view onlyDistributor returns (Share memory data) {
        require(last >= first);  // non-empty queue

        data  = queue[first];
    }

    function isEmpty() external view onlyDistributor returns (bool) {
        return ! (last >= first);
    }
}