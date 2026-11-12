"""Deploy the adjacent Remix FoodHandoff.json artifact to local Ganache."""
import json
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

RPC_URL = "http://127.0.0.1:7545"


def rpc(method, params):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    request = Request(RPC_URL, data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=10) as response:
        reply = json.load(response)
    if "error" in reply:
        raise RuntimeError(f"{method}: {reply['error']['message']}")
    return reply["result"]


def load_bytecode():
    path = Path(__file__).with_name("FoodHandoff.json")
    artifact = json.loads(path.read_text(encoding="utf-8-sig"))
    for section in (artifact.get("data", {}), artifact.get("evm", {}), artifact):
        code = section.get("bytecode", "")
        if isinstance(code, dict):
            code = code.get("object", "")
        if code and code != "0x":
            raw = bytes.fromhex(code.removeprefix("0x"))
            if raw:
                return "0x" + raw.hex()
    raise ValueError("No deployment bytecode in FoodHandoff.json. Use the compiled Remix artifact.")


def main():
    bytecode = load_bytecode()
    accounts = rpc("eth_accounts", [])
    if not accounts:
        raise RuntimeError("Ganache returned no test accounts.")
    transaction = {"from": accounts[0], "data": bytecode}
    transaction["gas"] = rpc("eth_estimateGas", [transaction])
    tx_hash = rpc("eth_sendTransaction", [transaction])
    print("Deployment transaction:", tx_hash)
    for _ in range(60):
        receipt = rpc("eth_getTransactionReceipt", [tx_hash])
        if receipt:
            address = receipt.get("contractAddress")
            if receipt.get("status") != "0x1" or not address:
                raise RuntimeError("Deployment failed. Inspect the transaction in Ganache.")
            if rpc("eth_getCode", [address, "latest"]) in ("0x", "0x0"):
                raise RuntimeError("No contract code was found at the new address.")
            print("Contract address:", address)
            return
        time.sleep(1)
    raise RuntimeError("Still awaiting a receipt. Check the printed transaction in Ganache.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, URLError, ValueError, RuntimeError) as error:
        sys.exit(str(error))
