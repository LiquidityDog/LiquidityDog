from brownie import accounts, config, SheqelToken, Contract, Reserve, HolderRewarderDistributor
import pytest
from brownie.network.state import Chain
spookyswapAddress = "0xF491e7B69E4244ad4002BC14e878a34207E38c29"
usdc_address = "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75" 

@pytest.fixture(scope='module')
def owner():
    yield accounts[0]
@pytest.fixture(scope='module')
def usdc(): 
    usdc = Contract.from_explorer(usdc_address)
    yield usdc

@pytest.fixture(scope='module')
def reserve_contract(owner):
    yield Reserve.deploy(
    spookyswapAddress,
    usdc_address,
    {'from': accounts[0]},
    )
@pytest.fixture(scope='module')
def sheqeltoken(owner, reserve_contract):
    yield SheqelToken.deploy(
    reserve_contract.address,
    accounts[2],
    40 * 10**6 * 10**18,
    spookyswapAddress,
    usdc_address,
    {'from': accounts[0]},
    )

@pytest.fixture(scope='module')
def distributor(owner):
    yield HolderRewarderDistributor.deploy(
        spookyswapAddress,
        reserve_contract.address,
        accounts[0],
        40 * 10**6 * 10**18,
        usdc_address,
        {'from': accounts[0]},
    )

@pytest.fixture(autouse=True)
def setup(fn_isolation, sheqeltoken, reserve_contract, usdc):
    usdc_amount = 20_000_000 * 10 ** 6
    shq_amount = 10 * 10**6 * 10 ** 18

    reserve_contract.setSheqelTokenAddress(sheqeltoken.address, {'from' : accounts[0]})
    distributor.setShq(sheqeltoken.address)
    sheqeltoken.setDistributor(distributor.address)

    usdc.transfer(accounts[0], usdc_amount, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})
    usdc.transfer(reserve_contract.address, 5000000, {'from' : '0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605'})

    # Adding liquidity to the pool
    uniswapRouter = Contract.from_explorer(spookyswapAddress)
    # Approving the transaction
    sheqeltoken.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
    usdc.approve(spookyswapAddress, shq_amount, {"from": accounts[0]})
    sheqeltoken.transfer(reserve_contract.address, 100_000 * 10 ** 18, {'from' : accounts[0]})


    uniswapRouter.addLiquidity(
        sheqeltoken.address,
        usdc_address,
        shq_amount,
        usdc_amount,
        0,
        0,
        accounts[0],
        1712933164 # Should be block.timestamp,
        , {"from": accounts[0]}

    )


'''
    uniswapRouter.addLiquidityETH(
        sheqeltoken.address,
        shq_amount,
        0,
        0,
        accounts[0],
        1712933164,
        {"from": accounts[0], "value": 10 * 10**18}
    )'''

