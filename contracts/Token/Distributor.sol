// SPDX-License-Identifier: MIT
// Rewards Distributor
pragma solidity ^0.8.0;

import "./IERC20.sol";
import "../../interfaces/Uniswap.sol";
import "./Queue.sol";
import "./Structures.sol";
import "../../interfaces/IReserve.sol";

contract HolderRewarderDistributor is Structures {
    //Atributes // TODO change visibility
    IERC20 private sheqelToken;
    IERC20 private USDC;
    address public WFTM;
    address public reserve;
    IReserve public reserveContract;

    uint256 public lastDistribution;

    uint256 public currentShqToRewards;
    uint256 public currentUSDCToRewards;
    uint256 public currentShqToUBR;
    uint256 public currentUSDCToUBR;
    bool public shqSet = false;

    IUniswapV2Router02 private uniswapV2Router;

    //Holders
    address[] public holders;
    uint256 nbOfHolders = 0;
    mapping(address => int256) holdersToRewardsBalance;
    mapping(address => bool) public isHolder;

    // UBR
    uint256 UBRthreshold = 10; // TODO: calculate the best threshold
    uint256 nbOfEligibleHoldersToUBR = 0;
    mapping(address => bool) public isEligibleToUBR;

    //Shares
    Queue private pendingTransactions;

    // Events
    event DistributedRewards(uint256 totalDistributedUSDC);



    //Constructor

    constructor(address _router, address _reserve, address _deployer, int _amount, address _usdcAddress) {
        uniswapV2Router = IUniswapV2Router02(_router);
        //sheqelToken = IERC20(msg.sender);
        pendingTransactions = new Queue();
        reserve = _reserve;
        reserveContract = IReserve(_reserve);
        USDC = IERC20(_usdcAddress);

        //setup init mint
        //holders.push(_deployer);
        isHolder[_deployer] = true;
        nbOfHolders++;        
        isEligibleToUBR[_deployer] = true;
        nbOfEligibleHoldersToUBR++;        
        holdersToRewardsBalance[_deployer] = _amount;

    }

    function setShq(address _addr) external {
        require(shqSet == false, "SHQ Already set");
        sheqelToken = IERC20(_addr);
        shqSet = true;
    }

    //Modifiers

    modifier onlyToken() {
        require(msg.sender == address(sheqelToken), "Must be Sheqel Token");
        _;
    }

    modifier onlyReserve() {
        require(msg.sender == reserve, "Must be Reserve");
        _;
    }

    modifier onlyNotNullAmount(int256 amount) {
        require(amount != 0, "Must transfer non null amount");
        _;
    }

    modifier onlyNotNullHolder(address holder) {
        require(
            holder > address(0),
            "Holder must have a non null positive address"
        );
        _;
    }

    modifier onlyHolder(address holder) {
        require(isHolder[holder] == true);
        _;
    }

    //Functions

    //Distributor
    function addToCurrentShqToUBR(uint256 amount) external onlyToken {
        currentShqToUBR += amount;
    }

    function addToCurrentShqToRewards(uint256 amount)
        external
        onlyToken
    {
        currentShqToRewards += amount;
    }

    function addToCurrentUsdcToRewards(uint256 amount) external onlyReserve {
        currentUSDCToRewards += amount;
    }

    function addToCurrentUsdcToUBR(uint256 amount) external onlyReserve {
        currentUSDCToUBR += amount;
    }


    //Holder management

    function addHolder(address holder) private onlyNotNullHolder(holder) {
        require(isHolder[holder] == false);
        holders.push(holder);
        isHolder[holder] = true;
        nbOfHolders++;
    }

    /**
     Removes holder, sets attribute to false and decrements number of holder to false 
     */
    function removeHolder(address holder) private onlyNotNullHolder(holder) {
        require(isHolder[holder] == true);
        isHolder[holder] = false;
        nbOfHolders--;
        removeFromEligibleUBR(holder);
    }

    // UBR Managment
    /**
     Sets the holder eligible to UBR reward and increments the number of eligible hodlers 
     */
    function addToEligibleUBR(address holder)
        private
        onlyNotNullHolder(holder)
    {
        require(isEligibleToUBR[holder] == false);
        require(holdersToRewardsBalance[holder] >= int (UBRthreshold));
        isEligibleToUBR[holder] = true;
        nbOfEligibleHoldersToUBR++;
    }

    /**
     Sets the holder not eligible to UBR reward and decrements the number of eligible hodlers 
     */
    function removeFromEligibleUBR(address holder)
        private
        onlyNotNullHolder(holder)
    {
        require(isEligibleToUBR[holder] == true);
        require(holdersToRewardsBalance[holder] < int (UBRthreshold));
        isEligibleToUBR[holder] = false;
        nbOfEligibleHoldersToUBR--;
    }

    //Share management
    function transferShare(address holder, int256 amount)
        public
        onlyToken
        onlyNotNullAmount(amount)
        onlyNotNullHolder(holder)
    {
        uint256 rewardDate = block.timestamp + 1 days;
        pendingTransactions.enqueue(Share(holder, amount, rewardDate));
    }

    /*
    Process the pendingTransactions queue,
    updates holder rewards balance
    */
    function processPendingTransactions() private returns (bool) {
        if(!pendingTransactions.isEmpty()){
            Share memory share = pendingTransactions.getFirst();
            while (share.rewardDate <= block.timestamp) {
                address holder = share.holder;
                int256 amount = share.amount;

                holdersToRewardsBalance[holder] += amount;

                if(amount > 0) {
                    if (isHolder[holder] == false && holder != address(reserveContract)) {
                        addHolder(holder);
                    }

                    if (isEligibleToUBR[holder] == false && holdersToRewardsBalance[holder]  >= int (UBRthreshold)&& holder != address(reserveContract)) {
                        addToEligibleUBR(holder);
                    }
                }
                else {
                    if (isHolder[holder] == true && int(holdersToRewardsBalance[holder]) <= 0) {
                        removeHolder(holder);
                    } else if (isEligibleToUBR[holder] == true && int(holdersToRewardsBalance[holder]) < int(UBRthreshold)) {
                        removeFromEligibleUBR(holder);
                    }
                }


                pendingTransactions.dequeue();
                // Verify that queue is not empty
                if(pendingTransactions.isEmpty()){
                    break;
                }
                else{
                    share = pendingTransactions.getFirst();
                }
            }
            return true;
            }
            else{
                return false;
            }
    }


    function computeReward(address holder, uint256 totalShqInCirculation)
        private
        view
        returns (uint256)
    {
        uint256 balance = uint(holdersToRewardsBalance[holder]);
        if(holdersToRewardsBalance[holder] < 0){
            balance = 0;
        }
        uint256 reward = (balance * (10 ** 24)) / totalShqInCirculation;

        return reward;
    }

    function computeUBR()
        private
        view
        returns (uint256)
    {
        return currentUSDCToUBR / nbOfHolders;
    }

    // Will process all rewards including UBR
    function processAllRewards() external {
        //require(block.timestamp >= lastDistribution + 1 days, "Cannot distribute two times in a day");
        processPendingTransactions();
        if((currentShqToRewards > 0|| currentShqToUBR > 0|| currentUSDCToRewards > 0|| currentUSDCToUBR> 0 )){
            uint256 totalUSDC = 0;
            uint256 totalShqInCirculation = sheqelToken.totalSupply();

            // Swapping SHQ to USDC
            if(currentShqToRewards > 0){
                currentUSDCToRewards += swapTokenToUSDC(currentShqToRewards);
                currentShqToRewards = 0;
            }
            if(currentShqToUBR > 0){
                currentUSDCToUBR += swapTokenToUSDC(currentShqToUBR);
                currentShqToUBR = 0;
            }   


            for (uint256 i = 0; i < holders.length; i++) {
                address holder = holders[i];

                // Setting Reward and UBR
                uint256 UBRToSend = 0;
                uint256 rewardToSend = 0;

                // Check if holder is eligible to get the rewards
                if (isHolder[holder] == true) {
                    rewardToSend =
                        (computeReward(holder, totalShqInCirculation) *
                        currentUSDCToRewards) / (10 ** 24);
                    currentUSDCToRewards -= rewardToSend;

                    // Calculating if the balance is over the UBR threshold
                    if (isEligibleToUBR[holder] == true) {
                        UBRToSend = computeUBR();
                        currentUSDCToUBR -= UBRToSend;
                    }

                    uint256 totalReward = rewardToSend + UBRToSend;
                    totalUSDC += totalReward;
                    if(totalReward > 0){
                        USDC.transfer(holder, totalReward);
                    }


                }
            }

            // Sending leftover to the reserve if there is any
            if(sheqelToken.balanceOf(address(this)) > 0){
                sheqelToken.transfer(reserve, sheqelToken.balanceOf(address(this)));
                currentShqToRewards = 0;
                currentShqToUBR = 0;
            }
            if(USDC.balanceOf(address(this)) > 0){
                USDC.transfer(reserve, USDC.balanceOf(address(this)));
                currentUSDCToRewards = 0;
                currentUSDCToUBR = 0;
            }

            lastDistribution = block.timestamp;


            emit DistributedRewards(totalUSDC);
        }
        
    }

    function swapTokenToUSDC(uint256 amount) internal returns(uint256){
        uint256 balancePreswapUSDC = USDC.balanceOf(address(this));
        sheqelToken.approve(address(reserveContract), amount);
        reserveContract.sellShq(address(this), amount);

        return USDC.balanceOf(address(this)) - balancePreswapUSDC;
    }

    function rewardsBalanceOf(address _addr) public view returns (int256) {
        return holdersToRewardsBalance[_addr];
    }
}
