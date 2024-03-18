from brownie import Contract, accounts
from random import randint
import csv

sheqel_token_abi = [{"inputs":[{"internalType":"address","name":"_reserveAddress","type":"address"},{"internalType":"address","name":"_MDOAddress","type":"address"},{"internalType":"uint256","name":"_tSupply","type":"uint256"},{"internalType":"address","name":"_spookyswapAddress","type":"address"},{"internalType":"address","name":"_USDCAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"MDOAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"USDC","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WFTM","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"distributor","outputs":[{"internalType":"contract Distributor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDistributor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initiateLiquidityProviding","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"liquidityManagerAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveContract","outputs":[{"internalType":"contract Reserve","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setDistributor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"spookySwapAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2PairContract","outputs":[{"internalType":"contract IUniswapV2Pair","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
reserve_abi = [{"inputs":[{"internalType":"address","name":"_spookyswapRouter","type":"address"},{"internalType":"address","name":"_usdcAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"amountSHQ","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amountUSDC","type":"uint256"}],"name":"ShqBought","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"amountSHQ","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amountUSDC","type":"uint256"}],"name":"ShqSold","type":"event"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"addToShqToConvert","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"buyPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"buyPriceWithTax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_shqAmount","type":"uint256"}],"name":"buyShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_usdcAmount","type":"uint256"}],"name":"buyShqWithUsdc","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"distributor","outputs":[{"internalType":"contract Distributor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sellPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_shqAmount","type":"uint256"}],"name":"sellShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setSheqelTokenAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_taxRate","type":"uint256"}],"name":"setTaxRate","outputs":[],"stateMutability":"nonpayable","type":"function"}]
distributor_abi = [{"inputs":[{"internalType":"address","name":"_usdcAddress","type":"address"},{"internalType":"address","name":"_reserveAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"message","type":"string"},{"indexed":False,"internalType":"uint256","name":"data","type":"uint256"}],"name":"Log","type":"event"},{"inputs":[],"name":"USDC","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentShqToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentShqToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastDistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"_addresses","type":"address[]"},{"internalType":"uint256[]","name":"_balances","type":"uint256[]"},{"internalType":"address[]","name":"_ubrAddresses","type":"address[]"},{"internalType":"uint256","name":"_totalBalance","type":"uint256"}],"name":"processAllRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"reserveContract","outputs":[{"internalType":"contract IReserve","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sheqelToken","outputs":[{"internalType":"contract ISheqelToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"shqSet","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
usdc_abi = [{"inputs":[{"internalType":"address","name":"_proxyTo","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_new","type":"address"},{"indexed":False,"internalType":"address","name":"_old","type":"address"}],"name":"ProxyOwnerUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_new","type":"address"},{"indexed":True,"internalType":"address","name":"_old","type":"address"}],"name":"ProxyUpdated","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"IMPLEMENTATION_SLOT","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"OWNER_SLOT","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxyOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxyType","outputs":[{"internalType":"uint256","name":"proxyTypeId","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferProxyOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newProxyTo","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"updateAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_newProxyTo","type":"address"}],"name":"updateImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

with open('betweenUsersTotal.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    step = 0 
    writer.writerow(["Step", "Comment", "Reserve SHQ", "Reserve USDC", "Distributor SHQ", "Distributor USDC", "MDO SHQ", "MDO USDC", "SHQ buyPrice", "SHQ sellPrice", "SHQ sellPrice/buyPrice"])
    step+=1

    # Initialize real contract addresses
    reserve = Contract("0xc44B03488eb7C713c9692EC7653569e58004Ac27")
    sheqel_token = Contract("0x6e55E57f3373d4E072dDaD0B777CC48044527527")
    distributor = Contract("0x59a04a66A35614e9e1cFf2cCbE4D46EFE52F544b")
    usdc = Contract.from_explorer("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")

    data = {
    "addresses": [
        {"address": "0x912858f594596b93abd9bbba663e24af53fade7d", "balance": 1926375648054608844595745, "used": 0},
        {"address": "0x25c96c82f97304ac9ea5850c118327d22e153dd6", "balance": 768777436786440415878724, "used": 0},
        {"address": "0x58dbcfa99eadaa55ec8139c4bd53a36d748bb436", "balance": 615818357659526375755925, "used": 0},
        {"address": "0x08efd0101756d12f0837073ab69ae2b46c2ea6f4", "balance": 313585046010120954444058, "used": 0},
        {"address": "0x296ac22b1fd2a2c218f0207168cdb168b0362ca2", "balance": 185916088306887264141800, "used": 0},
        {"address": "0x057dfe28ac9fe001d1e2533e9f5fe3d0f6eab651", "balance": 100578893675999000550801, "used": 0},
        {"address": "0x3f889d0e1103ea0b291ad2b04df7877983481989", "balance": 42216582582109695903419, "used": 0},
        {"address": "0x967e42134f50fe95065aab36af72a12fbee5118f", "balance": 36094450077155353349889, "used": 0},
        {"address": "0xc48a771477361455205c713008c2f7368f7b252a", "balance": 32065457468627436009490, "used": 0},
        {"address": "0xd012d3fd29a0c0fa886919e6a1dc094e4b0ba3f3", "balance": 26755330517828227473909, "used": 0},
        {"address": "0x3dfce3c95adaf38e7f988e311a826d0647bbed9d", "balance": 18853974121996303142329, "used": 0},
        {"address": "0x7d634626d4416c14316e2c444a68f13321399a48", "balance": 17664559315730754927482, "used": 0},
        {"address": "0x9ecc9e4acb7fb78efeff58240a0bb5ce658b8e26", "balance": 6153272422151780719746, "used": 0},
        {"address": "0xa61b1d479cdf6f5be938ca96e2de2634e00208b6", "balance": 5407421219466716390080, "used": 0}
    ]
}
    
    writer.writerow([step, "Everything is set up and no transactions have been made, Buying the reserve to 1M", sheqel_token.balanceOf(reserve.address), usdc.balanceOf(reserve.address), sheqel_token.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqel_token.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve.buyPriceWithTax(), reserve.sellPrice() - reserve.sellPrice() *0.05, reserve.sellPrice()/reserve.buyPriceWithTax()])


    step+=1

    total_addresses = 14


    binance_address = "0xe7804c37c13166fF0b37F5aE0BB07A3aEbb6e245"

    amount_to_buy = 1000000 / total_addresses

    for address in data["addresses"]:
        usdc.transfer(address["address"], amount_to_buy * 10**6, {'from': binance_address})
        usdc.approve(reserve, amount_to_buy * 10**6, {'from': address["address"]})

        reserve.buyShqWithUsdc(address["address"], amount_to_buy* 10**6, {'from': address["address"]})
        print("Step " + str(step) + ": " + str(amount_to_buy) + " USDC worth of SHQ bought by " + address["address"])
        writer.writerow([step, str(amount_to_buy) + " USDC worth of SHQ bought by " + address["address"], sheqel_token.balanceOf(reserve.address), usdc.balanceOf(reserve.address), sheqel_token.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqel_token.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve.buyPriceWithTax(), reserve.sellPrice() - reserve.sellPrice() *0.05, reserve.sellPrice() - reserve.sellPrice() *0.05/reserve.buyPriceWithTax()])
        



    while any(sheqel_token.balanceOf(address['address']) > 0 for address in data["addresses"]):
        if step % 1000 == 0:
            # distribute rewards
            distributor.processAllRewards(
                [address["address"] for address in data["addresses"]],
                [sheqel_token.balanceOf(address["address"]) for address in data["addresses"]],
                [address["address"] for address in data["addresses"]],
                sum(sheqel_token.balanceOf(address["address"]) for address in data["addresses"]),
                {'from': "0x7970C938b4DC547edCfe847BbbEad4B8036DF306"}
            )
            step+=1
            print("Step " + str(step) + ": Rewards distributed")
            writer.writerow([step, "Rewards distributed", sheqel_token.balanceOf(reserve.address), usdc.balanceOf(reserve.address), sheqel_token.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqel_token.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve.buyPriceWithTax(), reserve.sellPrice() - reserve.sellPrice() *0.05, reserve.sellPrice() - reserve.sellPrice() *0.05/reserve.buyPriceWithTax()])

        sender_index = randint(0, total_addresses - 1)
        receiver_index = randint(0, total_addresses - 1)

        while sender_index == receiver_index:
            receiver_index = randint(0, total_addresses - 1)
        
        sender = data["addresses"][sender_index]
        receiver = data["addresses"][receiver_index]

        while sheqel_token.balanceOf(sender["address"]) == 0:
            sender_index = randint(0, total_addresses - 1)
            sender = data["addresses"][sender_index]

        amount = sheqel_token.balanceOf(sender["address"])

        tx = sheqel_token.transfer(receiver["address"], amount, {'from': sender["address"]})

        print("Step " + str(step) + ": " + str(amount) + " SHQ sent from " + sender["address"] + " to " + receiver["address"])
        writer.writerow([step, str(amount) + " SHQ sent from " + sender["address"] + " to " + receiver["address"], sheqel_token.balanceOf(reserve.address), usdc.balanceOf(reserve.address), sheqel_token.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqel_token.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve.buyPriceWithTax(), reserve.sellPrice() - reserve.sellPrice() *0.05, reserve.sellPrice() - reserve.sellPrice() *0.05/reserve.buyPriceWithTax()])
        step+=1

        

