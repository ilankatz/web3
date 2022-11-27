# web3

The goal here is to make a tool that can make it easy to get block-by-block data on liquidity pools and all open positions.
Steps:

1. Get data from a pool given pool and token addresses and names
2. Get data from a pool with user inputted data
3. Get data from a list of pools from a .csv file
4. Get data from a pool given an LP token
5. Get data from all pools in which a wallet has LPs given the wallet address
6. Constantly update data from (5) and emit events on certain triggers
7. Store all that data and make it constantly accessible
