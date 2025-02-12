from argparse import ArgumentParser

from mnemonic import Mnemonic

from .derive import Secret, derive_seed_from_secret, derive_bytes_from_path


def cli_main():
    # Read CLI
    parser = ArgumentParser()
    
    cmd_subparsers = parser.add_subparsers(dest="command", required=True)

    cmd_subparsers.add_parser("generate")

    derive_parser = cmd_subparsers.add_parser("derive")
    derive_parser.add_argument("path", help="Derivation path", type=str)
    derive_parser.add_argument("length", help="Length", type=int)
    derive_parser.add_argument("output", help="Output", type=str)

    args = parser.parse_args()

    if args.command == "generate":
        generate()
    else:
        derive(args)


def generate():
    mnemonic = Mnemonic()
    print(mnemonic.generate())


def derive(args):
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
