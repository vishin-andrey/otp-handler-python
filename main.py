from EmailedOTPHandler import EmailedOTPHandler
from GmailHandler import GmailHandler

subject = "OTP test"
keyPhrase = "Your OTP is: "
otpLength = 6

if __name__ == '__main__':
    gmail = GmailHandler()
    otp_handler = EmailedOTPHandler(subject, keyPhrase, otpLength, gmail)
    otp_handler.start_email_provider()  # start email provider
    # -> Here trigger the OTP email sending
    otp = otp_handler.get_otp()  # get OTP from email
    print(f'OTP: {otp}')



