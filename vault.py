#!/usr/bin/python3
# VaultX Beta (0.1.2)
# Version date: 6 May 2018
# By Henry Harder

import pyAesCrypt as pac
import os, pickle
import config

class Vault():
    def __init__(self, wallets={}):
        self.wallets = wallets
        self.temp_key = ''
        self.message = ''
        self.bsize = 64*1024

    def add(self, wallet):
        self.wallets[wallet.name] = wallet

    def remove(self, wallet):
        del self.wallets[wallet]

    def open(self, key_entry):
        os.chdir(config.data_dir)
        self.temp_key = ''.join(key_entry.get())

        try:
            pac.decryptFile(config.data_e, config.data_u,
                                self.temp_key, self.bsize)

        except ValueError:
            self.message = 'Incorrect password or corrupted file.'
            return 0

        except IOError:
            self.message = 'Error encountered while opening file.'
            return 0

        pickle_file = open(config.data_u, 'rb')
        self.wallets = pickle.load(pickle_file)
        self.message = 'Data loaded from secure file.'
        os.remove(config.data_u)

        return 1

    def update_data(self):
        os.chdir(config.data_dir)
        object_file = open(config.temp_n, 'wb+')
        pickle.dump(self.wallets, object_file, protocol=4)
        object_file.close()
        pac.encryptFile(config.temp_n, config.data_e,
                        self.temp_key, self.bsize)
        os.remove(config.temp_n)
        self.message = 'Successfully updated secure data.'

class Wallet():
    def __init__(self, name, passw, seed, privkey='none'):
        self.name = str(name)
        self.pas = str(passw)
        self.seed = str(seed)
        self.pkey = str(privkey)
