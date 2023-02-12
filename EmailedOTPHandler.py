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
        return message.split(" ")[-1]

    def get_otp(self):
        if self.email_provider.is_email_received():
            return self.parse_otp()
        return None
