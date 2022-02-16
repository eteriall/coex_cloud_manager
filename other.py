import random


def generate_auth_code():
    return ''.join(random.choice('QWERTYUPASDFGHJKLZXCVBNM23456789') for _ in range(6))

def human_date(value, format="%B %d at %I:%M %p"):
    """Format a datetime object to be human-readable in a template."""
    return value.strftime(format)
