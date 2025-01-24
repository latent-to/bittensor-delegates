import json

from bittensor import Keypair

name = input("Your validator's descriptive name (e.g. Opentensor Foundation):\n")
url = input("Your validator url (e.g. www.opentensor.org ) [Optional]:\n")
description = input(
    "A short description for your validator ( e.g. Build, maintain and advance Bittensor):\n"
)

CK = "5EHVUNEqz1js5LdnW56hFpqKAV2pEGa7GCA2z6r7GVdLyTZE"
keypair = Keypair(ss58_address=CK)

delegates_entry = dict()
delegates_entry[keypair.ss58_address] = {
    "name": name,
    "url": url,
    "description": description,
}

message = json.dumps(delegates_entry)
print(message)
signed = False
while not signed:
    signature = input("Enter your signature: ")
    if signature == "":
        print("Signature cannot be empty")
        continue
    signed = keypair.verify(message, signature)
    if not signed:
        print("Signature is invalid")
        continue
print("Signature is valid!!")

delegates_entry[keypair.ss58_address]["signature"] = signature

print(f"Adding entry: {delegates_entry}")
with open("public/delegates.json", "r") as fh:
    delegates = json.loads(fh.read())

delegates.update(delegates_entry)

with open("public/delegates.json", "w") as fh:
    # Dump with 4 indent and do not escape non-ascii characters
    fh.write(json.dumps(delegates, indent=4, ensure_ascii=False))
print(
    "Success. Submit these changes as PR at https://github.com/opentensor/bittensor-delegates"
)
