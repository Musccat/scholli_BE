import string
import secrets

class SendEmailHelper:
    def make_random_code():
        digit_and_alpha = string.ascii_letters+string.digits
        return "".join(secrets.choice(digit_and_alpha) for _ in range(6))

sendEmailHelper = SendEmailHelper()