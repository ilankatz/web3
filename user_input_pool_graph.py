from web3 import Web3
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

class Token:
    def __init__(self, name, address, decimals, contract):
        self.name = name
        self.address = address
        self.decimals = decimals
        self.contract = contract

tokens = {}
pool = ""

def initTokens():
    global tokens
    name = "init"
    index = 1
    while name != "":
        name = input("Token " + str(index) + " name: ")
        if name == "":
            break
        address = input("Token " + str(index) + " address: ")
        decimals = int(input("Token " + str(index) + " decimals: "))
        contract = web3.eth.contract(address = address, abi = minABI)
        t = Token(name, address, decimals, contract)
        tokens[t.name] = t
        index += 1
def initPool():
    global pool
    pool = input("Pool address: ")
def getSlices():
    poolSize = 0
    slices = {}
    for token in tokens:
        size = (tokens[token].contract).functions.balanceOf(pool).call()
        size /= 10**tokens[token].decimals
        poolSize += size
        slices[tokens[token].name] = size
    for slice in slices:
        print(slice + ": " + str(slices[slice]/poolSize*100) + "%")
