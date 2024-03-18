pragma solidity ^0.8.0;

import "../Token/IERC20.sol";
import "../../interfaces/ISheqelToken.sol";
import "../../interfaces/Uniswap.sol";
import "../Token/DistributorV2.sol";

contract Reserve {
    ISheqelToken private sheqelToken;
    IERC20 private USDC;
    uint256 private shqToConvert;
    uint256 taxRate = 5;
    IUniswapV2Router02 private uniswapV2Router;
    address private WFTM = 0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83;
    address private teamAddress;
    bool shqAddressSet=false;


    Distributor public distributor;

    event ShqBought(uint256 amountSHQ, uint256 amountUSDC);
    event ShqSold(uint256 amountSHQ, uint256 amountUSDC);



    constructor(address _spookyswapRouter, address _usdcAddress) {
        // Contract constructed by the Sheqel token
        USDC = IERC20(_usdcAddress);
        uniswapV2Router = IUniswapV2Router02(_spookyswapRouter);
        teamAddress = msg.sender;
        shqToConvert = 0;
    }

    modifier onlyToken() {
        require(msg.sender == address(sheqelToken), "Must be Sheqel Token");
        _;
    }

    modifier onlyTeam() {
        require(msg.sender == address(teamAddress), "Must be Sheqel Team");
        _;
    }

    function setTaxRate(uint256 _taxRate) external onlyTeam() {
        taxRate = _taxRate;
    }
    function setSheqelTokenAddress(address _addr) public onlyTeam() {
        require(shqAddressSet == false, "Can only change the address once");
        sheqelToken = ISheqelToken(_addr);
        address distributorAddress = sheqelToken.getDistributor();
        distributor = Distributor(distributorAddress);
        shqAddressSet=true;

        // Initial buying in of 999USDC


        // Burning
        sheqelToken.transfer(0x1234567890123456789012345678901234567890, 2*10**18);

        // Adding liquidity
        sheqelToken.transfer(teamAddress, 2000 * 10 ** 18);

        // Initial tokens
        sheqelToken.transfer(teamAddress, 197998 * 10 ** 18);
        
    }

    function addToShqToConvert(uint256 amount) public onlyToken() {
        shqToConvert += amount;
    }

    function buyPrice() public view returns (uint256) {
        uint256 usdcInReserve = USDC.balanceOf(address(this)) * (10 ** 6);
        uint256 shqOutsideReserve = (sheqelToken.totalSupply() - sheqelToken.balanceOf(address(this))) / (10 ** 12);

        return (usdcInReserve / shqOutsideReserve); // Price in USDC (6 decimals)
    }

    function buyPriceWithTax() public view returns (uint256) {
        uint256 usdcInReserve = USDC.balanceOf(address(this)) * (10 ** 6);
        uint256 shqOutsideReserve = (sheqelToken.totalSupply() - sheqelToken.balanceOf(address(this))) / (10 ** 12);

        return (usdcInReserve / shqOutsideReserve) + ((usdcInReserve / shqOutsideReserve) * taxRate) / 100; // Price in USDC (6 decimals)
    }

    function sellPrice() public view returns (uint256) {
        uint256 totalShq = sheqelToken.totalSupply();
        uint256 shqInReserve = sheqelToken.balanceOf(address(this));
        uint256 usdcInReserve = USDC.balanceOf(address(this));
        uint256 shqDecimals = 10**18;
        uint256 coefficient = 97;

        return ((totalShq * buyPriceWithTax()) - (usdcInReserve*shqDecimals*coefficient)/100) / (shqInReserve - 1); // Price in USDC (6 decimals)
    }


    function buyShq(address _beneficiary, uint256 _shqAmount) external {
        require(_shqAmount > 0, "Amount of tokens purchased must be positive");
        _processPurchase(_beneficiary, _shqAmount);
    }

    function buyShqWithUsdc(address _beneficiary, uint256 _usdcAmount) public {
        require(_usdcAmount > 0, "Amount of tokens purchased must be positive");
        uint256 shqAmount = (_usdcAmount * (10 ** 18)) / sellPrice();
        _processPurchase(_beneficiary, shqAmount);
    }

    function sellShq(address _beneficiary, uint256 _shqAmount) external {
        require(_shqAmount > 0, "Amount of tokens sold must be positive");
        _processSell(_beneficiary, _shqAmount);
    }

    function _processSell(address _beneficiary, uint256 _shqAmount) internal {
        // Converting shq to usdc
        uint256 usdcAmount = (_shqAmount * buyPrice()) / (10 ** 18);
    
        // Making the user pay
        require(sheqelToken.transferFrom(msg.sender, address(this), _shqAmount), "Deposit failed");

        // Delivering the tokens
        uint256 usdcAmountTaxed = _takeTax(usdcAmount);
        _deliverUsdc(_beneficiary, usdcAmountTaxed);

        emit ShqSold(usdcAmount, _shqAmount);

  }

    function _processPurchase(address _beneficiary, uint256 _shqAmount) internal {
        require(sheqelToken.balanceOf(address(this)) - _shqAmount >= 2 * 10**18, "Cannot buy remaining SHQ");
        // Converting shq to usdc
        uint256 usdcAmount = (_shqAmount * sellPrice()) / (10 ** 18);
    
        // Making the user pay
        require(USDC.transferFrom(msg.sender, address(this), usdcAmount), "Deposit failed");

        // Paying the tax
        _takeTax(usdcAmount);

        // Delivering the tokens
        _deliverShq(_beneficiary, _shqAmount);


        emit ShqBought(_shqAmount, usdcAmount);
    }

    function _deliverShq(address _beneficiary, uint256 _shqAmount) internal {
        sheqelToken.transfer(_beneficiary, _shqAmount);
    }

    function _deliverUsdc(address _beneficiary, uint256 _usdcAmount) internal {
        USDC.transfer(_beneficiary, _usdcAmount);
    }

  /** @dev Creates `amount` tokens and takes all the necessary taxes for the account.*/
     
    function _takeTax(uint256 amount)
        internal
        returns (uint256 amountRecieved)
    {
        // Calculating the tax
        uint256 reserve = (amount * 88797) / 10000000;
        uint256 rewards = (amount * 255547) / 10000000;
        uint256 MDO = (amount * 44373) / 10000000;
        uint256 UBR = (amount * 88797) / 10000000;
        uint256 liquidity = (amount * 22187) / 10000000;


        // Adding the liquidity to the contract
        _addToLiquidity(liquidity); 

        // Sending the tokens to the reserve
        _sendToReserve(reserve);

        // Sending the MDO wallet
        _sendToMDO(MDO);

        // Adding to the Universal Basic Reward pool
        _addToUBR(UBR);

        // Adding to the rewards pool
        _addToRewards(rewards);

        return (amount - (reserve + rewards + MDO + UBR + liquidity));
    }

    function _addToLiquidity(uint256 _amount) private {
        USDC.transfer(sheqelToken.liquidityManagerAddress(), _amount);
    }

    function _sendToReserve(uint256 amount) private {
        USDC.transfer(address(this), amount);
    }

    function _addToRewards(uint256 amount) private {
        USDC.transfer(address(distributor), amount);

        distributor.addToCurrentUsdcToRewards(amount);
    }

    function _addToUBR(uint256 amount) private {
        USDC.transfer(address(distributor), amount);

        distributor.addToCurrentUsdcToUBR(amount);
    }

    function _sendToMDO(uint256 amount) private {
        address MDOAddress = sheqelToken.MDOAddress();
        USDC.transfer(MDOAddress, amount);
    }

}