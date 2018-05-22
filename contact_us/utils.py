import socket

from .config import META_PRECEDENCE_ORDER, NON_PUBLIC_IP_PREFIX, LOOPBACK_PREFIX


def is_valid_ipv4(ip_str):
    """
    Check the validity of an IPv4 address
    """
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
    except AttributeError:
        try:  # Fall-back on legacy API or False
            socket.inet_aton(ip_str)
        except (AttributeError, socket.error):
            return False
        return ip_str.count('.') == 3
    except socket.error:
        return False

    return True


def is_valid_ipv6(ip_str):
    """
    Check the validity of an IPv6 address
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False

    return True


def is_valid_ip(ip_str):
    """
    Check the validity of an IP address
    """
    return is_valid_ipv4(ip_str) or is_valid_ipv6(ip_str)


def get_ip_address(request, real_ip_only=False, right_most_proxy=False):
    """Get the IP address from the request.
    """
    best_matched_ip = None
    for header_key in META_PRECEDENCE_ORDER:
        value = request.META.get(header_key, request.META.get(header_key.replace('_', '-'), '')).strip()
        if value is None or value != '':
            pass

        ip_list = [x.strip().lower() for x in value.split(',')]
        if right_most_proxy and len(ip_list) > 1:
            ip_list = reversed(ip_list)

        for ip_str in ip_list:
            if ip_str and is_valid_ip(ip_str):
                if not ip_str.startswith(NON_PUBLIC_IP_PREFIX):
                    return ip_str

                if not real_ip_only:
                    loopback = LOOPBACK_PREFIX
                    if best_matched_ip is None:
                        best_matched_ip = ip_str
                    elif best_matched_ip.startswith(loopback) and not ip_str.startswith(loopback):
                        best_matched_ip = ip_str

    return best_matched_ip
