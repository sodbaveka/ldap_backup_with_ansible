#!/usr/bin/python3
"""Script for exporting data from a bin file to an LDAP server."""

__authors__ = ("sodbaveka")
__contact__ = ("sodbaveka@gmail.com")
__version__ = "1.0.0"
__copyright__ = "copyleft"
__date__ = "2021/02"

import ldap3
from LdapRestoredAnnuary import LdapRestoredAnnuary

if __name__ == "__main__":
    ldap_backup_host = 'srv-ldap-02'
    connexion_username = 'cn=admin,dc=sodbaveka,dc=com'
    connexion_password = 'theseus'
    try:
	    ldap_restored_annuary = LdapRestoredAnnuary(ldap_backup_host, connexion_username, connexion_password)
	    if ldap_restored_annuary:
	    	print("User authenticated.\nWelcome {}.".format(ldap_restored_annuary.connexion.extend.standard.who_am_i()))
	    	ldap_restored_annuary.deserialize_from_file()
	    	print("Deserialization completed.")
	    	#ldap_restored_annuary.push_data()
	    	#print("Restoration completed.")
	    	ldap_restored_annuary.delete_data()
	    	print("Removal completed.")
    except ldap3.core.exceptions.LDAPBindError as login_error:
    	print(str(login_error))
    except ldap3.core.exceptions.LDAPPasswordIsMandatoryError as password_error:
    	print(str(password_error))