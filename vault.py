#!usr/bin/env python3

import yaml
from os.path import basename
from ansible.constants import DEFAULT_VAULT_IDENTITY_LIST # type: ignore
from ansible.parsing.vault import VaultLib
from ansible.parsing.utils.yaml import from_yaml
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader

class Vault:
    def __init__(self) -> None:
        global vault_secret

        loader = DataLoader()
        vault_secret = CLI.setup_vault_secrets(loader=loader, vault_ids=DEFAULT_VAULT_IDENTITY_LIST)

    def decrypt_file(self, encrypted_file: str) -> dict:
        '''
            This method decrypts a file which is protected by Ansible Vault. The Vault password 
            is taken from the enviroment variable ANSIBLE_VAULT_PASSWORD_FILE based on default vault-id
            list option DEFAULT_VAULT_IDENTITY_LIST. If you need to change the behaviour, please read 
            this official docs about Ansible configuration settings 
            https://docs.ansible.com/ansible/2.9/reference_appendices/config.html

            args:
              encrypted_file (str): YAML file encrypted by Ansible Vault

            output:
              If the decryption process is successful, it'll return a decrypted content of 
              the original YAML file as a dictionary. If not - just empty dictionary.
        '''
        vault = VaultLib(vault_secret)
        try:
            inputdata = open(encrypted_file).read()
            credentials = yaml.load(vault.decrypt(inputdata), Loader=yaml.SafeLoader)
        except FileNotFoundError:
            print('Input encrypted file not found: ' + basename(encrypted_file))
            credentials = {}
        except PermissionError:
            print('File access error: no enough permissions to read ' + basename(encrypted_file))
            credentials = {}

        return credentials
    
    def decrypt_vault_secrets(self, vault_file: str) -> dict:
        '''
            This method decrypts a YAML file with Ansible Vault secrets. The Vault password 
            is taken from the enviroment variable ANSIBLE_VAULT_PASSWORD_FILE based on default vault-id 
            list option DEFAULT_VAULT_IDENTITY_LIST. If you need to change this behaviour, please read 
            the official docs about Ansible configuration settings 
            https://docs.ansible.com/ansible/2.9/reference_appendices/config.html

            args:
              vault_file (str): YAML file with Ansible Vault secrets

            output:
              If the decryption process is successful, it'll return the initial YAML file content as a dictionary with 
              decrypted secrets. If not - just empty dictionary.
        '''
        yaml_clear_text = {}
        try:
            yaml_data = from_yaml(
                data=open(vault_file).read(),
                vault_secrets=vault_secret
            )
            yaml_clear_text = yaml.load(str(yaml_data), Loader=yaml.SafeLoader)
        except FileNotFoundError:
            print('Input YAML file with Vault secrets hasn\'t been found: ' + basename(vault_file))
            return yaml_clear_text
        except PermissionError:
            print('File access error: no enough permissions to read ' + basename(vault_file))
            return yaml_clear_text
        return yaml_clear_text
