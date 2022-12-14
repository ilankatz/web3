from web3 import Web3
import json
provider = "" #node provider here
web3 = Web3(Web3.HTTPProvider(provider))


minABI = [
  {
    "constant": True,
    "inputs": [{ "name": "_owner", "type": "address" }],
    "name": "balanceOf",
    "outputs": [{ "name": "balance", "type": "uint256" }],
    "type": "function",
  }
]

tether = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
3poolAddress = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"

tetherCon = web3.eth.contract(address = tether, abi = minABI)
daiCon = web3.eth.contract(address = dai, abi = minABI)
usdcCon = web3.eth.contract(address = usdc, abi = minABI)
def getBalances():
    tethSlice = tetherCon.functions.balanceOf(3poolAddress).call()
    daiSlice = daiCon.functions.balanceOf(3poolAddress).call()
    usdcSlice = usdcCon.functions.balanceOf(3poolAddress).call()
    tethForm = tethSlice/10**6
    daiForm = daiSlice/10**18
    usdcForm = usdcSlice/10**6
    poolSize = tethForm + daiForm + usdcForm
    print("Tether share: " + str(tethForm/poolSize*100) + "%")
    print("Dai Share: " + str(daiForm/poolSize*100) + "%")
    print("USDC Share: " + str(usdcForm/poolSize*100) + "%")

getBalances()
