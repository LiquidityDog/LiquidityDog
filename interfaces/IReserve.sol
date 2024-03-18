pragma solidity ^0.8.0;

interface IReserve {
    function sellShq(address _beneficiary, uint256 _shqAmount) external;
    function buyShq(address _beneficiary, uint256 _shqAmount) external;
    function buyShqWithUsdc(address _beneficiary, uint256 _usdcAmount) external;
}