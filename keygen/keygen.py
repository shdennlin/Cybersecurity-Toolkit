"""This module is used to interact with the Keygen API."""

import json

import requests


class Keygen:
    """This class is used to interact with the Keygen API."""

    def __init__(
        self,
        account_id: str,
    ):
        if account_id == "":
            raise ValueError("Account ID is required")
        self.account_id = account_id
        self.base_url = f"https://api.keygen.sh/v1/accounts/{account_id}"

    def validate_license_key(
        self, license_key: str, fingerprint: str
    ) -> tuple[bool, str, str]:
        """
        Validates a license key against a given fingerprint.

        Args:
            license_key (str): The license key to be validated.
            fingerprint (str): The fingerprint to validate the license key against.

        Returns:
            tuple(bool, str, str): A tuple containing:
                - bool: Whether the license key is valid.
                - str: The validation code.
                - str: The validation detail.

        Raises:
            ValueError: If the validation response contains errors.
        """

        if license_key == "":
            raise ValueError("License key is required")
        if fingerprint == "":
            raise ValueError("Fingerprint is required")

        url = f"{self.base_url}/licenses/actions/validate-key"
        headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }
        data = json.dumps(
            {
                "meta": {
                    "key": license_key,
                    "scope": {
                        "fingerprint": fingerprint,
                    },
                }
            }
        )
        validation = requests.post(url, headers=headers, data=data, timeout=15).json()
        if validation.get("errors"):
            title = validation["errors"][0]["title"]
            code = validation["errors"][0]["code"]
            detail = validation["errors"][0]["detail"]
            raise ValueError(f"Error: {title} - {detail} (code: {code})")

        valid: bool = validation["meta"]["valid"]
        code: str = validation["meta"]["code"]
        detail: str = validation["meta"]["detail"]

        return valid, code, detail
