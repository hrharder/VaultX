""""
Henry Harder (c)
February 2018 (Ideas for VaultX)

Notes:
    The idea is that this module acts as a digital gate in the
    sense that the only time the sensitive data, including:
    - the pre-salt password string
    - the decrypted pickle file that contains the secure object
"""
import pyAesCrypt as pac
import hashlib
import base64
import uuid
import config
import random
from VaultX import*
from tkinter import*

class Gate():

    def __init__(self, parent, bag, top):
        self.parent = parent
        self.option = IntVar()
        self.bsize = 64*1024
        self.temp_key = None
        self.top = top
        self.make_widgets()
    
    def make_widgets(self):
        lock_window = Frame(self.parent)
        key_entry = Entry(lock_window, show='*')
        key_entry.pack()
        unlock_btn = Button(lock_window, text='Unlock',
            command=lambda: self.unlock(lock_window, key_entry))
        unlock_btn.pack()
        lock_window.pack()
        lock_window.mainloop()

    def unlock(self, lock_window, key_entry):
        out_file = None
        self.temp_key = "".join(key_entry.get())
        try:
            pac.decryptFile(config.data_n, config.data_o, self.temp_key, self.bsize)
            try:
                pickle_file = open(config.data_o, 'rb')
                loaded_wallet = pickle.load(pickle_file)
                bag = PassBag(loaded_wallet)
                print('Skipped readfile, data loaded from secure file.')
                self.bag = bag
                os.remove(config.data_o)
            except:
                print('Error')
        except:
            print('You probably messed up your password.')
            return
        lock_window.destroy()
        self.main_widgets()


    def main_widgets(self):
        wallet_list = list(self.bag.wallets.keys())
        select_frame = Frame(self.parent)
        self.top.subframes.append(select_frame)
        button_frame = Frame(select_frame)
        self.top.subframes.append(button_frame)
        option_frame = Frame(select_frame)
        self.top.subframes.append(option_frame)
        listbox = Listbox(button_frame)
        select_btns = []
        self.top.listbox = listbox
        for i in range(1, len(config.option_list)):
            new_btn = Radiobutton(option_frame, text=config.option_list[i],
                                      variable=self.option, value=i)
            select_btns.append(new_btn)
        for i in wallet_list:
            listbox.insert(END, i)
        button_frame.pack(fill=X)
        new_wallet = Button(option_frame, text='Add New Wallet',
                                command=self.top.gui_add_wallet)
        remove_wallet = Button(option_frame, text='Remove Selected Wallet',
                               command=lambda: self.top.gui_delete_wallet())
        copy = Button(option_frame, text='Copy Information',
                      command=lambda: self.copy_data())
        select_frame.columnconfigure(0, weight=1)
        select_frame.columnconfigure(1, weight=1)
        button_frame.grid(column=1)
        option_frame.grid(column=0, row=0)
        button_frame.columnconfigure(0, weight=1)
        for i in range(len(select_btns)):
            select_btns[i].grid(column=0, row=i, sticky=W)
        listbox.grid(column=0)
        copy.grid(row=3, column=0, sticky=W)
        new_wallet.grid(row=4, column=0, sticky=W)
        remove_wallet.grid(row=5, column=0, sticky=W)
        select_frame.pack()

    def copy_data(self):
        value = self.top.listbox.get(self.top.listbox.curselection())
        int_option = self.option.get()
        if int_option == 1:
            pyp.copy(self.top.bag.wallets[value].pas)
        elif int_option == 2:
            pyp.copy(self.top.bag.wallets[value].seed)
        elif int_option == 3:
            pyp.copy(self.top.bag.wallets[value].pkey)

    def make_pickle(self):
        object_file = open(config.temp_n, 'wb+')
        pickle.dump(self.top.bag.wallets, object_file, protocol=4)
        object_file.close()
        pac.encryptFile(config.temp_n, config.data_n, self.temp_key, self.bsize)
        os.remove(config.temp_n)
