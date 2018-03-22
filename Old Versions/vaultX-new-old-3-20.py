#!/usr/bin/python3
# VaultX Beta (0.0.6)
# Version date: 20 March 2018
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
    - config:  containing file path and other config information
    - vault: secure class that handles encryption/decryption and storage of data
'''

import config
from vault import*

#:: Begin main class declarations

class MainApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.winfo_toplevel().title('VaultX Beta (0.0.6)')
        self.option_list = config.option_list
        self.verbose = StringVar()
        self.option = IntVar()
        self.bsize = 65536
        self.wallet_list = None
        self.listbox = None
        self.temp_key = None
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
        key_entry.grid(column=0, row=1, ipady=15, ipadx=30)
        button_frame.grid(column=0, row=2, pady=30)
        lock_window.grid(column=1, row=1)
        self.verbose.set('Enter password or create new Vault.')
        app_frame.pack(fill='both', expand=True)
        lock_window.mainloop()

    def unlock(self, parent, lock_window, key_entry, app_frame):
        self.vault.open(key_entry)
        self.verbose.set(self.vault.message)
        lock_window.destroy()
        app_frame.destroy()
        self.make_widgets(self.option_list)

    def new_vault(self, lock_window, key_entry, app_frame):
        self.vault = Vault()
        self.verbose.set('New vault created with password.')
        app_frame.destroy()
        self.make_widgets(self.option_list)

    def make_widgets(self, option_list):
        self.top_frame = Frame(self.parent)
        dapp_frame = Frame(self.top_frame)
        wallet_list = list(self.vault.wallets.keys())
        self.winfo_toplevel().title('VaultX 0.0.6')

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)

        dapp_frame.grid_columnconfigure(0)
        dapp_frame.grid_columnconfigure(1)

        right_frame = Frame(dapp_frame)
        left_frame = Frame(dapp_frame)

        button_frame = Frame(self.top_frame)
        message_frame = Frame(self.top_frame)

        button_frame.grid_columnconfigure(0)
        button_frame.grid_columnconfigure(1)
        button_frame.grid_columnconfigure(2)

        right_frame.grid_columnconfigure(0)

        left_frame.grid_columnconfigure(0)
        

        listbox = Listbox(right_frame)
        self.listbox = listbox

        listbox.grid(column=0, row=0)

        select_btns = []

        for i in range(1, len(option_list)):
            new_btn = Radiobutton(left_frame, text=option_list[i], variable=self.option, value=i)
            select_btns.append(new_btn)

        for i in wallet_list:
            listbox.insert(END, i)

        new_wallet = Button(button_frame, text='Add', command=self.gui_add_wallet)
        remove_wallet = Button(button_frame, text='Remove', command=lambda: self.gui_delete_wallet())
        copy = Button(button_frame, text='Copy Field', command=lambda: self.copy_data())

        new_wallet.grid(column=0, row=0, sticky=W)
        remove_wallet.grid(column=1, row=0, sticky=W)
        copy.grid(column=2, row=0, sticky=W)
        
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

    def copy_data(self):
        value = self.listbox.get(self.listbox.curselection())
        int_option = self.option.get()
        if int_option == 1:
            pyp.copy(self.vault.wallets[value].pas)
        elif int_option == 2:
            pyp.copy(self.vault.wallets[value].seed)
        elif int_option == 3:
            pyp.copy(self.vault.wallets[value].pkey)
        self.verbose.set('Sucessfully copied information.')

    def encrypt_data(self):
        self.vault.update_data()
        self.verbose.set(self.vault.message)
        return

    def gui_new_wallet(self, n, ps, sd, pk, window):
        thiswallet = Wallet(n, ps, sd, pk)
        self.vault.add(thiswallet)
        window.destroy()
        self.listbox.delete(0, END)
        self.top_frame.destroy()
        self.wallet_list = list(self.vault.wallets.keys())
        self.make_widgets(self.option_list)
        self.encrypt_data()
        return

    def gui_delete_wallet(self):
        wallet = self.listbox.get(self.listbox.curselection())
        self.vault.remove(wallet)
        self.listbox.delete(0, END)
        self.top_frame.destroy()
        self.wallet_list = list(self.vault.wallets.keys())
        self.make_widgets(self.option_list)
        self.encrypt_data()

    def gui_add_wallet(self):
        wallet_add_window = Toplevel(self.parent, bg='#222')
        wallet_add_window_frame = Frame(wallet_add_window)
        Label(wallet_add_window, text='Name:', bg='#111111', fg='#D7DDDC',bd=0, justify="left").grid(row=0)
        name_entry = Entry(wallet_add_window, bg='#555',fg='#D7DDDC',highlightbackground='#353B3C',
            highlightthickness='2',highlightcolor='#A3A3A3',bd=0)
        name_entry.grid(row=1)

        Label(wallet_add_window, text='Password:', bg='#222', fg='#D7DDDC').grid(row=2)
        pas_entry = Entry(wallet_add_window, bg='#555',fg='#D7DDDC',highlightbackground='#353B3C',
            highlightthickness='2',highlightcolor='#A3A3A3',bd=0)
        pas_entry.grid(row=3)

        Label(wallet_add_window, text='Seed:', bg='#222', fg='#D7DDDC').grid(row=4)
        seed_entry = Entry(wallet_add_window, bg='#555',fg='#D7DDDC',highlightbackground='#353B3C',
            highlightthickness='2',highlightcolor='#A3A3A3',bd=0)
        seed_entry.grid(row=5)

        Label(wallet_add_window, text='Private Key:', bg='#222', fg='#D7DDDC').grid(row=6)
        pkey_entry = Entry(wallet_add_window, bg='#555',fg='#D7DDDC',highlightbackground='#353B3C',
            highlightthickness='2',highlightcolor='#A3A3A3',bd=0)
        pkey_entry.grid(row=7)

        Button(wallet_add_window, text='Add Entry', bg='#222', highlightbackground='#222', command=lambda: 
                    self.gui_new_wallet(name_entry.get(), pas_entry.get(), 
                    seed_entry.get(), pkey_entry.get(), wallet_add_window)).grid(row=10)

        wallet_add_window_frame.mainloop()

# End class declarations

if __name__ == '__main__':
    os.chdir(config.data_dir)
    main_tk = Tk()
    main_app = MainApp(main_tk)
    main_app.mainloop()