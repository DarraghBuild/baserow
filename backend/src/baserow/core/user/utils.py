import unicodedata
from django.conf import settings

def normalize_email_address(email):
    """
    Normalizes an email address by stripping the whitespace, converting to lowercase
    and by normalizing the unicode.

    :param email: The email address that needs to be normalized.
    :type email: str
    :return: The normalized email address.
    :rtype: str
    """

    return unicodedata.normalize("NFKC", email).strip().lower()

def is_user_super_admin(self, user):
    return self.is_email_super_admin(user.email)

def is_email_super_admin(self, email):
    return email in settings.SUPER_ADMINS
