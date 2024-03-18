from brownie.test import given, strategy
from brownie import accounts, reverts, Contract


def test_reserve_price(accounts, usdc, reserve_contract, sheqeltoken):
    pass
    '''usdc.transfer(reserve_contract.address, 4_000_000 * 10 ** 6, {'from' : '0x072f35Cfa85Af2793348cCC0eaA0E16E898946a8'})
    sheqeltoken.transfer(reserve_contract.address, 4_000_000 * 10 ** 18, {'from' : accounts[0]})
    #reserve_contract.sellPrice().call_trace()
    print(sheqeltoken.totalSupply())'''