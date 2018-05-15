#!/usr/local/bin/python3
# VaultX Beta (0.1.2b) @ dev
# Version date: 8 May 2018
# By Henry Harder

import pyAesCrypt as pac
import pyperclip as pyp
import os, pickle
import config

class Vault():
    def __init__(self, msg, wallets={}):
        self.wallets = wallets
        self.temp_key = ''
        self.msg = msg
        self.bsize = 64*1024

        self.resp = {
            'yes_copy' : 'Sucessfully copied information.',
            'yes_update' : 'Successfully updated secure data.',
            'yes_load' : 'Data loaded from secure file.',
            'no_copy' : 'Please select an entry.',
            'copy_fail' : 'Something went wrong',
            'pass_fail' : 'Incorrect password.',
            'io_fail' : 'Error encountered while opening file.',
            'fnf_fail' : "Data file not found, click 'Create New Vault.'"
            'perm_fail' : 'VaultX denied FS permission, check install location'
            }

    def cache_key(self, entry):
        self.temp_key = ''.join(entry.get())

    def add(self, wallet):
        self.wallets[wallet.name] = wallet

    def remove(self, wallet):
        del self.wallets[wallet]

    def open(self, key_entry):
        #os.chdir(config.data_dir)
        self.cache_key(key_entry)

        try:
            pac.decryptFile(config.data_e, config.data_u,
                                self.temp_key, self.bsize)

        except ValueError:
            self.msg.set(self.resp['pass_fail'])
            return 0

        except IOError:
            self.msg.set(self.resp['io_fail'])
            return 0

        except PermissionError:
            self.msg.set(self.resp['perm_fail'])
            return 0
        

        pickle_file = open(config.data_u, 'rb')
        self.wallets = pickle.load(pickle_file)
        self.msg.set(self.resp['yes_load'])
        os.remove(config.data_u)
        return 1

    def update_data(self):
        #os.chdir(config.data_dir)
        try:
            object_file = open(config.temp_n, 'wb+')
            pickle.dump(self.wallets, object_file, protocol=4)
            object_file.close()
            pac.encryptFile(config.temp_n, config.data_e,
                            self.temp_key, self.bsize)

        except ValueError:
            self.msg.set(self.resp['pass_fail'])
            return 0

        except IOError:
            self.msg.set(self.resp['io_fail'])
            return 0

        except PermissionError:
            self.msg.set(self.resp['perm_fail'])
            return 0

        os.remove(config.temp_n)
        self.msg.set(self.resp['yes_update'])

    def copy_data(self, value, option):
        try:
            if option == 1:
                pyp.copy(self.wallets[value].addr)
                self.msg.set(self.resp['yes_copy'])
            elif option == 2:
                pyp.copy(self.wallets[value].pas)
                self.msg.set(self.resp['yes_copy'])
            elif option == 3:
                pyp.copy(self.wallets[value].seed)
                self.msg.set(self.resp['yes_copy'])
            elif option == 4:
                pyp.copy(self.wallets[value].pkey)
                self.msg.set(self.resp['yes_copy'])
            else:
                self.msg.set(self.resp['no_copy'])
        except:
            self.msg.set(self.resp['copy_fail'])

    def display_data(self, value, option, msg):
        try:
            if option == 1:
                self.msg.set(self.wallets[value].addr)
            elif option == 2:
                self.msg.set(self.wallets[value].pas)
            elif option == 3:
                self.msg.set(self.wallets[value].seed)
            elif option == 4:
                self.msg.set(self.wallets[value].pkey)
            else:
                self.msg.set(self.resp['no_copy'])
        except:
            self.msg.set(self.resp['copy_fail'])

class Wallet():
    def __init__(self, name, passw, seed, privkey='none', addr='none'):
        self.name = str(name)
        self.pas = str(passw)
        self.seed = str(seed)
        self.pkey = str(privkey)
        self.addr = str(addr)
