    from brownie import accounts, USDC, Reserve, SheqelToken, Distributor, Contract
    import requests
    # Setting swap adresse + deployment of USDC
    spookyswapAddress = "0xF491e7B69E4244ad4002BC14e878a34207E38c29"#"0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff" # polygon testnet
    acct = accounts.load('shqdeployer')
    usdc = USDC.deploy(100_000_000 * 10 ** 6, {'from': acct}) 

    reserve_contract = Reserve.deploy(
        spookyswapAddress,
        usdc.address,
    {'from': acct}
    )
    sheqeltoken = SheqelToken.deploy(
    reserve_contract.address,   
    acct,
    800 * 10**6 * 10**18,
    spookyswapAddress,
    usdc.address,
    {'from': acct}
    )

    distributor = Distributor.deploy(
            usdc.address,
            reserve_contract.address,
            {'from': acct}
        )

    usdc_amount = 10_000 * 10 ** 6
    usdc_amount_liq = 1 * 10**6
    shq_amount_liq = 2000 * 10 ** 18
    shq_amount = 5 * 10**6 * 10 ** 18

    distributor.setShq(sheqeltoken.address)
    sheqeltoken.setDistributor(distributor.address)
    reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : acct})

    # Setting base usdc amount to reserve
    usdc.transfer(reserve_contract.address, 999 * 10**6, {'from' : acct})

    # Setting up liquidity
    # Adding liquidity to the pool
    uniswapRouter = Contract.from_explorer(spookyswapAddress)
    # Approving the transaction
    sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": acct})
    usdc.approve(spookyswapAddress, shq_amount, {"from": acct})

    # Buying the adequate liquidity
    usdc.approve(reserve_contract, 1 * 10**6, {"from": acct})



    uniswapRouter.addLiquidity(
        sheqeltoken.address,
        usdc.address,
        shq_amount_liq,
        1*10**6,
        0,
        0,
        acct,
        1712933164 # Should be block.timestamp,
        , {"from": acct}

    )

    # Sending 9k USDC to shelvey metamask and 3.5k to FP
    usdc.transfer("0x912858f594596B93abD9bBbA663E24aF53FaDE7d", 9000 * 10**6, {'from' : acct}) # shelvey
    usdc.transfer("0x58Dbcfa99EaDAA55eC8139C4Bd53A36D748bB436", 3500 * 10**6, {'from' : acct}) # FP

    # Sending half of the 197998 SHQ to shelvey and half to FP
    sheqeltoken.transfer("0x912858f594596B93abD9bBbA663E24aF53FaDE7d", (197998/2 -1) * 10**18, {'from' : acct}) # shelvey
    sheqeltoken.transfer("0x58Dbcfa99EaDAA55eC8139C4Bd53A36D748bB436", (197998/2 -1) * 10**18, {'from' : acct}) # FP


    print("Sheqel Token Address : " + sheqeltoken.address)
    print("Reserve Address : " + reserve_contract.address)
    print("Distributor Address : " + distributor.address)
    print("USDC Address : " + usdc.address)
    print("DeX Address : " + spookyswapAddress)


    ## TO DELETE ONLY TEST
    usdc.approve(reserve_contract.address, 3500 * 10**6, {"from": "0x58Dbcfa99EaDAA55eC8139C4Bd53A36D748bB436"})
    reserve_contract.buyShqWithUsdc(acct,  3500 * 10**6, {'from' : "0x58Dbcfa99EaDAA55eC8139C4Bd53A36D748bB436"})

    usdc.approve(reserve_contract.address, 9000 * 10**6, {"from": "0x912858f594596B93abD9bBbA663E24aF53FaDE7d"})
    reserve_contract.buyShqWithUsdc(acct,  9000 * 10**6, {'from' : "0x912858f594596B93abD9bBbA663E24aF53FaDE7d"})

    BURN_ADDRESS = '0x1234567890123456789012345678901234567890'
    RESERVE_ADDRESS= reserve_contract.address
    DISTRIBUTOR_ADDRESS = distributor.address
    SHEQEL_ADDRESS = sheqeltoken.address
    LIQUIDITY_ADDRESS = spookyswapAddress
    # distribute rewards

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
    response = [holder for holder in response if holder['holderAddress'] != BURN_ADDRESS and holder['holderAddress'] != RESERVE_ADDRESS and holder['holderAddress'] != LIQUIDITY_ADDRESS]
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


    holders = ['0x2c86ff0746e87c250bba4b52d2e1203379acdd3e', '0x338c9aa56390c6a15bc5e6d3209ccdb47eb72630', '0x58dbcfa99eadaa55ec8139c4bd53a36d748bb436', '0x7970c938b4dc547edcfe847bbbead4b8036df306', '0x912858f594596b93abd9bbba663e24af53fade7d']
    balances = [1860000000000000000000, 18248175182481751824817, 739018232421441774491682, 2000000000000000000, 1744353801832201211676152]
    UBR = ['0x2c86ff0746e87c250bba4b52d2e1203379acdd3e', '0x338c9aa56390c6a15bc5e6d3209ccdb47eb72630', '0x58dbcfa99eadaa55ec8139c4bd53a36d748bb436', '0x912858f594596b93abd9bbba663e24af53fade7d']
    print(holders)
    print(balances)
    print(UBR)
    distributor = Contract.from_abi(
        "Distributor",
        DISTRIBUTOR_ADDRESS,
        [{"inputs":[{"internalType":"address","name":"_usdcAddress","type":"address"},{"internalType":"address","name":"_reserveAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"USDC","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentShqToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addToCurrentUsdcToUBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentShqToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentShqToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentUSDCToUBR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastDistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"_addresses","type":"address[]"},{"internalType":"uint256[]","name":"_balances","type":"uint256[]"},{"internalType":"address[]","name":"_ubrAddresses","type":"address[]"},{"internalType":"uint256","name":"_totalBalance","type":"uint256"}],"name":"processAllRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"reserveContract","outputs":[{"internalType":"contract IReserve","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"setShq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sheqelToken","outputs":[{"internalType":"contract ISheqelToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"shqSet","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"teamAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
    )
    holder = '0x2c86ff0746e87c250bba4b52d2e1203379acdd3e'
    totBal = sum(balances)
    print((distributor.currentUSDCToRewards() * balances[holders.index(holder)]) / totBal)
    print(distributor.currentUSDCToRewards())
    print(distributor.currentUSDCToUBR())

    tx=distributor.processAllRewards(
        holders,
        balances,
        UBR,
        sum(balances),
        {'from': acct})


                                                            


