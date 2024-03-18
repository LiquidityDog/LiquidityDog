from brownie import Contract, accounts
from random import randint
import csv

def get_balances(accounts, sheqel_token, usdc):
    shq_balances = [sheqel_token.balanceOf(account.address) for account in accounts]
    usdc_balances = [usdc.balanceOf(account.address) for account in accounts]
    return shq_balances, usdc_balances


with open('noReinvestWithDistributorWithLiquidity.csv', 'w', newline='') as file:
    writer = csv.writer(file)


    step = 0 
    writer.writerow([
    "Step", 
    "Comment", 
    "Reserve SHQ", 
    "Reserve USDC", 
    "Distributor SHQ", 
    "Distributor USDC", 
    "MDO SHQ", 
    "MDO USDC", 
    "SHQ buyPrice", 
    "SHQ sellPrice", 
    "SHQ sellPrice/buyPrice",
    "SHQ Reserve in liquidity pool",
    "USDC Reserve in liquidity pool",
        ] + [f"Account {i} SHQ" for i in range(10)] + [f"Account {i} USDC" for i in range(10)]) 
    step+=1
    spookyswapAddress = "0xF491e7B69E4244ad4002BC14e878a34207E38c29"
    spookyswapFactory = Contract.from_explorer("0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3")

    usdc_address = "0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605" 
    usdc = USDC.deploy(1500000*9 * 10 ** 6, {'from': accounts[0]})
    reserve = Reserve.deploy(
        spookyswapAddress,
        usdc.address,
    {'from': accounts[0]},
    )
    sheqel_token = SheqelToken.deploy(
    reserve.address,   
    "0xfff739fC224dFfD50ff400063fB261010A7c0028",
    800 * 10**6 * 10**18,
    spookyswapAddress,
    usdc.address,
    {'from': accounts[0]},
    )

    pairContract = Contract.from_abi("Pair", sheqel_token.uniswapV2PairContract(), [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":True,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":True,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":False,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sync","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}])


    distributor = Distributor.deploy(
            usdc.address,
            reserve.address,
            {'from': accounts[0]},
        )

    usdc_amount = 10_000 * 10 ** 6
    shq_amount_liq = 166_000 * 10 ** 18
    shq_amount = 5 * 10**6 * 10 ** 18

    distributor.setShq(sheqel_token.address)
    sheqel_token.setDistributor(distributor.address)
    reserve.setSheqelTokenAddress(sheqel_token.address, {'from' : accounts[0]})

    # Burning (now also happening in the constructor)
    usdc.approve(reserve.address, 100_000 * 10 ** 6, {'from' : accounts[0]})

    

    step+=1

    total_addresses = 10



    usdc.transfer(reserve.address, 1000 * 10**6, {'from': accounts[0]})

    print(pairContract.getReserves()[0], pairContract.getReserves()[1])


    amount_to_buy = 1000000 / total_addresses

    print("VERIFY IF TRUE: ", pairContract.token0() == usdc.address)
    print("VERIFY IF TRUE: ", pairContract.token1() == sheqel_token.address)

    for i in range(0,10):
        usdc.transfer(accounts[i].address, amount_to_buy * 10**6, {'from': accounts[0]})
        usdc.approve(reserve.address, amount_to_buy * 10**6, {'from': accounts[i]})

        reserve.buyShqWithUsdc(accounts[i].address, amount_to_buy* 10**6, {'from': accounts[i]})
        print("Step " + str(step) + ": " + str(amount_to_buy) + " USDC worth of SHQ bought by " + accounts[i].address)
        shq_balances, usdc_balances = get_balances(accounts[:10], sheqel_token, usdc)

        shq_balances, usdc_balances = get_balances(accounts[:10], sheqel_token, usdc)

        # Write the updated row with account balances
        writer.writerow([
            step, 
            str(amount_to_buy) + " USDC worth of SHQ bought by " + accounts[i].address, 
            sheqel_token.balanceOf(reserve.address), 
            usdc.balanceOf(reserve.address), 
            sheqel_token.balanceOf(distributor.address), 
            usdc.balanceOf(distributor.address), 
            sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
            usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
            reserve.buyPriceWithTax(), 
            reserve.sellPrice() - reserve.sellPrice() * 0.05, 
            (reserve.sellPrice() - reserve.sellPrice() * 0.05) / reserve.buyPriceWithTax(),
            pairContract.getReserves()[1],
            pairContract.getReserves()[0],

        ] + shq_balances + usdc_balances)

    
    accounts_addresses = [account.address for account in accounts]

    # Burning the remaining USDC
    usdc.transfer("0x0000000000000000000000000000000000000001", usdc.balanceOf(accounts[0].address), {'from': accounts[0]})

    # Add liquidity
    account_index = randint(0, 9)
    sheqel_token.initiateLiquidityProviding({'from': accounts[account_index]})
    writer.writerow([
        step, 
        "Liquidity provided by " + accounts[account_index].address, 
        sheqel_token.balanceOf(reserve.address), 
        usdc.balanceOf(reserve.address), 
        sheqel_token.balanceOf(distributor.address), 
        usdc.balanceOf(distributor.address), 
        sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
        usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
        reserve.buyPriceWithTax(), 
        reserve.sellPrice() - reserve.sellPrice() * 0.05, 
        (reserve.sellPrice() - reserve.sellPrice() * 0.05) / reserve.buyPriceWithTax(),
        pairContract.getReserves()[1],
        pairContract.getReserves()[0],
    ] + shq_balances + usdc_balances)
        



    while step < 1200:
        if step % 80 == 0:
            # distribute rewards
            distributor.processAllRewards(
                [account.address for account in accounts],
                [sheqel_token.balanceOf(account.address) for account in accounts],
                [account.address for account in accounts],
                sum(sheqel_token.balanceOf(account.address) for account in accounts),
                {'from': accounts[0]}
            )
            print("Step " + str(step) + ": Rewards distributed")
            shq_balances, usdc_balances = get_balances(accounts[:10], sheqel_token, usdc)

            writer.writerow([
            step, 
            "Rewards distributed", 
            sheqel_token.balanceOf(reserve.address), 
            usdc.balanceOf(reserve.address), 
            sheqel_token.balanceOf(distributor.address), 
            usdc.balanceOf(distributor.address), 
            sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
            usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
            reserve.buyPriceWithTax(), 
            reserve.sellPrice() - reserve.sellPrice() * 0.05, 
            (reserve.sellPrice() - reserve.sellPrice() * 0.05) / reserve.buyPriceWithTax(),
            pairContract.getReserves()[1],
            pairContract.getReserves()[0],
            ] + shq_balances + usdc_balances)
            
        sender_index = randint(0, total_addresses - 1)
        receiver_index = randint(0, total_addresses - 1)

        while sender_index == receiver_index:
            receiver_index = randint(0, total_addresses - 1)
        
        sender = accounts[sender_index]
        receiver = accounts[receiver_index]

        while sheqel_token.balanceOf(sender.address) == 0:
            sender_index = randint(0, total_addresses - 1)
            sender = accounts[sender_index]

        amount = sheqel_token.balanceOf(sender.address)

        tx = sheqel_token.transfer(receiver.address, amount, {'from': sender.address})

        print("Step " + str(step) + ": " + str(amount) + " SHQ sent from " + sender.address + " to " + receiver.address)
        shq_balances, usdc_balances = get_balances(accounts[:10], sheqel_token, usdc)  # Get balances for accounts 0 to 9

        writer.writerow([
            step, 
            str(amount) + " SHQ sent from " + sender.address + " to " + receiver.address, 
            sheqel_token.balanceOf(reserve.address), 
            usdc.balanceOf(reserve.address), 
            sheqel_token.balanceOf(distributor.address), 
            usdc.balanceOf(distributor.address), 
            sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
            usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"),
            reserve.buyPriceWithTax(), 
            reserve.sellPrice() - reserve.sellPrice() * 0.05, 
            (reserve.sellPrice() - reserve.sellPrice() * 0.05)/ reserve.buyPriceWithTax(),
            pairContract.getReserves()[1],
            pairContract.getReserves()[0],
        ] + shq_balances + usdc_balances)        
        
        '''if step % 100 == 0:
            for i in range(0,10):
                # make 25% chance of buying SHQ with USDC
                if randint(0, 3) == 0:
                    amount_to_buy = usdc.balanceOf(accounts[i].address) / 10**6
                    usdc.approve(reserve.address, amount_to_buy * 10**6, {'from': accounts[i]})

                    reserve.buyShqWithUsdc(accounts[i].address, amount_to_buy* 10**6, {'from': accounts[i]})
                    print("Step " + str(step) + ": " + str(amount_to_buy) + " USDC worth of SHQ bought by " + accounts[i].address)
                    shq_balances, usdc_balances = get_balances(accounts[:10], sheqel_token, usdc)

                    # Write the updated row with account balances
                    writer.writerow([
                        step, 
                        str(amount_to_buy) + " USDC rebuy of SHQ bought by " + accounts[i].address, 
                        sheqel_token.balanceOf(reserve.address), 
                        usdc.balanceOf(reserve.address), 
                        sheqel_token.balanceOf(distributor.address), 
                        usdc.balanceOf(distributor.address), 
                        sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
                        usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
                        reserve.buyPriceWithTax(), 
                        reserve.sellPrice() - reserve.sellPrice() * 0.05, 
                        (reserve.sellPrice() - reserve.sellPrice() * 0.05) / reserve.buyPriceWithTax(),
                        pairContract.getReserves()[1],
                        pairContract.getReserves()[0],
                    ] + shq_balances + usdc_balances)
        '''
                    

        if step % 150 == 0:
            # Add liquidity
            account_index = randint(0, 9)
            sheqel_token.initiateLiquidityProviding({'from': accounts[account_index]})
            writer.writerow([
                step, 
                "Liquidity provided by " + accounts[account_index].address, 
                sheqel_token.balanceOf(reserve.address), 
                usdc.balanceOf(reserve.address), 
                sheqel_token.balanceOf(distributor.address), 
                usdc.balanceOf(distributor.address), 
                sheqel_token.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
                usdc.balanceOf("0xfff739fC224dFfD50ff400063fB261010A7c0028"), 
                reserve.buyPriceWithTax(), 
                reserve.sellPrice() - reserve.sellPrice() * 0.05, 
                (reserve.sellPrice() - reserve.sellPrice() * 0.05) / reserve.buyPriceWithTax(),
                pairContract.getReserves()[1],
                pairContract.getReserves()[0],
            ] + shq_balances + usdc_balances)

        step+=1

        

