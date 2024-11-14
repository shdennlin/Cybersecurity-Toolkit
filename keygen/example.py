"""Code Example for Keygen"""

from src.keygen import Keygen

# Keygen.sh
KEYGEN_ACCOUNT_ID = ""  # ex: "00000000-0000-0000-0000-000000000000"
KEYGEN_LICENSE_KEY = ""  # ex: "C1B6DE-39A6E3-DE1529-8559A0-4AF593-V3"
KEYGEN_MACHINE_FINGERPRINT = ""  # ex: "f1adc3aed0ba31a418fc7c2e1d63c3e0b1207a6cea5613f650945235f1812fcd"


def valid_license():
    """Validate a license key Example"""
    keygen = Keygen(KEYGEN_ACCOUNT_ID)
    valid, code, detail = keygen.validate_license_key(KEYGEN_LICENSE_KEY, KEYGEN_MACHINE_FINGERPRINT)
    print(
        f"License is {'VALID' if valid else 'INVALID'}: detail=\"{detail}\" code=\"{code}\""
    )


if __name__ == "__main__":
    valid_license()
