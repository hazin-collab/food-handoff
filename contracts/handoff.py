"""Interact with FoodHandoff on local Ganache using its unlocked test accounts."""
import argparse
import sys
import time

from deploy_food_handoff import rpc

STATES = ("Registered", "Dispatched", "Received")


def calldata(signature, batch_id, retailer=None):
    # All four contract functions take a UTF-8 string as their first argument.
    selector = rpc("web3_sha3", ["0x" + signature.encode().hex()])[:10]
    encoded_id = batch_id.encode()
    head = (64 if retailer else 32).to_bytes(32, "big")
    if retailer:
        head += bytes.fromhex(retailer[2:]).rjust(32, b"\x00")
    tail = len(encoded_id).to_bytes(32, "big") + encoded_id
    tail += bytes((-len(encoded_id)) % 32)
    return selector + (head + tail).hex()


def show_batch(address, batch_id):
    data = calldata("getBatch(string)", batch_id)
    result = rpc("eth_call", [{"to": address, "data": data}, "latest"])
    words = bytes.fromhex(result[2:])
    if len(words) != 96:
        raise ValueError("Unexpected lookup response. Check the contract address.")
    status = int.from_bytes(words[64:], "big")
    if status >= len(STATES):
        raise ValueError("Unknown batch status.")
    print("Supplier:", "0x" + words[12:32].hex())
    print("Retailer:", "0x" + words[44:64].hex())
    print(f"{batch_id}: {STATES[status]} (status {status})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["register", "dispatch", "receive", "lookup"])
    parser.add_argument("address", help="deployed FoodHandoff address")
    parser.add_argument("batch", help="batch ID, for example B-104")
    args = parser.parse_args()
    if rpc("eth_getCode", [args.address, "latest"]) in ("0x", "0x0"):
        raise ValueError("No contract at this address on the current Ganache chain.")
    if args.action != "lookup":
        accounts = rpc("eth_accounts", [])
        if len(accounts) < 2:
            raise ValueError("Two Ganache test accounts are required.")
        supplier, retailer = accounts[:2]
        if args.action == "register":
            data = calldata("registerBatch(string,address)", args.batch, retailer)
        elif args.action == "dispatch":
            data = calldata("dispatchBatch(string)", args.batch)
        else:
            data = calldata("confirmReceipt(string)", args.batch)
        sender = retailer if args.action == "receive" else supplier
        tx = {"from": sender, "to": args.address, "data": data}
        tx["gas"] = rpc("eth_estimateGas", [tx])
        tx_hash = rpc("eth_sendTransaction", [tx])
        print("Transaction:", tx_hash)
        for _ in range(60):
            receipt = rpc("eth_getTransactionReceipt", [tx_hash])
            if receipt:
                if receipt["status"] != "0x1":
                    raise RuntimeError("Transaction reverted.")
                break
            time.sleep(1)
        else:
            raise RuntimeError("Receipt pending. Check the transaction in Ganache.")
    show_batch(args.address, args.batch)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        sys.exit(str(error))
