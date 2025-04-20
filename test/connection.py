from web3 import Web3

# Connect to your Ganache instance
ganache_url = "http://127.0.0.1:8545"  # Change if using a different port
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verify connection
if web3.is_connected():
    print("✅ Successfully connected to the Blockchain!")
else:
    print("❌ Connection to Blockchain failed!")

# Fetch latest block number
print("🔗 Latest Block Number:", web3.eth.block_number)
