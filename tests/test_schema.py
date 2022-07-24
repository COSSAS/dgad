from dgad.schema import Domain

domains = ["google.com", "mail.google.com" "super.mail.google.com"]

from dgad.utils import setup_logging

setup_logging("debug")
Domain("google.com")
Domain("mail.google.com")
