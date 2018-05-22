from django.conf import settings


PAGE_CONTEXT = {
    'title': getattr(settings, 'SITE_TITLE', 'Contact Us'),
    'author': getattr(settings, 'SITE_AUTHOR', 'Morgyn Stryker'),
    'description': getattr(settings, 'SITE_DESCRIPTION', 'Contact us with any comments or questions!'),
    'keywords': getattr(settings, 'CONTACT_US_KEYWORDS', 'contact'),
    'favicon': getattr(settings, 'SITE_FAVICON', ''),
    'header': getattr(settings, 'CONTACT_US_HEADER', 'Contact Us')
}

META_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR',
    'X_FORWARDED_FOR',  # client, proxy1, proxy2
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)
PRIVATE_IP_PREFIX = (
    '0.',  # externally non-routable
    '10.',  # class A private block
    '169.254.',  # link-local block
    '172.16.',
    '172.17.',
    '172.18.',
    '172.19.',
    '172.20.',
    '172.21.',
    '172.22.',
    '172.23.',
    '172.24.',
    '172.25.',
    '172.26.',
    '172.27.',
    '172.28.',
    '172.29.',
    '172.30.',
    '172.31.',  # class B private blocks
    '192.0.2.',  # reserved for documentation and example code
    '192.168.',  # class C private block
    '255.255.255.',  # IPv4 broadcast address
    '2001:db8:',  # reserved for documentation and example code
    'fc00:',  # IPv6 private block
    'fe80:',  # link-local unicast
    'ff00:',  # IPv6 multicast
)
LOOPBACK_PREFIX = (
    '127.',  # IPv4 loopback device
    '::1',  # IPv6 loopback device
)
NON_PUBLIC_IP_PREFIX = PRIVATE_IP_PREFIX + LOOPBACK_PREFIX
