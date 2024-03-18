// SPDX-License-Identifier: MIT
// Liquidity Manager
pragma solidity ^0.8.0;

import "./IERC20.sol";
import "../../interfaces/Uniswap.sol";
import "../../interfaces/IReserve.sol";

contract LiquidityManager {
    IERC20 public sheqelToken;
    IERC20 public USDC;
    IUniswapV2Router02 public uniswapV2Router;
    IReserve public reserve;

    constructor(address _usdcAddress, address _spookySwapAddress, address _reserveAddress) {
        sheqelToken = IERC20(msg.sender);
        USDC = IERC20(_usdcAddress);
        uniswapV2Router = IUniswapV2Router02(_spookySwapAddress);
        reserve = IReserve(_reserveAddress);
    }

    modifier onlyToken() {
        require(msg.sender == address(sheqelToken), "Must be Sheqel Token");
        _;
    }

    /*function addToCurrentShqToLiquidity(uint256 _amount) onlyToken() public {
        currentShqToLiquidity += _amount;
    }*/

    function swapAndLiquify() onlyToken() public {
        // Converting all USDC to SHQ
        uint256 currentUSDCBalance = USDC.balanceOf(address(this));
        if(currentUSDCBalance > 0) {
            USDC.approve(address(reserve), currentUSDCBalance);
            reserve.buyShqWithUsdc(address(this), currentUSDCBalance);
        }
        uint256 currentShqToLiquidity = sheqelToken.balanceOf(address(this));
        require(currentShqToLiquidity > 0, "No SHQ to sell");
        // split the contract balance into halves
        uint256 half = currentShqToLiquidity / 2;
        uint256 otherHalf = currentShqToLiquidity - half;

        uint256 initialUSDCBalance = USDC.balanceOf(address(this));

        // swap tokens for USDC
        sheqelToken.approve(address(reserve), otherHalf);
        reserve.sellShq(address(this), otherHalf); 


        uint256 newBalance = USDC.balanceOf(address(this)) - (initialUSDCBalance);

        // add liquidity to uniswap
        addLiquidity(half, newBalance);
    }

    function addLiquidity(uint256 _shqAmount, uint256 _usdcAmount) private {
        // approve token transfer to cover all possible scenarios
        USDC.approve(address(uniswapV2Router), _usdcAmount);
        sheqelToken.approve(address(uniswapV2Router), _shqAmount);
        // add the liquidity
        uniswapV2Router.addLiquidity(
            address(sheqelToken),
            address(USDC),
            _shqAmount,
            _usdcAmount,
            0, 
            0, 
            address(this),
            block.timestamp + 15
        );
    }
}