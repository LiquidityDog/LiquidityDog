pragma solidity ^0.8.0;

interface ISheqelToken {
    function getDistributor() external returns (address);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function MDOAddress() external returns (address);
    function liquidityManagerAddress() external returns (address);
    function reserveAddress() external view returns (address);



}