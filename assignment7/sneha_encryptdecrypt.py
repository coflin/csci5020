#!/usr/bin/python
"""
Assignment 7: Encrypts or Decrypts a file. Take a key, encrypted file or decrypted file as an optional parameter.
The default key file would be key.key unless specified.
"""
import argparse
import cryptography.fernet as fernet
import os


def save_key(key, key_file):
    try:
        with open(key_file, "wb") as file:
            file.write(key)
    except Exception as e:
        print(f"Error saving key to {key_file}: {str(e)}")


def load_key(key_file):
    try:
        with open(key_file, "rb") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading key from {key_file}: {str(e)}")


def encrypt_file(input_file, output_file, key_file):
    key = fernet.Fernet.generate_key()
    save_key(key, key_file)
    f = fernet.Fernet(key)

    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        data = infile.read()
        encrypted_data = f.encrypt(data)
        outfile.write(encrypted_data)


def decrypt_file(input_file, output_file, key_file):
    key = load_key(key_file)
    f = fernet.Fernet(key)

    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        encrypted_data = infile.read()
        decrypted_data = f.decrypt(encrypted_data)
        outfile.write(decrypted_data)


def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt text files.")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt the input file")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt the input file")
    parser.add_argument(
        "--key_file", default="key.key", help="Key file path (default: key.key)"
    )

    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.input_file, args.output_file, args.key_file)
        print(
            f"'{args.input_file}' has been encrypted and saved to '{args.output_file}' with key saved to '{args.key_file}'."
        )

    if args.decrypt:
        try:
            decrypt_file(args.input_file, args.output_file, args.key_file)
            print(
                f"'{args.input_file}' file has been decrypted and saved to '{args.output_file}'."
            )
        except Exception as e:
            print(
                f"Problem decrypting the file. It might be because the key file was not found. Please check and try again: {e}"
            )


if __name__ == "__main__":
    main()
