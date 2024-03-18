
from brownie import Contract
export FTMSCAN_TOKEN=NPC879ZBFMY5XSAQIRTDTGFT3A1GY5YW1I
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
accounts[2],
40 * 10**6 * 10**18,
spookyswapAddress,
usdc.address,
{'from': accounts[0]},
)

distributor = HolderRewarderDistributor.deploy(
        spookyswapAddress,
        reserve_contract.address,
        accounts[0],
        40 * 10**6 * 10**18,
        usdc.address,
        {'from': accounts[0]},
    )

usdc_amount = 10_000_000 * 10 ** 6
shq_amount = 1 * 10**6 * 10 ** 18

distributor.setShq(sheqeltoken.address)
sheqeltoken.setDistributor(distributor.address)
reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : accounts[0]})

usdc.transfer(accounts[0], usdc_amount, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
usdc.transfer(reserve_contract.address, 10_000_000 * 10**6, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})

# Adding liquidity to the pool
uniswapRouter = Contract.from_explorer(spookyswapAddress)
# Approving the transaction
sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
usdc.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
sheqeltoken.transfer(reserve_contract.address, 35_000_000 * 10 ** 18, {'from' : accounts[0]})


uniswapRouter.addLiquidity(
    sheqeltoken.address,
    usdc.address,
    shq_amount,
    usdc_amount - 1_000_000 * 10**6,
    0,
    0,
    accounts[0],
    1712933164 # Should be block.timestamp,
    , {"from": accounts[0]}

)

#tx=distributor.processAllRewards()
sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")

####
sheqeltoken.transfer(accounts[3], 100_000 * 10 ** 18, {'from' : accounts[0]})
sheqeltoken.transfer(accounts[4], 100_000 * 10 ** 18, {'from' : accounts[0]})
chain.mine(timedelta=60*60*25)

tx=distributor.processAllRewards()

txa=distributor.processAllRewards()

sheqeltoken.approve(reserve_contract.address, 100_000 * 10 ** 18, {'from' : accounts[0]})
usdc.approve(reserve_contract.address, 100_000 * 10 ** 6, {'from' : accounts[0]})
txa=reserve_contract.buyShq(accounts[0], 10 * 10**18, {'from' : accounts[0]})
txb=reserve_contract.sellShq(accounts[0], 10 * 10**18, {'from' : accounts[0]})