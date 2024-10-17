# vault<span>.py
You can use this python module to decrypt sensitive values which are stored in a YAML file as separate variables encrypted by Ansible Vault. Also, this module can decrypt the whole file and return initial values. 
This module operates with Ansible Vault libraries directly. 

### Prerequisite
Installed Python 3 (at least 3.10.10) and Ansible Core (it includes Ansible Vault). Password for Vault has been set either as an environment variable **ANSIBLE_VAULT_PASSWORD_FILE** or in the ansible.cfg file.
### Getting Started

This module has been tested with
 - ansible-vault [core 2.16.2]
 - Python 3.10.10

#### Scenario 1
For example, you’ve created a YAML file (let it be variables.yml) and there has been added sensitive information like passwords, token etc. as key=value pairs. For instance, file may be look like that:
```
---
username1: j.doe
password1: $ANSIBLE_VAULT;1.1;AES256
           32633430653435346562336338306662343948392099234111938524916163616363306134373437
           3438303933313962663363313766373563383564343036300a333039333231313765636331616539
           37616235363734982719453061356430383236373235363564343739323030386639386463323337
           3638306134626135650a656664336263666234616435377823200029456285392183750633437336
           38613563303832653436346332356139643439646263666263633664303535666334

username2: jj.doe
password2: $ANSIBLE_VAULT;1.1;AES256
           32633430653435346562336338306662343948392099234111938524916163616363306134373437
           3438303933313962663363313766373563383564343036300a333039333231313765636331616539
           37616235363734982719453061356430383236373235363564343739323030386639386463323337
           3638306134626135650a656664336263666234616435377823200029456285392183750633437336
           38613563303832653436346332356139643439646263666263633664303535666334
```
To use decrypted variables somewhere else you must decrypt them first. This can be done by importing **vault<span>.py** module to your Python script and call the method ***decrypt_vault_secrets(<path to variables.yml >)*** from class Vault
```
import vault

vault_instance = vault.Vault()
credentials = vault_instance.decrypt_vault_secrets(variables.yml) 
```
The variable **credentials** will be contained both your plain text variables and decrypted ones from the initial file variables.yml as a python dictionary. If there is an error during the file processing, the output dictionary will be empty.

#### Scenario 2
You want to securely handle with all information that is contained in a YAML file (for example, the file name is vault.yml). First, you create a file with your sensitive information, for instance:
```
---
username1: j.doe
password1: test-password

username2: jj.doe
password2: test-password-2
```
and then you encrypt it using Ansible Vault. 
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