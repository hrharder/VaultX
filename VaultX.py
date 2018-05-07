#!/usr/local/bin/python3
# VaultX (0.1.2)
# Version date: 5 May 2018
# By Henry Harder
# All Rights Reserved (2018)

'''
Dependant modules (must be installed to function):
    1) pyperclip: used to copy data to the clipboard
    2) pyAesCrypt: used to securely encrypt all user data
    3) pickle: the data structure used to store user data, using a
       popular object storage protocol called pickle. This pickle object
       is what is encrypted and stored in the users specified directory.

    --- (the ones below should come pre-installed with Python 3+) ----

    4) tkinter: used to create the gui
    5) sys: interface with user system
    6) os: used to change directory
'''

import pyperclip as pyp
import pyAesCrypt as pac
from tkinter import*
import sys, os, pickle

'''
Custom modules: (written for this program)
    - config:  containing file path and other config information that users can and should modify
    - vault: secure class that handles encryption/decryption and storage of data
'''

import config
from vault import*

# Begin main class declarations

class VaultX(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.winfo_toplevel().title('VaultX (0.1.2)')
        self.option_list = config.option_list
        self.verbose = StringVar()
        self.option = IntVar()
        self.vault = Vault()
        self.text_widget = None
        self.top_frame = None
        self.main_gate()

    def main_gate(self):
        app_frame = Frame(self.parent)
        lock_window = Frame(app_frame)
        button_frame = Frame(lock_window)

        self.text_widget = Label(lock_window, textvariable=self.verbose, anchor=W)
        key_entry = Entry(lock_window, show='*',justify='center')

        unlock_btn = Button(button_frame, text='Unlock Existing Vault',
            command=lambda: self.unlock(self.parent, lock_window, key_entry, app_frame))
        new_wallet_btn = Button(button_frame, text='Encrypt New Vault',
            command=lambda: self.new_vault(lock_window, key_entry, app_frame))

        app_frame.grid_rowconfigure(0, weight=1)
        app_frame.grid_rowconfigure(2, weight=1)
        app_frame.grid_columnconfigure(0, weight=1)
        app_frame.grid_columnconfigure(2, weight=1)

        lock_window.grid_columnconfigure(0, weight=1)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)

        unlock_btn.grid(column=0, row=0, padx=5, pady=5)
        new_wallet_btn.grid(column=1, row=0, padx=5, pady=5)
        self.text_widget.grid(column=0, row=0, padx=5, pady=10)
        key_entry.grid(column=0, row=1, ipady=10, ipadx=10)
        button_frame.grid(column=0, row=2, pady=10)
        lock_window.grid(column=1, row=1)

        self.verbose.set('Enter password or create new Vault.')

        app_frame.pack(fill='both', expand=True)
        lock_window.mainloop()

    def unlock(self, parent, lock_window, key_entry, app_frame):
        if self.vault.open(key_entry) == 1:
            self.verbose.set(self.vault.message)
            lock_window.destroy()
            app_frame.destroy()
            self.make_widgets(self.option_list)
        else:
            self.verbose.set(self.vault.message)
            return

    def new_vault(self, lock_window, key_entry, app_frame):
        self.vault = Vault()
        while len(key_entry.get()) < 4:
            self.verbose.set('Please enter a longer encryption key.')
            return
        self.verbose.set('New vault created with password.')
        app_frame.destroy()
        self.make_widgets(self.option_list)

    def make_widgets(self, option_list):
        self.winfo_toplevel().title('VaultX 0.0.6')

        self.top_frame = Frame(self.parent,pady=5, padx=5)
        dapp_frame = Frame(self.top_frame)


        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)

        right_frame = Frame(dapp_frame, pady=5, padx=5)
        left_frame = Frame(dapp_frame, pady=5, padx=5)

        button_frame = Frame(self.top_frame)
        message_frame = Frame(self.top_frame)

        listbox = Listbox(right_frame)
        listbox.grid(column=0, row=0)
        select_btns = []

        for i in range(1, len(option_list)):
            new_btn = Radiobutton(left_frame, text=option_list[i], variable=self.option, value=i)
            select_btns.append(new_btn)

        for i in list(self.vault.wallets.keys()):
            listbox.insert(END, i)

        new_wallet = Button(button_frame, text='Create Entry', command=self.gui_add_wallet)
        remove_wallet = Button(button_frame, text='Remove Entry', command=lambda: self.gui_delete_wallet(listbox))
        copy = Button(button_frame, text='Copy Data', command=lambda: self.copy_data(listbox))
        display = Button(button_frame, text='Display Data', command=lambda: self.display_data(listbox))

        new_wallet.grid(column=0, row=0, sticky=E)
        remove_wallet.grid(column=1, row=0, sticky=W)
        copy.grid(column=0, row=1, sticky=E)
        display.grid(column=1, row=1, sticky=W)

        for i in range(len(select_btns)):
            select_btns[i].grid(column=0, row=i, sticky=W)

        button_frame.grid(column=0, row=1)

        self.text_widget = Label(message_frame, textvariable=self.verbose)
        self.text_widget.grid(sticky=S)
        message_frame.grid(column=0, row=2)

        left_frame.grid(column=0, row=0)
        right_frame.grid(column=1, row=0)

        dapp_frame.grid(column=0, row=0)
        button_frame.place()

        self.top_frame.pack(expand=True, fill='both')
        self.top_frame.mainloop()

    def copy_data(self, listbox):
        yes_msg = 'Sucessfully copied information.'
        no_msg = 'Please select an entry.'
        try:
            value = listbox.get(listbox.curselection())
            int_option = self.option.get()
            if int_option == 1:
                pyp.copy(self.vault.wallets[value].pas)
                self.verbose.set(yes_msg)
            elif int_option == 2:
                pyp.copy(self.vault.wallets[value].seed)
                self.verbose.set(yes_msg)
            elif int_option == 3:
                pyp.copy(self.vault.wallets[value].pkey)
                self.verbose.set(yes_msg)
            else:
                self.verbose.set(no_msg)
        except:
            self.verbose.set(no_msg)

    def display_data(self, listbox):
        try:
            value = listbox.get(listbox.curselection())
            int_option = self.option.get()
            if int_option == 1:
                self.verbose.set(self.vault.wallets[value].pas)
            elif int_option == 2:
                self.verbose.set(self.vault.wallets[value].seed)
            elif int_option == 3:
                self.verbose.set(self.vault.wallets[value].pkey)
        except:
            self.verbose.set('Please select an entry.')

    def encrypt_data(self):
        self.vault.update_data()
        self.verbose.set(self.vault.message)

    def gui_new_wallet(self, n, ps, sd, pk, window):
        self.vault.add(Wallet(n, ps, sd, pk))
        window.destroy()
        self.top_frame.destroy()
        self.make_widgets(self.option_list)
        self.encrypt_data()

    def gui_delete_wallet(self, listbox):
        try:
            self.vault.remove(listbox.get(listbox.curselection()))
            self.top_frame.destroy()
            self.make_widgets(self.option_list)
            self.encrypt_data()
        except:
            self.verbose.set('Please select an entry to remove.')

    def gui_add_wallet(self):
        wallet_add_window = Toplevel(self.parent)
        add_wallet_frame = Frame(wallet_add_window)

        Label(add_wallet_frame, text='Name:').grid(row=0)
        name_entry = Entry(add_wallet_frame)
        name_entry.grid(row=1)

        Label(add_wallet_frame, text='Password:').grid(row=2)
        pas_entry = Entry(add_wallet_frame)
        pas_entry.grid(row=3)

        Label(add_wallet_frame, text='Seed:').grid(row=4)
        seed_entry = Entry(add_wallet_frame)
        seed_entry.grid(row=5)

        Label(add_wallet_frame, text='Private Key:').grid(row=6)
        pkey_entry = Entry(add_wallet_frame)
        pkey_entry.grid(row=7)

        Button(add_wallet_frame, text='Add Entry', command=lambda:
                    self.gui_new_wallet(name_entry.get(), pas_entry.get(),
                    seed_entry.get(), pkey_entry.get(), wallet_add_window)).grid(row=10)

        add_wallet_frame.pack(expand=True, fill='both')
        add_wallet_frame.mainloop()

# End main class declarations

# Begin main loop

if __name__ == '__main__':
    os.chdir(config.data_dir)
    main_gui = VaultX(Tk())
    main_gui.mainloop()

# End main loop
