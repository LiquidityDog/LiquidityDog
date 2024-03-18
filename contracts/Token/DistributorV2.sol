// SPDX-License-Identifier: MIT
// Rewards Distributor
pragma solidity ^0.8.0;

import "../../interfaces/ISheqelToken.sol"; 
import "./IERC20.sol";
import "../../interfaces/IReserve.sol";

contract Distributor {
    event Log(string message, uint data);

    uint256 public lastDistribution;
    uint256 public currentShqToUBR;
    uint256 public currentShqToRewards;
    uint256 public currentUSDCToUBR;
    uint256 public currentUSDCToRewards;
    bool public shqSet = false;
    ISheqelToken public sheqelToken;
    IERC20 public USDC;
    address public teamAddress;
    IReserve public reserveContract;

    constructor(address _usdcAddress, address _reserveAddress) {
        teamAddress = msg.sender;
        USDC = IERC20(_usdcAddress);
        reserveContract = IReserve(_reserveAddress);
    }

    modifier onlyTeam() {
        require(msg.sender == teamAddress, "Caller must be team address");
        _;
    }

    modifier onlyToken() {
        require(msg.sender == address(sheqelToken), "Caller must be Sheqel Token");
        _;
    }

    modifier onlyReserve() {
        require(msg.sender == address(reserveContract), "Caller must be Reserve");
        _;
    }

    function setShq(address _addr) external onlyTeam() {
        require(shqSet == false, "SHQ Already set");
        sheqelToken = ISheqelToken(_addr);
        shqSet = true;
    }

    function addToCurrentShqToUBR(uint256 _amount) external onlyToken() {
        currentShqToUBR += _amount;
    }

    function addToCurrentShqToRewards(uint256 _amount) external onlyToken() {
        currentShqToRewards += _amount;
    }

    function addToCurrentUsdcToRewards(uint256 _amount) external onlyReserve() {
        currentUSDCToRewards += _amount;
    }

    function addToCurrentUsdcToUBR(uint256 _amount) external onlyReserve() {
        currentUSDCToUBR += _amount;
    }



    function processAllRewards(address[] calldata _addresses , uint256[] calldata _balances, address[] calldata _ubrAddresses, uint256 _totalBalance) onlyTeam() external{
        //TODO: delete the first require
        //require(block.timestamp >= lastDistribution + 1 days, "Cannot distribute two times in a day");
        require(_addresses.length == _balances.length, "Addresses and balances must be the same length");

        // Convert all SHQ to USDC
        if(currentShqToRewards > 0){
            currentUSDCToRewards += swapSHQToUSDC(currentShqToRewards);
            currentShqToRewards = 0;
        }
        if(currentShqToUBR > 0){
            currentUSDCToUBR += swapSHQToUSDC(currentShqToUBR);
            currentShqToUBR = 0;
        }   

        require(currentUSDCToRewards > 0, "No USDC to distribute prec");
        require(currentUSDCToUBR > 0, "No USDC to distribute UBR");

        // Iterate through all balances and add it to checkTotalBalance
        uint256 checkTotalBalance = 0;
        for (uint256 i = 0; i < _balances.length; i++) {
            checkTotalBalance += _balances[i];
        }

        // Check if the total balance is the same as the total balance !
        require(checkTotalBalance == _totalBalance, "Total balance does not match");

        // Iterate through all addresses
        for (uint256 i = 0; i < _addresses.length; i++) {
            // Get the address
            address holder = _addresses[i];
            // Get the balance
            uint256 balance = _balances[i];

            // Calculate the rewards
            uint256 percentageReward = (balance * (currentUSDCToRewards-100)) / _totalBalance;
            // Send the rewards
            USDC.transfer(holder, percentageReward);
        }
        currentUSDCToRewards = 0;

        currentUSDCToUBR = USDC.balanceOf(address(this));

        // Compute the UBR
        uint256 ubrReward = (currentUSDCToUBR / _ubrAddresses.length) - 100;
        // Iterate through all UBR addresses
        for (uint256 i = 0; i < _ubrAddresses.length; i++) {
            // Get the address
            address holder = _ubrAddresses[i];

            // Send the UBR
            USDC.transfer(holder, ubrReward);
        }
        currentUSDCToUBR = 0;

        // Update last distribution
        lastDistribution = block.timestamp;

        // Send rest to the reserve 
        USDC.transfer(address(reserveContract), USDC.balanceOf(address(this)));
        sheqelToken.transfer(address(reserveContract), sheqelToken.balanceOf(address(this)));
    }

    function swapSHQToUSDC(uint256 amount) internal returns(uint256){
        uint256 balancePreswapUSDC = USDC.balanceOf(address(this));
        sheqelToken.approve(address(reserveContract), amount);
        reserveContract.sellShq(address(this), amount);

        return USDC.balanceOf(address(this)) - balancePreswapUSDC;
    }
}