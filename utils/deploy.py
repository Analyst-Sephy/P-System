import json
import os
from web3 import Web3
from solcx import compile_source, install_solc

# ✅ 1. Install Solidity Compiler ======================================
try:
    install_solc('0.8.20')
except Exception as e:
    print(f"🚨 Error installing Solidity compiler: {e}")
    exit(1)

# ✅ 2. Connect to Ethereum (Ganache or Infura) =======================
RPC_URL = 'http://127.0.0.1:7545'  # Update if using Infura or Alchemy

try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError("🚨 Not connected to Ethereum! Is Ganache running?")
except Exception as e:
    print(f"🚨 Web3 connection error: {e}")
    exit(1)

# ✅ 3. Load Solidity Contract =========================================
contract_path = os.path.join(os.path.dirname(__file__), "../contracts/contracts.sol")

if not os.path.exists(contract_path):
    print(f"🚨 Solidity contract file not found: {contract_path}")
    exit(1)

with open(contract_path, 'r') as f:
    contract_source = f.read()

# ✅ 4. Compile Contract ==============================================
try:
    compiled = compile_source(
        contract_source,
        output_values=["abi", "bin"],
        solc_version="0.8.20"
    )
except Exception as e:
    print(f"🚨 Compilation error: {e}")
    exit(1)

# Debug: Print compiled contract keys
print("🔍 Compiled contracts:", list(compiled.keys()))

# ✅ 5. Extract ABI & Bytecode ========================================
contract_name = list(compiled.keys())[0]  # Automatically fetch first contract
contract_interface = compiled[contract_name]

abi = contract_interface.get("abi", [])
bytecode = contract_interface.get("bin", "")

if not abi or not bytecode:
    print("🚨 ABI or Bytecode extraction failed!")
    exit(1)

print(f"✅ ABI & Bytecode extracted! ABI Length: {len(abi)}, Bytecode Length: {len(bytecode)}")

# ✅ 6. Deploy Contract ===============================================
try:
    account = w3.eth.accounts[0]  # Use first account in Ganache
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    gas_estimate = Contract.constructor().estimate_gas()
    print(f"⛽ Estimated Gas: {gas_estimate}")
    
    tx_hash = Contract.constructor().transact({
        "from": account,
        "gas": gas_estimate + 100000  # Buffer to avoid underpricing
    })
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"🚀 Contract deployed at: {contract_address}")
except Exception as e:
    print(f"🚨 Contract deployment failed: {e}")
    exit(1)

# ✅ 7. Save Contract Details ==========================================
output_path = os.path.join(os.path.dirname(__file__), "../static/contract_info.json")

try:
    with open(output_path, 'w') as f:
        json.dump({
            "address": contract_address,
            "abi": abi
        }, f, indent=2)
    print(f"✅ Contract info saved to {output_path}")
except Exception as e:
    print(f"🚨 Error saving contract info: {e}")
    exit(1)

# ✅ 8. Final Summary ================================================
print(f"""
🎉 SUCCESS!
🔹 Contract Address: {contract_address}
🔹 ABI Length: {len(abi)}
🔹 Bytecode: {bytecode[:10]}...{bytecode[-10:]} (trimmed)
""")
