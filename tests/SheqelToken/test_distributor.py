from brownie import accounts, Contract


def test_distribution(sheqeltoken):
    sheqeltoken.transfer(accounts[3], 10**16 * 10 ** 18, {'from' : accounts[0]})

    distributor = Contract(sheqeltoken.getDistributor())
    distributor.processAllRewards()