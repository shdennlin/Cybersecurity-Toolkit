# Cybersecurity Toolkit

- [Cybersecurity Toolkit](#cybersecurity-toolkit)
  - [License with Keygen.sh](#license-with-keygensh)
  - [Encrypt large file using AES-256-CBC and seal key to TPM](#encrypt-large-file-using-aes-256-cbc-and-seal-key-to-tpm)
    - [Prerequisites](#prerequisites)
    - [Encrypt](#encrypt)
    - [Decrypt](#decrypt)
    - [TPM2 Utilities](#tpm2-utilities)

## License with Keygen.sh

Using [./keygen/keygen.py](./keygen/keygen.py) to validate a license key from [Keygen.sh](https://keygen.sh/).

Example can be found in [./example_keygen.py](./example_keygen.py)

Python library required: `requests`

## Encrypt large file using AES-256-CBC and seal key to TPM

### Prerequisites

1. Check system if support TPM

    ``` bash
    cat /sys/class/tpm/tpm*/tpm_version_major 
    ```

2. Install `openssl` and `tpm2-tools`

    ``` bash
    sudo apt-get install openssl tpm2-tools
    ```

3. Add user to `tss` group if you need.

    ``` bash
    sudo groupadd tss
    newgrp tss
    ```

### Encrypt

Using [./tpm/tpm_encrypt.sh](./tpm/tpm_encrypt.sh) to encrypt a file and seal the key to TPM.

Usage (use `./tpm_encrypt.sh -h` to show help):

``` bash
chmod +x ./tpm_encrypt.sh
./tpm_encrypt.sh <file> <tpm_address>
```

### Decrypt

- Option 1: Decrypt using command line

    ``` bash
    tpm2_unseal -c <tpm_address> -o key.bin
    openssl enc -d -aes-256-cbc -in ${file_enc} -out ${file} -pass file:./key.bin -pbkdf2 -iter 10000
    ```

- Option 2: Decrypt using [./tpm/tpm_decrypter.py](./tpm/tpm_decrypter.py)
    Example can be found in [./example_tpm_decrypter.py](./example_tpm_decrypter.py)

### TPM2 Utilities

- Show current persistent handles in TPM

    ```bash
    tpm2_getcap handles-persistent
    ```

- Clean up persistent handles

    ```bash
    tpm2_evictcontrol -C o -c 0x810F2A89; tpm2_getcap handles-persistent
    ```