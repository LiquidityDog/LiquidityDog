pragma solidity ^0.8.0;

import "../Token/IERC20.sol";
import "../../interfaces/Uniswap.sol";

contract Convertor {
    IUniswapV2Router02 public uniswapV2Router = IUniswapV2Router02(0xF491e7B69E4244ad4002BC14e878a34207E38c29);
    IERC20 public sheqelToken;
    IERC20 public USDC = IERC20(0x4188663a85C92EEa35b5AD3AA5cA7CeB237C6fe9);

    constructor(address _sheqelTokenAddress) {
        sheqelToken = IERC20(_sheqelTokenAddress);
    }


    function swapSheqelToUSDC() internal {
        address[] memory path = new address[](2);
        path[0] = address(this);
        path[1] = uniswapV2Router.WETH();


    }


}