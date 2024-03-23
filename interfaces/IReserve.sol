pragma solidity ^0.8.0;

interface IReserve {
    function sellLQDog(address _beneficiary, uint256 _LQDogAmount) external;
    function buyLQDog(address _beneficiary, uint256 _LQDogAmount) external;
    function buyLQDogWithUsdc(address _beneficiary, uint256 _usdcAmount) external;
}