// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../Token/IERC20.sol";
import "../../interfaces/Uniswap.sol";


contract Reserve {
    IERC20 private LiquidityDog;
    IERC20 private USDC;
    address private teamAddress;
    bool LQDogAddressSet=false;

    event LQDogBought(uint256 amountLQDog, uint256 amountUSDC);
    event LQDogSold(uint256 amountLQDog, uint256 amountUSDC);



    constructor(address _usdcAddress) {
        // Contract constructed by the LiquidityDog
        USDC = IERC20(_usdcAddress);
        teamAddress = msg.sender;
    }

    modifier onlyToken() {
        require(msg.sender == address(LiquidityDog), "Must be LiquidityDog");
        _;
    }

    modifier onlyTeam() {
        require(msg.sender == address(teamAddress), "Must be LiquidityDog Team");
        _;
    }


    function setLiquidityDogAddress(address _addr) public onlyTeam() {
        require(LQDogAddressSet == false, "Can only change the address once");
        LiquidityDog = IERC20(_addr);
        LQDogAddressSet=true;

        // Initial buying in of 0.000002USDC


        // Burning 2
        LiquidityDog.transfer(0x1234567890123456789012345678901234567890, 2*10**18);
        
    }


    function buyPrice() public view returns (uint256) {
        uint256 usdcInReserve = USDC.balanceOf(address(this)) * (10 ** 6);
        uint256 LQDogOutsideReserve = (LiquidityDog.totalSupply() - LiquidityDog.balanceOf(address(this))) / (10 ** 12);

        return ((usdcInReserve*99/100/ LQDogOutsideReserve); // Price in USDC (6 decimals)
    }
    
    function buyPriceVariableForSellPrice() public view returns (uint256) {
        uint256 usdcInReserve = USDC.balanceOf(address(this)) * (10 ** 6);
        uint256 LQDogOutsideReserve = (LiquidityDog.totalSupply() - LiquidityDog.balanceOf(address(this))) / (10 ** 12);

        return (usdcInReserve / LQDogOutsideReserve); // Price in USDC (6 decimals)
    }

    function sellPrice() public view returns (uint256) {
        uint256 totalLQDog = LiquidityDog.totalSupply();
        uint256 LQDogInReserve = LiquidityDog.balanceOf(address(this));
        uint256 LQDogOutsideReserve = (totalLQDog - LiquidityDog.balanceOf(address(this))) / (10 ** 12)
        uint256 usdcInReserve = USDC.balanceOf(address(this));
        uint256 LQDogDecimals = 10**18;

        return (totalLQDog * buyPriceVariableForSellPrice()  + ( usdcInReserve * LQDogDecimals )/100 ) / (LQDogInReserve - 1); // Price in USDC (6 decimals)
    }


    function buyLQDog(address _beneficiary, uint256 _LQDogAmount) external {
        require(_LQDogAmount > 0, "Amount of tokens purchased must be positive");
        _processPurchase(_beneficiary, _LQDogAmount);
    }

    function buyLQDogWithUsdc(address _beneficiary, uint256 _usdcAmount) public {
        require(_usdcAmount > 0, "Amount of tokens purchased must be positive");
        uint256 LQDogAmount = (_usdcAmount * (10 ** 18)) / sellPrice();
        _processPurchase(_beneficiary, LQDogAmount);
    }

    function sellLQDog(address _beneficiary, uint256 _LQDogAmount) external {
        require(_LQDogAmount > 0, "Amount of tokens sold must be positive");
        _processSell(_beneficiary, _LQDogAmount);
    }

    function _processSell(address _beneficiary, uint256 _LQDogAmount) internal {
        // Converting LQDog to usdc
        uint256 usdcAmount = (_LQDogAmount * buyPrice()) / (10 ** 18);
    
        // Making the user pay
        require(LiquidityDog.transferFrom(msg.sender, address(this), _LQDogAmount), "Deposit failed");

        _deliverUsdc(_beneficiary, usdcAmount);

        emit LQDogSold(usdcAmount, _LQDogAmount);

  }

    function _processPurchase(address _beneficiary, uint256 _LQDogAmount) internal {
        require(LiquidityDog.balanceOf(address(this)) - _LQDogAmount >= 2 * 10**18, "Cannot buy remaining LQDog");
        // Converting LQDog to usdc
        uint256 usdcAmount = (_LQDogAmount * sellPrice()) / (10 ** 18);
    
        // Making the user pay
        require(USDC.transferFrom(msg.sender, address(this), usdcAmount), "Deposit failed");

        // Delivering the tokens
        _deliverLQDog(_beneficiary, _LQDogAmount);


        emit LQDogBought(_LQDogAmount, usdcAmount);
    }

    function _deliverLQDog(address _beneficiary, uint256 _LQDogAmount) internal {
        LiquidityDog.transfer(_beneficiary, _LQDogAmount);
    }

    function _deliverUsdc(address _beneficiary, uint256 _usdcAmount) internal {
        USDC.transfer(_beneficiary, _usdcAmount);
    }
}