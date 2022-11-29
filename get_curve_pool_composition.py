from web3 import Web3
import streamlit as st
import json
provider = "https://mainnet.infura.io/v3/062cdeab4e804758a8a87ebc1dc8a2b2" #node provider here
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

threepoolAddress = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"

tetherCon = web3.eth.contract(address = tether, abi = minABI)
daiCon = web3.eth.contract(address = dai, abi = minABI)
usdcCon = web3.eth.contract(address = usdc, abi = minABI)
def getBalances():
    tethSlice = tetherCon.functions.balanceOf(threepoolAddress).call()
    daiSlice = daiCon.functions.balanceOf(threepoolAddress).call()
    usdcSlice = usdcCon.functions.balanceOf(threepoolAddress).call()
    tethForm = tethSlice/10**6
    daiForm = daiSlice/10**18
    usdcForm = usdcSlice/10**6
    poolSize = tethForm + daiForm + usdcForm
    st.write("Tether share: " + str(tethForm/poolSize*100) + "%")
    st.write("Dai Share: " + str(daiForm/poolSize*100) + "%")
    st.write("USDC Share: " + str(usdcForm/poolSize*100) + "%")

getBalances()
