from pyotp import TOTP


class CreateOTPCommand:
    @staticmethod
    def execute(secret: str) -> TOTP:
        return TOTP(secret)


create_otp_command = CreateOTPCommand.execute
