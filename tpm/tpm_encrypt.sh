#!/usr/bin/bash
# This script encrypts a given file using AES-256 encryption and secures the encryption key using a TPM (Trusted Platform Module).
# Usage: ./model_encrypt.sh <file> <tpm_address>
#
# Arguments:
#   file - The file to be encrypted.
#   tpm_address - The address of the TPM to be used.
#
# Steps:
# 1. Generate a 256-bit AES key and save it to key.bin.
# 2. Encrypt the input file using the generated AES key and save the encrypted file with a .enc extension.
# 3. Create a Primary Key in the TPM.
# 4. Create a Sealing Object to seal the AES key.
# 5. Load the sealed key object into the TPM.
# 6. Make the sealed key persistent in the TPM.
# 7. Display the persistent handles in the TPM.
# 8. Securely delete the AES key, the original file, and intermediate files using the shred command.

function show_help() {
    echo "Usage: ./model_encrypt.sh <file> <tpm_address>"
    echo "Arguments:"
    echo "  file - The file to be encrypted."
    echo "  tpm_address - The address of the TPM to be used."
    echo "Example: ./model_encrypt.sh secret.txt 0x810F2A89"
    echo "Note: The TPM address should be in the range from 0x81000000 to 0x81FFFFFF."
}

# Check for help flag
if [[ $1 == "-h" || $1 == "--help" ]]; then
    show_help
    exit 0
fi

# Check if file argument is provided
if [[ -z $1 ]]; then
    echo "Error: No file provided."
    show_help
    exit 1
fi
if [[ -z $2 ]]; then
    echo "Error: No TPM address provided, range from 0x81000000 to 0x81FFFFFF, e.g. 0x810F2A89."
    show_help
    exit 1
fi

file=$1
file_enc=${file}.enc
tpm_address=$2
set -x
# Generate a 128-bit AES key and save it to key.bin
openssl rand -out key.bin 32
# Encrypt file using the generated AES key
openssl enc -aes-256-cbc -in ${file} -out ${file_enc} -pass file:./key.bin -pbkdf2 -iter 10000
# Create a Primary Key in TPM
sudo tpm2_createprimary -C o -g sha256 -G rsa -c primary.ctx
# Create a Sealing Object
sudo tpm2_create -C primary.ctx -u seal.pub -r seal.priv -i key.bin
# Load the sealed key object into the TPM
sudo tpm2_load -C primary.ctx -u seal.pub -r seal.priv -c seal.ctx
# Make the sealed key persistent in the TPM
sudo tpm2_evictcontrol -C o -c seal.ctx 0x810F2A89
# Show persistent handles
sudo tpm2_getcap handles-persistent
# Remove the not-needed files
sudo shred -vzun 10 key.bin ${file} seal.pub seal.priv primary.ctx seal.ctx
