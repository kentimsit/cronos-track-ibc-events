import requests
import pprint
import bech32

# Get all IBC transactions
# For example, look for a transaction originating from Cronos chain

print("\n**Get all IBC transactions**")
page_number = 86000
tx_found = False
example_tx = {}

while not tx_found:
    api_response = requests.request(
        method="get",
        url="https://cronos.org/indexing/api/v1/bridges/activities",
        params={
            'page': page_number
        }
    )
    for tx in api_response.json()['result']:
        if tx['sourceChain'] == "Cronos":
            example_tx = tx
            tx_found = True
            break
    page_number += 1

print("**Example of IBC transaction, originating from Cronos**")
pprint.pprint(example_tx)
print("Pagination data")
pprint.pprint(api_response.json()['pagination'])

# Get IBC transactions associated with a specific network and address

print("\n**Get IBC transactions associated with a specific network and address**")
network = "cronos"
account = example_tx['sourceAddress']

page_number = 1
tx_found = False
example_tx_2 = {}

while not tx_found:
    api_response = requests.request(
        method="get",
        url="https://cronos.org/indexing/api/v1/bridges/" + network + "/account/" + account + "/activities",
            params={
            'page': page_number
        }
    )
    for tx in api_response.json()['result']:
        if tx['sourceTransactionId'] == tx['sourceTransactionId']:
            example_tx_2 = tx
            tx_found = True
            break
    page_number += 1

# Confirm that we have found the transaction
print("Found transaction", tx['sourceTransactionId'])
print("Pagination data")
pprint.pprint(api_response.json()['pagination'])


# Get IBC transaction by transaction hash
print("\n**Get IBC transaction by transaction hash**")

tx_hash = example_tx['sourceTransactionId']

api_response = requests.request(
    method="get",
    url="https://cronos.org/indexing/api/v1/bridges/txs/" + tx_hash,
)

pprint.pprint(api_response.json())

# Convert Cronos EVM address into Cosmos address and vice versa
print("\n**Convert Cronos EVM address into Cosmos address and vice versa**")

print("\nFrom Cosmos address to EVM address")
# Cosmos (Bech32) address
bech32_address = example_tx['sourceAddress']
print("Input: Cosmos address", bech32_address)

_, bz = bech32.bech32_decode(bech32_address)
hexbytes=bytes(bech32.convertbits(bz, 5, 8))
eth_address = '0x' + hexbytes.hex()
print("Output: EVM address is",eth_address)

print("\nFrom EVM address to Cosmos address")
# EVM address
print("Input: EVM address", eth_address)
eth_address_bytes = bytes.fromhex(eth_address[2:])

print("EVM address length: ", len(eth_address_bytes))
print("EVM address: ", eth_address_bytes.hex())
bz = bech32.convertbits(eth_address_bytes, 8, 5)
new_bech32_address = bech32.bech32_encode("crc",bz)
print("Output: Cosmos address", new_bech32_address)