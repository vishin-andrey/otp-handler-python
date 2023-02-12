import time
from abc import ABC, abstractmethod


class EmailProviderHandler(ABC):
    # this abstract class should be implemented for a particular email provider

    @abstractmethod
    def start(self, email_subject):  # start the connection to email provider
        pass

    @abstractmethod
    def is_email_received(self):  # check if a new email with email_subject was received
        pass

    @abstractmethod
    def get_message(self):  # get the message of the last email with email_subject
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
        position = message.find(self.otp_key_phrase)  # find the position of the OTP key phrase
        assert position != -1, 'OTP key phrase not found'
        position = position + len(self.otp_key_phrase)  # move to the position of the OTP
        return message[position:position + self.otp_length]  # get the OTP

    def get_otp(self):
        # trying to get a new email with email_subject, checking every 5 sec
        for attempt in range(6):
            if self.email_provider.is_email_received():
                return self.parse_otp()
            time.sleep(5)
        assert False, 'No OTP email received'

