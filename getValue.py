from web3 import Web3
import requests
import json
ethProvider = "ADD_NODE"
arbProvider = "ADD_NODE"
avaxProvider = "ADD_NODE"
web3eth = Web3(Web3.HTTPProvider(ethProvider))
web3arb = Web3(Web3.HTTPProvider(arbProvider))
web3avax = Web3(Web3.HTTPProvider(avaxProvider))
cmcKey = "bce70376-013b-471f-8b42-359ef481b0b7"
ethplorerKey = ""

minABI = [
  {
    "constant": True,
    "inputs": [{ "name": "_owner", "type": "address" }],
    "name": "balanceOf",
    "outputs": [{ "name": "balance", "type": "uint256" }],
    "type": "function",
  }
]

minABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_maxTxAmount","type":"uint256"}],"name":"MaxTxAmountUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"notbot","type":"address"}],"name":"delBot","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"manualsend","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"manualswap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"openTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"removeStrictTxLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"bots_","type":"address[]"}],"name":"setBots","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"onoff","type":"bool"}],"name":"setCooldownEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'


def getBalances(poolAddress, lpAddress, chainID,tokenAddresses):
    decimals = 1
    poolSize = 0
    #data = {'name': ["X", "Y", 'Z']}
    #df = pd.DataFrame(data=data, index=[0, 1, 2])
    web3 = ""
    if chainID == "eth":
        web3 = web3eth
    elif chainID == "arb":
        web3 = web3arb
    elif chainID == "avax":
        web3 = web3avax
    else:
        print("Not a valid Chain ID")
        return False
    slices = {}
    for token in tokenAddresses:
        contract = web3.eth.contract(address = token, abi = minABI)
        slices[token] = contract.functions.balanceOf(poolAddress).call()
        decimals = contract.functions.decimals().call()
        slices[token] /= 10**decimals
        poolSize += slices[token]
    #for slice in slices:
    #    print(slice + " slice: " + str(slices[slice]/poolSize*100) + "%")
    for slice in slices:
        slices[slice] /= poolSize
    lpAddress = web3.toChecksumAddress(lpAddress)
    lpCon = web3.eth.contract(address = lpAddress, abi = minABI)
    lpSupply = lpCon.functions.totalSupply().call()/10**lpCon.functions.decimals().call()
    #print("lp total supply: " + str(lpSupply))
    return slices, lpSupply, poolSize

def get_price_data(crypto):
    response = requests.get(f"https://api.coinmarketcap.com/v1/ticker/{crypto}/")
    data = json.loads(response.text)
    return data["price_usd"]

def get_price_dataEthplorer(address):
    # Use the requests module to make an API call to get the current price data
    response = requests.get(f"https://api.ethplorer.io/getTokenInfo/{address}?apiKey=MY_API_KEY")
    data = json.loads(response.text)
    print(data)
    return data["price"]["rate"]


def getValue(slices, lpSupply, poolSize):
    value = 0

    for slice in slices:
        unitVal = get_price_dataEthplorer(slice)
        value  += unitVal * slices[slice] * poolSize

    value /= lpSupply
    return value

slices, lpSupply, poolSize = getBalances("0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", "eth", ["0xdAC17F958D2ee523a2206206994597C13D831ec7","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0x6B175474E89094C44Da98b954EedeAC495271d0F"])
print("Slices: ", slices, "LP Supply: ", lpSupply, "Pool Size: ", poolSize)
print("Value of 1 LP: ", getValue(slices,lpSupply, poolSize))
