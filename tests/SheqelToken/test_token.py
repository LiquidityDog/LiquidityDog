from brownie.test import given, strategy
from brownie import accounts, reverts, Contract
import pytest
import time

transferedAmount = 10 * 10**18
reserve = 197/10000
rewards = 267 / 10000
mdo = 75 / 10000
ubr = 86 / 10000
liquidity = 75 / 10000

def test_transaction(sheqeltoken, reserve_contract, usdc, accounts):
    distributor_address = sheqeltoken.getDistributor()
    assert sheqeltoken.balanceOf(accounts[3]) == 0 # Verifiy reciepend doesnt have any SHQ
    assert usdc.balanceOf(reserve_contract.address) == 0 # Verify reserve don't have any USDC
    assert sheqeltoken.balanceOf(distributor_address) == 0 # Verify the rewards distributor don't have any SHQ


    beforeTransferBalanceAccounts0 = sheqeltoken.balanceOf(accounts[0])
    beforeTransferBalanceAccountsReserve = sheqeltoken.balanceOf(reserve_contract.address)


    sheqeltoken.transfer(accounts[3], transferedAmount, {'from' : accounts[0]})
    print("hemmp")
    
    assert sheqeltoken.balanceOf(accounts[0]) == beforeTransferBalanceAccounts0 - transferedAmount # Verify recipiend has recieved taxed SHQ
    assert sheqeltoken.balanceOf(accounts[3]) == transferedAmount - (transferedAmount*(reserve + rewards + mdo + ubr + liquidity))

    assert usdc.balanceOf(reserve_contract.address) > 0
    assert sheqeltoken.balanceOf(distributor_address) > 0


def test_sending_nulladdress(sheqeltoken, reserve_contract, usdc, accounts):
    sheqeltoken.transfer("0x0000000000000000000000000000000000000000", 100_000, {'from' : accounts[0]})
    assert sheqeltoken.balanceOf("0x0000000000000000000000000000000000000000") == 100_000







    


