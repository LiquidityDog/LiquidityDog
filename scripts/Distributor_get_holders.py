import requests
acct = accounts.load('shqdeployer')
"""
Addresses Definitions
"""
BURN_ADDRESS = '0x1234567890123456789012345678901234567890'
RESERVE_ADDRESS= '0x99B687e58Bb7cb9000c502Dd62f58910BC7f8592'
DISTRIBUTOR_ADDRESS = '0x1BD7F6237Cc7B7026aD585799567Aeb1c8f043AD'
SHEQEL_ADDRESS = '0x721Fa74C94830f0Cb93C8Ec2D80fd2099EDA8AD3'
LIQUIDITY_ADDRESS = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
reserve_contract = Contract.from_abi("Reserve",
                                     RESERVE_ADDRESS,
                                     [{"inputs":[{"internalType":"address","name":"_spookyswapRouter","type":"address"},{"internalType":"address","name":"_usdcAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"amountSHQ","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amountUSDC","type":"uint256"}],"name":"ShqBought","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"amountSHQ","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amountUSDC","type":"uint256"}],"name":"ShqSold","type":"event"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"addToShqToConvert","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"buyPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"buyPriceWithTax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_shqAmount","type":"uint256"}],"name":"buyShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_usdcAmount","type":"uint256"}],"name":"buyShqWithUsdc","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"distributor","outputs":[{"internalType":"contract HolderRewarderDistributor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sellPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_shqAmount","type":"uint256"}],"name":"sellShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setSheqelTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_taxRate","type":"uint256"}],"name":"setTaxRate","outputs":[],"stateMutability":"nonpayable","type":"function"}])

# Account Loading 



"""
Requesting the holders from Ankr
"""

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
# Remove the burn address and the reserve address from the array
response = [holder for holder in response if holder['holderAddress'] != BURN_ADDRESS.lower() and holder['holderAddress'] != RESERVE_ADDRESS.lower() and holder['holderAddress'] != LIQUIDITY_ADDRESS.lower() and holder['holderAddress'] != DISTRIBUTOR_ADDRESS.lower()]
# Take all 'holderAddress'
holders = [holder['holderAddress'] for holder in response]
# Take all 'balanceRawInteger'
balances = [int(holder['balanceRawInteger']) for holder in response]

"""
Calculate holders eligible for UBR
"""

# Requesto to reserve to get the buyPrice
buyPrice = reserve_contract.buyPrice({'from': acct})
# Decrease buyprice by 7%
buyPrice = (buyPrice * 0.93)/10**6

# Calculate balance of SHQ for each holder and add them to UBR array of more than 5USDC

MINIMUM_SHQ_WORTH_USDC = 5

UBR = []
for holder in holders:
    formatted_balance = balances[holders.index(holder)]/10**18
    if buyPrice*formatted_balance > MINIMUM_SHQ_WORTH_USDC:
        UBR.append(holder)


"""
Calculating the rewards
"""
distributor = Contract.from_abi(
    "Distributor",
    DISTRIBUTOR_ADDRESS,
    [{"inputs":[{"internalType":"address","name":"_usdcAddress","type":"address"},{"internalType":"address","name":"_reserveAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"USDC","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentShqToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentShqToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastDistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"_addresses","type":"address[]"},{"internalType":"uint256[]","name":"_balances","type":"uint256[]"},{"internalType":"address[]","name":"_ubrAddresses","type":"address[]"},{"internalType":"uint256","name":"_totalBalance","type":"uint256"}],"name":"processAllRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"reserveContract","outputs":[{"internalType":"contract IReserve","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sheqelToken","outputs":[{"internalType":"contract ISheqelToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"shqSet","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
)

tx=distributor.processAllRewards(
    holders,
    balances,
    UBR,
    sum(balances),
    {'from': acct})