import subprocess
import platform
import time


class VPN:
    def __init__(self, vpn_gateway, vpn_server, vpn_username, vpn_password):
        self.vpn_gateway = vpn_gateway
        self.vpn_server = vpn_server
        self.vpn_username = vpn_username
        self.vpn_password = vpn_password
        self.routes = []
        self.connected = False

    def add_route(self, destination):
        if platform.system() == "Windows":
            subprocess.run(["route", "add", destination,
                            "mask", "255.255.255.255",
                            self.vpn_gateway], shell=True)
        else:
            subprocess.run(["sudo",
                            "ip", "route", "add", destination,
                            "via", self.vpn_gateway])
        self.routes.append(destination)

    def remove_route(self):
        for destination in self.routes:
            if platform.system() == "Windows":
                subprocess.run(["route", "delete", destination], shell=True)
            else:
                subprocess.run(["sudo", "ip", "route", "del", destination])
        self.routes = []

    def connect(self):
        if not self.connected:
            vpn_cmd = [
                "openvpn" if platform.system() == "Linux" else "openvpn.exe",
                "--remote", self.vpn_server,
                "--dev", "tun",
                "--proto", "udp",
                "--resolv-retry", "infinite",
                "--nobind",
                "--persist-key",
                "--persist-tun",
                "--route-noexec"
            ]

            env = {
                "VPN_USERNAME": self.vpn_username,
                "VPN_PASSWORD": self.vpn_password
            }

            subprocess.Popen(vpn_cmd, env=env)

            self.connected = True

    def disconnect(self):
        if self.connected:
            if platform.system() == "Windows":
                subprocess.run(["taskkill", "/IM", "openvpn.exe", "/F"], shell=True)
            else:
                subprocess.run(["sudo", "killall", "openvpn"])
            self.connected = False


# Usage
if __name__ == "__main__":
    vpn1_gateway = "VPN1_GATEWAY_IP"
    vpn1_server = "VPN1_SERVER_IP"
    vpn1_username = "YOUR_VPN_USERNAME"
    vpn1_password = "YOUR_VPN_PASSWORD"

    vpn1 = VPN(vpn1_gateway, vpn1_server, vpn1_username, vpn1_password)

    try:
        # Adding routes
        vpn1.add_route("REMOTE_HOST_IP1")
        vpn1.add_route("REMOTE_HOST_IP2")

        # Connect to VPN
        vpn1.connect()

        # Now you can establish SSH connections to the remote hosts through the VPN

        # Wait for a while to use the VPN
        time.sleep(10)

    finally:
        # Disconnect from VPN, remove routes, and clean up
        vpn1.disconnect()
        vpn1.remove_route()