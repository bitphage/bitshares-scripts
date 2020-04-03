import secrets
import string


def generate_password(size=53, chars=string.ascii_letters + string.digits):
    """ Generate random word with letters and digits
    """
    return ''.join(secrets.choice(chars) for x in range(size))
