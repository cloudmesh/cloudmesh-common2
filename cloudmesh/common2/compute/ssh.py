import paramiko
from cloudmesh.common2.compute import CloudmeshComputeABC
import paramiko
from openvpn_api import VPN


class SSHCompute(CloudmeshComputeABC):

    def __init__(self,
                 vpn_host=None,
                 vpn_port=None,
                 vpn_username=None,
                 vpn_password=None,
                 ssh_host=None,
                 ssh_username=None,
                 private_key_path=None):
        self.vpn_host = vpn_host
        self.vpn_port = vpn_port
        self.vpn_username = vpn_username
        self.vpn_password = vpn_password
        self.ssh_host = ssh_host
        self.ssh_username = ssh_username
        self.private_key_path = private_key_path
        self.ssh_client = None

    def connect_vpn(self):
        self.vpn = VPN(
            endpoint=f'{self.vpn_host}:{self.vpn_port}',
            username=self.vpn_username,
            password=self.vpn_password
        )
        self.vpn.connect()
        print("Connected to VPN")

    def disconnect_vpn(self):
        self.vpn.disconnect()
        print("Disconnected from VPN")

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(
            self.ssh_host, username=self.ssh_username,
            key_filename=self.private_key_path
        )

    def run(self, command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

    def close(self):
        self.ssh_client.close()
        print("SSH connection closed")

    def authenticate(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.hostname, username=self.username, password=self.password)

    def upload(self, local_path, remote_path):
        sftp = self.ssh_client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def download(self, remote_path, local_path):
        sftp = self.ssh_client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()


if __name__ == "__main__":
    # DO NOT USE THIS EXAMPLE AS PASSWORDS MUST NOT HARDCODED.
    hostname = "example.com"
    username = "your_username"
    password = "your_password"

    compute = SSHCompute(hostname, username, password)
    compute.authenticate()
    compute.upload("local_file.txt", "/home/remote_user/remote_file.txt")
    stdout, stderr = compute.run("ls -l /home/remote_user")
    print("Stdout:", stdout)
    print("Stderr:", stderr)
    # ... other method calls ...


# if __name__ == "__main__":
#       vpn_host = "vpn.example.com"
#       vpn_port = 443
#       vpn_username = "your_vpn_username"
#       vpn_password = "your_vpn_password"
#       ssh_host = "target.example.com"
#       ssh_username = "your_ssh_username"
#       private_key_path = "/path/to/your/private_key.pem"
#       ssh_command = "ls -l"
#
#       vpn_ssh_executor = VPNSSHExecutor(vpn_host, vpn_port, vpn_username, vpn_password, ssh_host, ssh_username,
#                                         private_key_path)
#
#       vpn_ssh_executor.connect_vpn()
#       vpn_ssh_executor.connect_ssh()
#       vpn_ssh_executor.execute_ssh_command(ssh_command)
#       vpn_ssh_executor.close_ssh()
#       vpn_ssh_executor.disconnect_vpn()