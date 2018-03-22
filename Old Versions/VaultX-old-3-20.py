#!/usr/bin/python3
# VaultX Alpha - test (0.4.3)
# By Henry Harder
# All Rights Reserved (2018)
'''
Prebuilt modules (must be installed to function):
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
Custom module:
    - config:  containing file path and other config information
'''

import config


#:: Begin main class declarations

class new_wallet():
    def __init__(self, name, passw, seed, privkey='none', notes='none'):
        self.name = str(name)
        self.pas = str(passw)
        self.seed = str(seed)
        self.pkey = str(privkey)
        self.notes = str(notes)
        return

class Vault():
    def __init__(self, wallets={}):
        self.wallets = wallets
        return

    def add(self, wallet):
        self.wallets[wallet.name] = wallet
        return

    def remove(self, wallet):
        del self.wallets[wallet]

class MainApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.winfo_toplevel().title('VaultX Alpha')
        self.subframes = []
        self.option_list = config.option_list
        self.verbose = StringVar()
        self.option = IntVar()
        self.bsize = 65536 # 64*1024 Bytes - increase buffer size if necesary. 
        self.wallet_list = None
        self.listbox = None
        self.temp_key = None
        self.bag = None
        self.text_widget = None
        self.main_gate()

    def main_gate(self):
        app_frame = Frame(self.parent, bg='#222')#,bg='#222', width='500', height='500')
        lock_window = Frame(app_frame, bg='#222')#,bg='#222', align=C )
        button_frame = Frame(lock_window, bg='#222')
        self.parent.geometry('350x300')
        self.text_widget = Label(lock_window, textvariable=self.verbose,
            bg='#222', fg='#D7DDDC',bd=0,anchor=W)
        #self.text_widget.pack()
        key_entry = Entry(lock_window, show='*',bg='#555',fg='#D7DDDC',
            highlightbackground='#353B3C', highlightthickness='2',
            highlightcolor='#A3A3A3',bd=0, justify='center')
        #key_entry.pack()
        unlock_btn = Button(button_frame, text='Unlock Existing Vault',
            command=lambda: self.unlock(lock_window, key_entry),bg='#222', 
            highlightbackground='#222')
        new_wallet_btn = Button(button_frame, text='Encrypt New Vault', 
            command=lambda: self.new_vault(lock_window, key_entry),
            bg='#222', highlightbackground='#222')
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

    def unlock(self, lock_window, key_entry):
        self.temp_key = "".join(key_entry.get())
        try:
            pac.decryptFile(config.data_n, config.data_o,
                            self.temp_key, self.bsize)
            try:
                pickle_file = open(config.data_o, 'rb')
                loaded_wallet = pickle.load(pickle_file)
                bag = Vault(loaded_wallet)
                self.verbose.set('Data loaded from secure file.')
                self.bag = bag
                os.remove(config.data_o)
            except:
                self.verbose.set('Unexpected error')
                print('Unexpected error')
                return
        except:
            self.verbose.set('Incorrect password, or missing file.')
            return
        lock_window.destroy()
        self.verbose.set('Sucessfully unlocked.')
        self.make_widgets(self.option_list)

    def new_vault(self, lock_window, key_entry):
        self.temp_key = "".join(key_entry.get())
        new_bag = Vault()
        self.verbose.set('New bag created with password.')
        self.bag = new_bag
        lock_window.destroy()
        self.make_widgets(self.option_list)

    def make_widgets(self, option_list):
        wallet_list = list(self.bag.wallets.keys())
        self.winfo_toplevel().title('VaultX Alpha')
        select_frame = Frame(self.parent)
        self.subframes.append(select_frame)
        button_frame = Frame(select_frame)
        self.subframes.append(button_frame)
        option_frame = Frame(select_frame)
        self.subframes.append(option_frame)
        listbox = Listbox(button_frame)
        select_btns = []
        self.listbox = listbox
        for i in range(1, len(option_list)):
            new_btn = Radiobutton(option_frame, text=option_list[i],
                                  variable=self.option, value=i)
            select_btns.append(new_btn)
        for i in wallet_list:
            listbox.insert(END, i)
        new_wallet = Button(option_frame, text='Add New Wallet',
                            command=self.gui_add_wallet)
        remove_wallet = Button(
            option_frame, text='Remove Selected Wallet', 
            command=lambda: self.gui_delete_wallet())
        copy = Button(option_frame, text='Copy Information',
                      command=lambda: self.copy_data())
        select_frame.columnconfigure(0, weight=1)
        select_frame.columnconfigure(1, weight=1)
        select_frame.columnconfigure(2, weight=1)
        button_frame.grid(column=1)
        option_frame.grid(column=0, row=0)
        for i in range(len(select_btns)):
            select_btns[i].grid(column=0, row=i, sticky=W)
        listbox.grid(column=0)
        copy.grid(row=3, column=0, sticky=W)
        new_wallet.grid(row=4, column=0, sticky=W)
        remove_wallet.grid(row=5, column=0, sticky=W)
        self.text_widget = Label(button_frame, textvariable=self.verbose)
        self.text_widget.grid(row=6, column=0)
        select_frame.pack()

    def copy_data(self):
        value = self.listbox.get(self.listbox.curselection())
        int_option = self.option.get()
        if int_option == 1:
            pyp.copy(self.bag.wallets[value].pas)
        elif int_option == 2:
            pyp.copy(self.bag.wallets[value].seed)
        elif int_option == 3:
            pyp.copy(self.bag.wallets[value].pkey)
        self.verbose.set('Sucessfully copied information')

    def encrypt_data(self):
        object_file = open(config.temp_n, 'wb+')
        pickle.dump(self.bag.wallets, object_file, protocol=4)
        object_file.close()
        pac.encryptFile(config.temp_n, config.data_n,
                        self.temp_key, self.bsize)
        os.remove(config.temp_n)

    def gui_new_wallet(self, n, ps, sd, pk, window):
        thiswallet = new_wallet(n, ps, sd, pk)
        self.bag.add(thiswallet)
        window.destroy()
        self.listbox.delete(0, END)
        for i in self.subframes:
            i.destroy()
        self.wallet_list = list(self.bag.wallets.keys())
        self.make_widgets(self.option_list)
        self.encrypt_data()

    def gui_delete_wallet(self):
        wallet = self.listbox.get(self.listbox.curselection())
        self.bag.remove(wallet)
        self.listbox.delete(0, END)
        for i in self.subframes:
            i.destroy()
        self.wallet_list = list(self.bag.wallets.keys())
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