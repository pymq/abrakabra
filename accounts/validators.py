import re

from django.utils import six
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w+-]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and +/-/_ characters.'
    )
    flags = re.ASCII if six.PY3 else 0


custom_username_validators = [ASCIIUsernameValidator()]
