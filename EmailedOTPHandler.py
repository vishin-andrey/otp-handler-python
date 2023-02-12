import time
from abc import ABC, abstractmethod


class EmailProviderHandler(ABC):

    @abstractmethod
    def start(self, email_subject):
        pass

    @abstractmethod
    def is_email_received(self):
        pass

    @abstractmethod
    def get_message(self):
        pass


class EmailedOTPHandler:

    def __init__(self, email_subject, otp_key_phrase, otp_length, email_provider):
        self.email_subject = email_subject
        self.otp_key_phrase = otp_key_phrase
        self.otp_length = otp_length
        self.email_provider = email_provider

    def start_email_provider(self):
        self.email_provider.start(self.email_subject)

    def parse_otp(self):
        message = self.email_provider.get_message()
        assert message is not None, 'No message received'
        pos = message.find(self.otp_key_phrase)  # find the position of the OTP key phrase
        assert pos != -1, 'OTP key phrase not found'
        pos = pos + len(self.otp_key_phrase)  # move to the position of the OTP
        return message[pos:pos + self.otp_length]  # get the OTP

    def get_otp(self):
        # trying to get a new email, checking for a new message every 5 sec
        for i in range(6):
            if self.email_provider.is_email_received():
                return self.parse_otp()
            time.sleep(5)
        assert False, 'No OTP email received'

