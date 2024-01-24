# vault<span>.py
This python module uses Ansible Vault libraries directly to decrypt credentials which are stored in a YAML file.

### Prerequisite
Installed Python 3 (at least 3.10.10) and Ansible Core (it includes Ansible Vault). Password for Vault has been set either as an environment variable **ANSIBLE_VAULT_PASSWORD_FILE** or in the ansible.cfg file.
### Getting Started

This module has been tested with
 - ansible-vault [core 2.16.2]
 - Python 3.10.10

You have to create a YAML file (vault.yml) which will be contain you credentials, for instance:
```
username1: j.doe
password1: test

username2: jj.doe
password2: test2
```
Then, you ought to encrypt this file using Ansible Vault. 
```
$ansible-vault encrypt vault.yml
```
In order to decrypt this file in your python script you have to import **vault<span>.py** module and call the method ***decrypt_file()*** from class Vault
```
import vault

vault_instance = vault.Vault()
credentials = vault_instance.decrypt_file('vault.yml') 
```
The variable **credentials** will contain your decrypted data from the initial file vault.yml as a dictionary. If there is an error during the file processing, the output dictionary will be empty.