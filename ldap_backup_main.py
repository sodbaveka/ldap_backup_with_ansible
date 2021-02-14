#!/usr/bin/python3
"""Script for exporting (saving) and importing data from an LDAP directory in LDIFF and JSON formats."""

__authors__ = ("sodbaveka")
__contact__ = ("sodbaveka@gmail.com")
__version__ = "1.0.0"
__copyright__ = "copyleft"
__date__ = "2021/02"

import ldap3
from LdapAnnuary import LdapAnnuary

if __name__ == "__main__":
    ldap_main_host = 'srv-ldap-01'
    connexion_username = 'cn=admin,dc=sodbaveka,dc=com'
    connexion_password = 'theseus'
    try:
	    ldap_annuary = LdapAnnuary(ldap_main_host, connexion_username, connexion_password)
	    if ldap_annuary:
	    	## Informations about server and connexion
	    	print("User authenticated.\nWelcome {}.".format(ldap_annuary.connexion.extend.standard.who_am_i()))
	    	#print("\nServer informations : {}".format(ldap_annuary.server))
	    	#print("\nConnexion informations : {}".format(ldap_annuary.connexion))
	    	
	    	## Informations about saved data
	    	#print("\nUnites organisationnelles :\n", ldap_annuary.organizational_units_dicts)
	    	#print("\nUtilisateurs :\n", ldap_annuary.users_dicts)
	    	#print(ldap_annuary.data_ldif)

	    	## Serialization
	    	#ldap_annuary.serialize_in_file()
	    	#print("Serialization completed.")
	    	
	    	# Copy to files
	    	ldap_annuary.copy_to_ldif_file()
	    	print("Copy to ldif file completed.")
	    	ldap_annuary.copy_to_json_file()
	    	print("Copy to json file completed.")

    except ldap3.core.exceptions.LDAPBindError as login_error:
    	print(str(login_error))
    except ldap3.core.exceptions.LDAPPasswordIsMandatoryError as password_error:
    	print(str(password_error))