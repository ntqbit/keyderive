from argparse import ArgumentParser

from mnemonic import Mnemonic

from .derive import Secret, derive_seed_from_secret, derive_bytes_from_path

# Read CLI
parser = ArgumentParser()
parser.add_argument("path", help="Derivation path", type=str)
parser.add_argument("length", help="Length", type=int)
parser.add_argument("output", help="Output", type=str)
args = parser.parse_args()

path = args.path.split("/")

phrase = input("Input mnemonic phrase: ")

# Derive seed
mnemonic = Mnemonic()
secret = Secret(mnemonic.to_entropy(phrase))
seed = derive_seed_from_secret(secret)

# Generate bytes
result = derive_bytes_from_path(seed, path, args.length)

# Write result to the output
with open(args.output, "wb") as f:
    f.write(result)
