const Web3 = require("web3");

const provider =
  "" //node provider here

const Web3Client = new Web3(new Web3.providers.HttpProvider(provider));

const minABI = [
  {
    constant: true,
    inputs: [{ name: "_owner", type: "address" }],
    name: "balanceOf",
    outputs: [{ name: "balance", type: "uint256" }],
    type: "function",
  },
];
const tether = "0xdAC17F958D2ee523a2206206994597C13D831ec7";
const usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F";
const walletAddress = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7";
const wallet = "0xee5b5b923ffce93a870b3104b7ca09c3db80047a";


const tetherCon = new Web3Client.eth.Contract(minABI, tether);
const daiCon = new Web3Client.eth.Contract(minABI, dai);
const USDCCon = new Web3Client.eth.Contract(minABI, usdc);
async function getBalances() {
  const tethSlice = await tetherCon.methods.balanceOf(walletAddress).call()/10**6;
  const daiSlice = await daiCon.methods.balanceOf(walletAddress).call()/10**18;
  const USDCSlice = await USDCCon.methods.balanceOf(walletAddress).call()/10**6;
  const poolSize = tethSlice + daiSlice + USDCSlice;
  console.log("Tether share: " + tethSlice/poolSize*100 + "%")
  console.log("Dai Share: " + daiSlice/poolSize*100 + "%");
  console.log("USDC Share: " + USDCSlice/poolSize*100 + "%");
}

getBalances();
