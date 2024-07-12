import ldap

# Used to parse key-value LDAP attributes
USERNAME_FILTER_TEMPLATE = "(&(objectClass=user)(sAMAccountName=%s))"
BINDING_TEMPLATE = "%s@IC.AC.UK"


class LdapAuthenticator:
    def __init__(self, server_url: str, base_dn: str) -> None:
        self.server_url = server_url
        self.base_dn = base_dn

    def authenticate(self, username: str, password: str) -> bool:
        try:
            connection = ldap.initialize(self.server_url)
            connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
            connection.simple_bind_s(BINDING_TEMPLATE % username, password)
            connection.unbind_s()
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
