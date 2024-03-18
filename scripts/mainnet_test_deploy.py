from brownie import accounts, USDC, Reserve, SheqelToken, Distributor, Contract

# Setting swap adresse + deployment of USDC
spookyswapAddress = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff" # polygon testnet and mainnet
acct = accounts.load('shqdeployer')
usdc = Contract.from_explorer("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")

MDO_address = "0x9feA2E7f60b21eC4B5ed571fBCEC27Fa620fd48d"

reserve_contract = Reserve.deploy(
    spookyswapAddress,
    usdc.address,
{'from': acct},publish_source=True
)
#OK
sheqeltoken = SheqelToken.deploy(
reserve_contract.address,   
MDO_address,
800 * 10**6 * 10**18,
spookyswapAddress,
usdc.address,
{'from': acct},publish_source=True
)

#OK

distributor = Distributor.deploy(
        usdc.address,
        reserve_contract.address,
        {'from': acct},publish_source=True
    )

usdc_amount = 1 * 10 ** 6
usdc_amount_liq = 0.2 * 10**6
shq_amount_liq = 20 * 10 ** 18
shq_amount = 5 * 10**6 * 10 ** 18

distributor.setShq(sheqeltoken.address)
sheqeltoken.setDistributor(distributor.address)
reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : acct})

# Setting base usdc amount to reserve
usdc.transfer(reserve_contract.address, usdc_amount, {'from' : acct})

# Setting up liquidity
# Adding liquidity to the pool
uniswapRouter = Contract.from_explorer(spookyswapAddress)
# Approving the transaction
sheqeltoken.approve(spookyswapAddress, shq_amount_liq, {"from": acct})
usdc.approve(spookyswapAddress, usdc_amount_liq, {"from": acct})

# Buying the adequate liquidity
usdc.approve(reserve_contract, usdc_amount, {"from": acct})



uniswapRouter.addLiquidity(
    sheqeltoken.address,
    usdc.address,
    shq_amount_liq,
    usdc_amount_liq,
    0,
    0,
    acct,
    1712933164 # Should be block.timestamp,
    , {"from": acct}

)

# Sending half of the 197998 SHQ to shelvey and half to FP
sheqeltoken.transfer("0x912858f594596B93abD9bBbA663E24aF53FaDE7d", (180/2 -1) * 10**18, {'from' : acct}) # shelvey
sheqeltoken.transfer("0x58Dbcfa99EaDAA55eC8139C4Bd53A36D748bB436", (180/2 -1) * 10**18, {'from' : acct}) # FP


print("Sheqel Token Address : " + sheqeltoken.address)
print("Reserve Address : " + reserve_contract.address)
print("Distributor Address : " + distributor.address)
print("USDC Address : " + usdc.address)
print("DeX Address : " + spookyswapAddress)  


