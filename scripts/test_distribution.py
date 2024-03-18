from brownie import accounts, USDC, Reserve, SheqelToken, Distributor, Contract

# Setting swap adresse + deployment of USDC
spookyswapAddress = "0xF491e7B69E4244ad4002BC14e878a34207E38c29" # ftm main fork
acct = accounts.load('shqdeployer')
usdc = USDC.deploy(100_000_000 * 10 ** 6, {'from': acct}, publish_source=True) 

reserve_contract = Reserve.deploy(
    spookyswapAddress,
    usdc.address,
{'from': acct},publish_source=True
)
sheqeltoken = SheqelToken.deploy(
reserve_contract.address,   
acct,
800 * 10**6 * 10**18,
spookyswapAddress,
usdc.address,
{'from': acct},publish_source=True
)

distributor = Distributor.deploy(
        usdc.address,
        reserve_contract.address,
        {'from': acct},publish_source=True
    )
# hey
usdc_amount = 10_000 * 10 ** 6
shq_amount_liq = 166_000 * 10 ** 18
shq_amount = 5 * 10**6 * 10 ** 18

distributor.setShq(sheqeltoken.address)
sheqeltoken.setDistributor(distributor.address)
reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : acct})

# Setting base usdc amount to reserve
usdc.transfer(reserve_contract.address, 990 * 10**6, {'from' : acct})

# Setting up liquidity
    # Adding liquidity to the pool
uniswapRouter = Contract.from_explorer(spookyswapAddress)
# Approving the transaction
sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": acct})
usdc.approve(spookyswapAddress, shq_amount, {"from": acct})

# Buying the adequate liquidity
usdc.approve(reserve_contract, 100000*10**18, {"from": acct})
#reserve_contract.buyShq(acct, shq_amount_liq, {'from' : acct}) Already have the SHQ !!



uniswapRouter.addLiquidity(
    sheqeltoken.address,
    usdc.address,
    shq_amount_liq,
    10*10**6,
    0,
    0,
    acct,
    1712933164 # Should be block.timestamp,
    , {"from": acct}

)

# Buying 10000USDC worth of SHQ from the reserve to test
usdc.approve(reserve_contract.address, 10000*10**6, {"from": acct})
reserve_contract.buyShqWithUsdc(acct, 10000*10**6, {'from' : acct})

acctShqbalance = sheqeltoken.balanceOf(acct)

# Sending  SHQ to random accounts
sheqeltoken.transfer("0x18EC2101fEb19F245b5BFaDf4F925398d1B3DB00", acctShqbalance/20, {'from' : acct})
sheqeltoken.transfer("0xdd00e9794A5B1ebc8227CA2A44C3eA8615745D72", acctShqbalance/10, {'from' : acct})
sheqeltoken.transfer("0xC052f4bE270c2F0F736f1cC1AE0B3bADd3F09Ccf", acctShqbalance/8, {'from' : acct})
balanceBefore = sheqeltoken.balanceOf(acct)
sheqeltoken.transfer("0x5d13f4bf21db713e17e04d711e0bf7eaf18540d6", 100*10**18, {'from' : acct})
balanceAfter = sheqeltoken.balanceOf(acct)
print(balanceBefore - balanceAfter)

import requests
BURN_ADDRESS = '0x1234567890123456789012345678901234567890'
RESERVE_ADDRESS= reserve_contract.address
DISTRIBUTOR_ADDRESS = distributor.address
SHEQEL_ADDRESS = sheqeltoken.address
acct = accounts[0]

url = "https://rpc.ankr.com/multichain/?ankr_getTokenHolders="

payload = {
    "jsonrpc": "2.0",
    "method": "ankr_getTokenHolders",
    "params": {
        "blockchain": "polygon_mumbai",
        "contractAddress": SHEQEL_ADDRESS
    },
    "id": 1
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

response = response.json()['result']['holders']
print(response)
# Remove the burn address and the reserve address from the array
response = [holder for holder in response if holder['holderAddress'] != BURN_ADDRESS and holder['holderAddress'] != RESERVE_ADDRESS]
# Take all 'holderAddress'
holders = [holder['holderAddress'] for holder in response]
# Take all 'balanceRawInteger'
balances = [int(holder['balanceRawInteger']) for holder in response]

# Calculate mean balance
mean_balance = int(sum(balances) / len(balances))
# Number of addresses over mean balance divided by 1000
num_addresses_over_threshold = len([balance for balance in balances if balance > (mean_balance/ 1000)])
print(holders)
print(balances)
print(mean_balance)
print(num_addresses_over_threshold)

distributor = Contract.from_explorer(DISTRIBUTOR_ADDRESS)

distributor.processAllRewards(
    holders,
    balances,
    mean_balance,
    num_addresses_over_threshold,
    {'from': acct})



                                                        


