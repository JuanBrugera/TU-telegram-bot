class UserData:
    CHAT_ID = 'CHAT_ID'
    DETAILS = 'DETAILS'
    MESSAGE_IDS = 'MESSAGE_IDS'
    PRODUCT_URL = 'PRODUCT_URL'

    @classmethod
    def all_literals(cls):
        return {k for k, v in cls.__dict__.items() if k == v}
