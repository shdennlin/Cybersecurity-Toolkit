"""TPM Decrypter module to decrypt files using TPM2.0"""
import os
import secrets
import subprocess
import tempfile


def secure_delete(file_path, passes=10):
    """Overwrite the file with random data multiple times and delete it."""
    with open(file_path, "ba+", buffering=0) as f:
        length = f.tell()  # Get the file size
        for _ in range(passes):
            f.seek(0)
            f.write(secrets.token_bytes(length))  # Overwrite with random bytes
            f.flush()
            os.fsync(f.fileno())  # Ensure changes are written to disk
    os.remove(file_path)  # Delete the file


class TPMDecrypter:
    """TPM Decrypter class to decrypt files using TPM2.0"""

    def unseal_key(self, tpm_address) -> bytes:
        """
        Unseals a key from the TPM (Trusted Platform Module) using the provided TPM address.

        Args:
            tpm_address (str): The address of the TPM from which to unseal the key.

        Returns:
            bytes: The unsealed key.

        Raises:
            ValueError: If the unsealed key size is not 16, 24, or 32 bytes.
            RuntimeError: If the TPM unsealing process fails.
        """
        try:
            result = subprocess.run(
                ['tpm2_unseal', '-c', tpm_address],
                check=True,
                capture_output=True,
                text=False
            )
            key = result.stdout.strip()
            if len(key) not in (16, 24, 32):
                raise ValueError(f"Invalid key size ({len(key)}) for AES. Key must be 16, 24, or 32 bytes.")
            print("Key unsealed successfully from TPM.")
            return key
        except subprocess.CalledProcessError as e:
            print("Error during tpm2_unseal:", e.stderr)
            raise RuntimeError("Failed to unseal the key from TPM") from e

    def decrypt_file_aes_256_cbc(self, key: bytes, encrypted_file_path: str) -> bytes:
        """
        Decrypts an encrypted file using AES-256-CBC mode with a provided key.

        Args:
            key (bytes): The encryption key used for decryption.
            encrypted_file_path (str): The path to the encrypted file.

        Returns:
            bytes: The decrypted data.

        Raises:
            RuntimeError: If decryption fails due to an error in the OpenSSL command.
        """
        temp_key_file_path: str = ""
        decrypted_data: bytes = b""
        try:
            # Create a temporary file for the key
            with tempfile.NamedTemporaryFile(delete=False) as temp_key_file:
                temp_key_file.write(key)
                temp_key_file_path = temp_key_file.name

            # Construct the OpenSSL command for decryption
            command = [
                'openssl', 'enc', '-d', '-aes-256-cbc',           # AES-256-CBC decryption mode
                '-in', encrypted_file_path,                       # Input encrypted file path
                '-pass', f'file:{temp_key_file_path}',            # Pass key from temporary file
                '-pbkdf2',                                        # Use PBKDF2 key derivation
                '-iter', '10000'                                  # Number of PBKDF2 iterations
            ]
            # Execute OpenSSL command
            decrypted_data = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            print("Error during decryption:", e.stderr)
            raise RuntimeError("Failed to decrypt the file") from e

        finally:
            # Securely delete the temporary key file if it exists
            if temp_key_file_path and os.path.exists(temp_key_file_path):
                secure_delete(temp_key_file_path)

        return decrypted_data
