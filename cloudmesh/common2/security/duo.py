from duo_universal.client import Client


class DuoAuthentication:
    def __init__(self, integration_key, secret_key, api_hostname):
        self.integration_key = integration_key
        self.secret_key = secret_key
        self.api_hostname = api_hostname
        self.duo_client = Client(self.integration_key, self.secret_key, self.api_hostname)

    def initiate_authentication(self, username):
        response = self.duo_client.auth('push', username=username)

        if response['result'] == 'allow':
            return response['txid']
        else:
            return None

    def check_authentication_status(self, txid):
        response = self.duo_client.auth_status(txid)

        if response['result'] == 'success':
            return True
        else:
            return False


def main():
    integration_key = "your_integration_key"
    secret_key = "your_secret_key"
    api_hostname = "api_hostname"

    username = input("Enter your username: ")

    duo_auth = DuoAuthentication(integration_key, secret_key, api_hostname)
    txid = duo_auth.initiate_authentication(username)

    if txid:
        print("Duo Push authentication initiated. Approve the request in your Duo app.")
        success = duo_auth.check_authentication_status(txid)

        if success:
            print("Two-factor authentication successful.")
        else:
            print("Two-factor authentication failed.")
    else:
        print("Duo Push authentication initiation failed.")


if __name__ == "__main__":
    main()
