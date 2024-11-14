"""Code Example for TPMDecrypter"""

from hashlib import sha256

from tpm.tpm_decrypter import TPMDecrypter

# TPMDecrypter
TPM_ADDRESS = ""  # TPM Address, ex: "0x81000000"
ENCRYPTED_FILE = ""  # Encrypted file path, ex: "./encrypted_file.enc"


def file_decrypt():
    """Model decrypt Example"""
    decrypter = TPMDecrypter()
    key = decrypter.unseal_key(TPM_ADDRESS)
    decrypted_data = decrypter.decrypt_file_aes_256_cbc(key, ENCRYPTED_FILE)
    del key

    sha256_checksum = sha256(decrypted_data).hexdigest()
    print(f"SHA-256 checksum of decrypted data: {sha256_checksum}")


if __name__ == "__main__":
    file_decrypt()
