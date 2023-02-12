from EmailedOTPHandler import EmailedOTPHandler
from GmailHandler import GmailHandler

SUBJECT = "OTP test"
KEY_PHRASE = "Your OTP is: "
OTP_LENGTH = 6

if __name__ == '__main__':
    gmail = GmailHandler()
    otp_handler = EmailedOTPHandler(SUBJECT, KEY_PHRASE, OTP_LENGTH, gmail)
    otp_handler.start_email_provider()
    # -> Here trigger the OTP email sending
    otp = otp_handler.get_otp()
    print(f'Received OTP: {otp}')



