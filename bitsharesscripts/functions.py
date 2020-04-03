import secrets
import string
from typing import Any, Dict, List, Optional

from bitsharesbase.account import PasswordKey


def generate_password(size=53, chars=string.ascii_letters + string.digits):
    """ Generate random word with letters and digits
    """
    return ''.join(secrets.choice(chars) for x in range(size))


def get_keys_from_password(
    account_name: str, password: str, blockchain_instance: Any, key_types: Optional[List[str]] = None,
) -> Dict[str, str]:
    """ Generates public/private keys from a password
    """
    if not key_types:
        key_types = ['active', 'owner', 'memo']

    keys = dict()
    for key_type in key_types:
        # PasswordKey object
        k = PasswordKey(account_name, password, role=key_type)

        privkey = k.get_private_key()
        print('{} private: {}'.format(key_type, str(privkey)))  # we need explicit str() conversion!

        # pubkey with default prefix GPH
        pubkey = k.get_public_key()

        # pubkey with correct prefix
        keys[key_type] = format(pubkey, blockchain_instance.prefix)
        print('{} public: {}\n'.format(key_type, keys[key_type]))

    return keys
