import socket
from socket import AF_INET, SOCK_STREAM
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose_mode=False):
    open_ports = []

    for port in range(port_range[0], port_range[1] + 1):
        server_socket = socket.socket(family=AF_INET, type=SOCK_STREAM)
        socket.setdefaulttimeout(1)
        try:
            result = server_socket.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
        except socket.gaierror:
            if target[0].isalpha():
                return "Error: Invalid hostname"
            return "Error: Invalid IP address"

        server_socket.close()

    if not verbose_mode:
        return open_ports

    if not target[0].isalpha():
        ip_addr = target
        try:
            target = socket.gethostbyaddr(ip_addr)[0]
        except socket.herror:
            target = ""
    else:
        ip_addr = socket.gethostbyname(target)

    if target:
        ans = f"Open ports for {target} ({ip_addr})\nPORT     SERVICE\n"

    else:
        ans = f"Open ports for {ip_addr}\nPORT     SERVICE\n"

    for port in open_ports:
        ans += f"{port:<9}{ports_and_services[port]}\n"
    return ans.strip()
