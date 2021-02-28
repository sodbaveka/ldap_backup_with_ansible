### Table of Contents
***
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [License](#License)
5. [Ressources](#Ressources)

### General Info
***
Hello World!

My name is Mickaël alias sodbaveka.
I created this repository as a lab to discover git, gitHub, Python and Ansible.

My project as a learner is to create a python script to automate the saving of objects from an ldap directory to files of different exploitable formats (ldif, json, yml). Another python script will allow data to be restored to a backup server, using the generated json file.
These scripts will be factored into Ansible modules.

Ansible will therefore have the following task:
- install and configure openLDAP,
- to install a Web interface allowing the management of the entries (for example, users, groups, DHCP parameters) stored in an LDAP directory,
- play the backup and restore scripts.

Please feel free to message me if you have any questions.

Bye ;-)

### Technologies
***
A list of technologies used within the project:
* Linux Debian 10.8
* ansible 2.10.5
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.7/dist-packages/ansible
  executable location = /usr/local/bin/ansible
* python version = 3.7.3 (default, Jul 25 2020, 13:03:44) [GCC 8.3.0]

### Installation
***
A little intro about the installation. 
```
$ git clone https://github.com/sodbaveka/SodbavekaProject.git
$ cd ../path/to/the/file
```

### License
***
* Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
* GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

### Ressources
***
https://docs.ansible.com/
https://ldap3.readthedocs.io/en/latest/
‘python for dummies’ :-p 

