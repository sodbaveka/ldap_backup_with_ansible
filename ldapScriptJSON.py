from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import json
import simplejson

# Variables
total_entries_users = 0
total_entries_uo = 0
ldif_file = ""

# Declaration serveur ldap
server = Server('srv-ldap-01', get_info=ALL)

# Connexion
connexion = Connection(server, user = 'cn=admin,dc=sodbaveka,dc=com', password = 'theseus', auto_bind=True)

# Recherche users
connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
total_entries_users += len(connexion.response)

# Copie dans fichiers
for entry in connexion.entries:
	data = entry.entry_to_ldif().lstrip('version: 1\n').rstrip('# total number of entries: 1')
	ldif_file += data

#print(ldif_file)

# Ecriture dans un fichier json
fichier = open("users.json","wt")
fichier.write(simplejson.dumps(ldif_file))
fichier.close()

# Lecture du fichier json
fichier2 = open("users.json","rt")
data2 = simplejson.loads(fichier2.read())
print(data2)
fichier.close()