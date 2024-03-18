from brownie import Contract, accounts
from random import randint
import csv
with open('run8.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    step = 0 
    writer.writerow(["Step", "Comment", "Reserve SHQ", "Reserve USDC", "Distributor SHQ", "Distributor USDC", "MDO SHQ", "MDO USDC", "SHQ buyPrice", "SHQ sellPrice"])
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
    40 * 10**6 * 10**18,
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
    shq_amount = 5 * 10**6 * 10 ** 18

    distributor.setShq(sheqeltoken.address)
    sheqeltoken.setDistributor(distributor.address)
    reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : accounts[0]})
    sheqeltoken.transfer(reserve_contract.address, 35_000_000 * 10 ** 18, {'from' : accounts[0]})

    usdc.transfer(accounts[0], usdc_amount, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
    usdc.transfer(reserve_contract.address, 900 * 10**6, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
    print(step, "Everything is set up and no transactions have been made", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice())
    writer.writerow([step, "Everything is set up and no transactions have been made", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1


    # Adding liquidity to the pool
    uniswapRouter = Contract.from_explorer(spookyswapAddress)
    # Approving the transaction
    sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
    usdc.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})



    uniswapRouter.addLiquidity(
        sheqeltoken.address,
        usdc.address,
        shq_amount,
        10*10**6,
        0,
        0,
        accounts[0],
        1712933164 # Should be block.timestamp,
        , {"from": accounts[0]}

    )
    writer.writerow([step, "Added 10K usdc + 5M SHQ into liquidity", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1

    distributor.processAllRewards()
    sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")
    writer.writerow([step, "Distributed rewards", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1

    ####
    #sheqeltoken.transfer(accounts[3], 100_000 * 10 ** 18, {'from' : accounts[0]})
    #sheqeltoken.transfer(accounts[4], 100_000 * 10 ** 18, {'from' : accounts[0]})


    # Burning
    usdc.approve(reserve_contract.address, 100_000 * 10 ** 6, {'from' : accounts[0]})
    reserve_contract.buyShq(accounts[0], 1000 * 10**18, {'from' : accounts[0]})
    sheqeltoken.transfer("0x0000000000000000000000000000000000000000", 1000 * 10**18, {'from' : accounts[0]})
    writer.writerow([step, "Buying 1M SHQ to burn them (sending them to 0 address)", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1

    j = 1

    oldPrice = reserve_contract.buyPrice() # 183 at this point (0,000183 USDC)

    usdcBalanceStd = (usdc.balanceOf("0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})

    usdcBalanceStd = (usdc.balanceOf("0x083dee8e5ca1e100a9c9ec0744f461b3507e9376"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x083dee8e5ca1e100a9c9ec0744f461b3507e9376'})
        
    usdcBalanceStd = (usdc.balanceOf("0x12edea9cd262006cc3c4e77c90d2cd2dd4b1eb97"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x12edea9cd262006cc3c4e77c90d2cd2dd4b1eb97'})

    while sheqeltoken.balanceOf(reserve_contract.address) > 2_000_000 * 10**18:
        usdc.approve(reserve_contract.address, 100000000_000 * 10 ** 6, {'from' : accounts[j]})
        reserve_contract.buyShq(accounts[j], 1_000_000 * 10**18, {'from' : accounts[j]}) 
        writer.writerow([step, "Address " + str(accounts[j]) + "bought SHQ 1M", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
        step+=1

        if j < 8:
            j+=1
        else:
            j = 1

        if reserve_contract.buyPrice() < oldPrice:
            raise Exception("Price went down")
        
        oldPrice = reserve_contract.buyPrice()

    # Buying the last bit
    usdc.approve(reserve_contract.address, 100000000_000 * 10 ** 6, {'from' : accounts[1]})
    reserve_contract.buyShq(accounts[1], sheqeltoken.balanceOf(reserve_contract.address) - 200 * 10 ** 18, {'from' : accounts[1]}) 
    writer.writerow([step, "Address " + str(accounts[1]) + "bought all remaining SHQ", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1


    oldPrice = reserve_contract.buyPrice() # Price at this point : 4390 (0,004390 USDC)

    # Transactions between accounts
    for i in range(1, 9):
        randomAddress = randint(1, 8)
        sheqeltoken.transfer(accounts[randomAddress], 1 * 10**18, {'from' : accounts[i]})
        writer.writerow([step, "Address " + str(accounts[i]) + " sent 1M SHQ to " + str(accounts[randomAddress]), sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
        step+=1


    distributor.processAllRewards()
    sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")
    writer.writerow([step, "Distributed rewards", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1

    # Selling it all to the LP
    for x in range(1, 9):
        balance = sheqeltoken.balanceOf(accounts[x])
        path = [sheqeltoken.address, usdc.address]
        sheqeltoken.approve(uniswapRouter.address, balance, {'from' : accounts[x]})
        uniswapRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            balance,
            0,
            path,
            accounts[x],
            1712933164 + 90,
            {'from' : accounts[x]}
        )
        writer.writerow([step, "Address " + str(accounts[x]) + " swapped its whole SHQ balance to USDC ", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
        step+=1
    oldPrice = reserve_contract.buyPrice() # Price at this point : 4465 (0,004465 USDC)

    # Buying it back from the LP

    path = [usdc.address, sheqeltoken.address]
    for _ in range(1,15):
        usdc.approve(uniswapRouter.address, 10**6, {'from' : accounts[j]})
        tx=uniswapRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            10**6,
            0,
            path,
            accounts[j],
            1712933164 + 90,
            {'from' : accounts[j]}
        )
        writer.writerow([step, "Address " + str(accounts[x]) + " swapped its whole USDC balance to SHQ", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
        step+=1
        if j < 8:
            j+=1
        else:
            j = 1

    oldPrice = reserve_contract.buyPrice() # Price at this point : 4541 (0,004541 USDC)

    # Selling it all back to the Reserve
    for i in range(1, 9):
        shqBalance = sheqeltoken.balanceOf(accounts[i])

        sheqeltoken.approve(reserve_contract.address, shqBalance, {'from' : accounts[i]})
        reserve_contract.sellShq(accounts[i], shqBalance,{'from' : accounts[i]})

        if reserve_contract.buyPrice() < oldPrice:
            raise Exception("Price went down")

        oldPrice = reserve_contract.buyPrice() 
        writer.writerow([step, "Address " + str(accounts[i]) + " sold its whole SHQ balance to the reserve", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
        step+=1

    oldPrice = reserve_contract.buyPrice() # Price at this point : 4817 (0,004817 USDC)

    distributor.processAllRewards()
    sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")
    writer.writerow([step, "Distributed rewards", sheqeltoken.balanceOf(reserve_contract.address), usdc.balanceOf(reserve_contract.address), sheqeltoken.balanceOf(distributor.address), usdc.balanceOf(distributor.address), sheqeltoken.balanceOf(accounts[9]), usdc.balanceOf(accounts[9]), reserve_contract.buyPriceWithTax(), reserve_contract.sellPrice()])
    step+=1






    ########################################################### Second test #################################################################
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

    usdc_amount = 10_000 * 10 ** 6
    shq_amount = 5 * 10**6 * 10 ** 18

    distributor.setShq(sheqeltoken.address)
    sheqeltoken.setDistributor(distributor.address)
    reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : accounts[0]})

    usdc.transfer(accounts[0], usdc_amount, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
    usdc.transfer(reserve_contract.address, 900 * 10**6, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})

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
        10*10**6,
        0,
        0,
        accounts[0],
        1712933164 # Should be block.timestamp,
        , {"from": accounts[0]}

    )

    #tx=distributor.processAllRewards()
    sheqeltoken.balanceOf("0x3897810a334833184Ef7D6B419ba4d78EC2bBF80")

    ####
    #sheqeltoken.transfer(accounts[3], 100_000 * 10 ** 18, {'from' : accounts[0]})
    #sheqeltoken.transfer(accounts[4], 100_000 * 10 ** 18, {'from' : accounts[0]})


    # Burning
    usdc.approve(reserve_contract.address, 100_000 * 10 ** 6, {'from' : accounts[0]})
    reserve_contract.buyShq(accounts[0], 1000 * 10**18, {'from' : accounts[0]})
    sheqeltoken.transfer("0x0000000000000000000000000000000000000000", 1000 * 10**18, {'from' : accounts[0]})

    usdcBalanceStd = (usdc.balanceOf("0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})

    usdcBalanceStd = (usdc.balanceOf("0x083dee8e5ca1e100a9c9ec0744f461b3507e9376"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x083dee8e5ca1e100a9c9ec0744f461b3507e9376'})
        
    usdcBalanceStd = (usdc.balanceOf("0x12edea9cd262006cc3c4e77c90d2cd2dd4b1eb97"))/8

    for i in range(1,9):
        usdc.transfer(accounts[i], usdcBalanceStd, {'from' : '0x12edea9cd262006cc3c4e77c90d2cd2dd4b1eb97'})


    j = 1

    oldPrice = reserve_contract.buyPrice() # 183 at this point (0,000183 USDC)

    path = [usdc.address, sheqeltoken.address]
    for _ in range(1,15):
        usdc.approve(uniswapRouter.address, 10**6, {'from' : accounts[j]})
        tx=uniswapRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            10**6,
            0,
            path,
            accounts[j],
            1712933164 + 90,
            {'from' : accounts[j]}
        )
        if j < 8:
            j+=1
        else:
            j = 1
    oldPrice = reserve_contract.buyPrice() # Price at this point : 185 (0,000185 USDC)


    # Selling it all back to the Reserve
    for i in range(1, 9):
        shqBalance = sheqeltoken.balanceOf(accounts[i])

        sheqeltoken.approve(reserve_contract.address, shqBalance, {'from' : accounts[i]})
        reserve_contract.sellShq(accounts[i], shqBalance,{'from' : accounts[i]})

        if reserve_contract.buyPrice() < oldPrice:
            raise Exception("Price went down")

        oldPrice = reserve_contract.buyPrice() 

    oldPrice = reserve_contract.buyPrice() # Price at this point : 180 (0,000189 USDC)
