#!usr/bin/env python3

import yaml
from os.path import basename
from ansible.constants import DEFAULT_VAULT_IDENTITY_LIST
from ansible.parsing.vault import VaultLib
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader

class Vault:
    def __init__(self) -> None:
        # for future use
        pass

    def decrypt_file(self, encrypted_file: str) -> dict:
        '''
                This method decrypts a file which is protected by Ansible Vault. The Vault password is taken from 
            the environment variable ANSIBLE_VAULT_PASSWORD_FILE based on default vault-id 
            list option DEFAULT_VAULT_IDENTITY_LIST. If you need to modify this behaviour, please read about 
            Ansible configuration settings: https://docs.ansible.com/ansible/2.9/reference_appendices/config.html 
            and change this module in accordance with your requirements.

            Usage:

              input:  'encrypted_file' - YAML file encrypted by Ansible Vault

              output: If the decryption process is successful, it'll return a decrypted content of the 
                           original YAML file as a dictionary. If not - just empty dictionary.
        '''
        loader = DataLoader()
        vault_secret = CLI.setup_vault_secrets(loader=loader, vault_ids=DEFAULT_VAULT_IDENTITY_LIST)
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