from app.utils import send_test_email
from .utils.utils import random_email


def test_send_test_email():
    send_test_email(random_email())
