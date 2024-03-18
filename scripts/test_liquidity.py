
step = 0 
step+=1
spookyswapAddress = "0xF491e7B69E4244ad4002BC14e878a34207E38c29"

usdc_address = "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75" 
usdc = Contract.from_explorer(usdc_address)
reserve_contract = Reserve.deploy(
    spookyswapAddress,
    usdc.address,
{'from': accounts[0]},
)
sheqeltoken = SheqelToken.deploy(
reserve_contract.address,   
accounts[9],
800 * 10**6 * 10**18,
spookyswapAddress,
usdc.address,
{'from': accounts[0]},
)

distributor = HolderRewarderDistributor.deploy(
        spookyswapAddress,
        reserve_contract.address,
        accounts[0],
        sheqeltoken.totalSupply(),
        usdc.address,
        {'from': accounts[0]},
    )

usdc_amount = 10_000 * 10 ** 6
shq_amount_liq = 166_000 * 10 ** 18
shq_amount = 5 * 10**6 * 10 ** 18

distributor.setShq(sheqeltoken.address)
sheqeltoken.setDistributor(distributor.address)
reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : accounts[0]})

# Burning (now also happening in the constructor)
usdc.transfer(accounts[0], 2*990 * 10**6, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
usdc.approve(reserve_contract.address, 100_000 * 10 ** 6, {'from' : accounts[0]})


usdc.transfer(reserve_contract.address, 990 * 10**6, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
print(step, "Everything is set up and no transactions have been made", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice())
step+=1

tx=reserve_contract.buyShq(accounts[0], 2 * 10**18, {'from' : accounts[0]})
sheqeltoken.transfer("0x1234567890123456789012345678901234567890", 2 * 10**18, {'from' : accounts[0]})
step+=1




# Adding liquidity to the pool
uniswapRouter = Contract.from_explorer(spookyswapAddress)
# Approving the transaction
sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
usdc.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})

# Buying the adequate liquidity
usdc.approve(reserve_contract, 100000*10**18, {"from": accounts[0]})
#reserve_contract.buyShq(accounts[0], shq_amount_liq, {'from' : accounts[0]}) Already have the SHQ !!



uniswapRouter.addLiquidity(
    sheqeltoken.address,
    usdc.address,
    shq_amount_liq,
    10*10**6,
    0,
    0,
    accounts[0],
    1712933164 # Should be block.timestamp,
    , {"from": accounts[0]}

)
step+=1

distributor.processAllRewards()
sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")
step+=1
tx=sheqeltoken.initiateLiquidityProviding({"from": accounts[0]})