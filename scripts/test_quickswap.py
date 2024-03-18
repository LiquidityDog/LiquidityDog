quickswapAddress = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
usdcAddress = '0x4BC9651557F39c9B8fA262f024EaFcd0706580A9'
shqAddress = '0x6bf2f7CFFddCF0197EDEFbeec8B8f3C4EAB1Ec90'
acct = accounts.load('shqdeployer')
deadline = 9999999999  # Set a high deadline for the swap

usdc = Contract(usdcAddress)
shq = Contract(shqAddress)
quickswap = Contract(quickswapAddress)

usdc_amount = 10*10**6
shq_amount = 986 * 10**18
# Use uniswapV2 (quickswap to swap 10 USDC to SHQ)
# Approve QuickSwap to spend USDC tokens
usdc.approve(quickswapAddress, usdc_amount, {'from': acct})
path = [usdcAddress, shqAddress]
amounts = quickswap.getAmountsOut(usdc_amount, path)
min_shq_amount = amounts[-1] - (amounts[-1] // 10)  # 10% slippage tolerance
quickswap.swapExactTokensForTokens(
    usdc_amount,
    min_shq_amount,
    path,
    acct,
    deadline,
    {'from': acct}
)
########################################################################################################

quickswapAddress = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
usdcAddress = '0x4BC9651557F39c9B8fA262f024EaFcd0706580A9'
shqAddress = '0x6bf2f7CFFddCF0197EDEFbeec8B8f3C4EAB1Ec90'
acct = accounts.load('shqdeployer')
deadline = 9999999999  # Set a high deadline for the swap

usdc = Contract(usdcAddress)
shq = Contract(shqAddress)
quickswap = Contract(quickswapAddress)

usdc_amount = 10 * 10**6
shq_amount = 2000 * 10**18  # Updated SHQ amount

# Use QuickSwap to swap USDC to SHQ
# Approve QuickSwap to spend USDC tokens
usdc.approve(quickswapAddress, usdc_amount, {'from': acct})
path = [usdcAddress, shqAddress]
amounts = quickswap.getAmountsOut(usdc_amount, path)
min_shq_amount = shq_amount - (shq_amount // 10)  # 10% slippage tolerance

quickswap.swapExactTokensForTokens(
    usdc_amount,
    min_shq_amount,
    path,
    acct,
    deadline,
    {'from': acct}
)

