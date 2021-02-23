class OrganizationalUnit:
	"""
	A class to represent a LDAP Organizational Unit

	...

	Attributes
	----------
	dn : str
		Distinguished Name

	attributes : dict
		Dictionary of attributes

	objectClass : str
		Object class

	ou : str
		Organizational unit's name

	description : str
		A description of organizational unit

	Methods
	-------
	str__():
		Redefinition of method __str__()
	"""

	def __init__(self, uo_dict):
		"""
		Constructs all the necessary attributes for the LDAP Organizational Unit object

		...

		Attributes
		----------
		dn : str
			Distinguished Name

		attributes : dict
			Dictionary of attributes

		objectClass : str
			Object class

		ou : str
			Organizational unit's name

		description : str
			A description of organizational unit

		"""

		
		self.dn = uo_dict['dn']
		self.attributes = uo_dict['attributes']
		self.objectClass = uo_dict['attributes']['objectClass'][0]
		self.ou = uo_dict['attributes']['ou'][0]
		self.description = uo_dict['attributes']['description'][0]

	def __str__(self):
		"""Redefinition of method __str__"""
		return "dn: {}\nobjectClass: {}\nou: {}\ndescription: {}\n".format(self.dn, self.objectClass, self.ou, self.description)