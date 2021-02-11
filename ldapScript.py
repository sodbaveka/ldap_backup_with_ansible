from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import json

# Variables
total_entries_users = 0
total_entries_uo = 0
ldif_file = ""

# Declaration serveur ldap
server = Server('srv-ldap-01', get_info=ALL)

# Connexion
connexion = Connection(server, user = 'cn=admin,dc=sodbaveka,dc=com', password = 'theseus', auto_bind=True)

# Recherche organizational units
connexion.search('dc=sodbaveka,dc=com', '(objectclass=organizationalUnit)', attributes=ALL_ATTRIBUTES)
total_entries_uo += len(connexion.response)

# Copie dans fichiers
for entry in connexion.entries:
	data = entry.entry_to_ldif().lstrip('version: 1\n').rstrip('# total number of entries: 1')
	ldif_file += data

# Recherche users
connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
total_entries_users += len(connexion.response)

# Copie dans fichiers
for entry in connexion.entries:
	data = entry.entry_to_ldif().lstrip('version: 1\n').rstrip('# total number of entries: 1')
	ldif_file += data

# Ecriture dans un fichier ldif
fichier = open("users.ldif","wt")
fichier.write(ldif_file.strip())
fichier.close()

# fichier2 = open("users.json","rt")
# test = fichier2.read()
# print(test.strip())

