#!/usr/bin/python3
# VaultX Alpha - Experimental (0.11)
# https://likegeeks.com/python-gui-examples-tkinter-tutorial
'''
# IDEAS
# - Create a root frame that launches before the main interface
#   that prompts for a simple password, which (attempts) to decrypt
#   pickle file with pyAesCrypt
#   (after this we will need to create a frame for the new user possibility)
#   - on launch, the program will hold the decrypted pickle file
#     as an attribute of the main_app class
'''
import pyperclip as pyp
import pyAesCrypt as pac
from tkinter import*
import csv
import sys
import os
import pickle
import config
os.chdir(config.data_dir)
class new_wallet():
    def __init__(self, name, passw, seed, privkey='none'):
        self.name = str(name)
        self.pas = str(passw)
        self.seed = str(seed)
        self.pkey = str(privkey)
        return

class MainApp(Frame):
    def __init__(self, parent, bag):
        Frame.__init__(self, parent)
        self.parent = parent
        self.option = IntVar()
        self.bag = bag
        self.subframes = []
        self.option_list = ['none', 'Password', 'Seed', 'Private Key']
        self.bsize = 64*1024
        self.wallet_list = None
        self.listbox = None
        self.data_obj = None
        self.temp_key = None
        self.main_gate()

    def main_gate(self):
        lock_window = Frame(self.parent)#nw)
        key_entry = Entry(lock_window, show='o')
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
            pac.decryptFile((config.data_dir+config.data_n), (config.data_dir+config.data_o), self.temp_key, self.bsize)
            try:
                pickle_file = open((config.data_dir+config.data_o), 'rb')
                loaded_wallet = pickle.load(pickle_file)
                bag = PassBag(loaded_wallet)
                print('Skipped readfile, data loaded from secure file.')
                self.bag = bag
                os.remove((config.data_dir+config.data_o))
            except:
                print('youfucked')
        except:
            print('this is not an error that should ever show')
            return
        lock_window.destroy()
        #self.temp_key = None
        self.make_widgets(self.option_list)

    def make_widgets(self, option_list):
        wallet_list = list(self.bag.wallets.keys())
        self.winfo_toplevel().title('VaultX Alpha (0.3)')
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
        button_frame.pack(fill=X)
        new_wallet = Button(option_frame, text='Add New Wallet',command=self.gui_add_wallet)
        remove_wallet = Button(option_frame, text='Remove Selected Wallet', command=lambda: self.gui_delete_wallet())
        copy = Button(option_frame, text='Copy Information',command=lambda: self.copy_data())
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
        value = self.listbox.get(self.listbox.curselection())
        int_option = self.option.get()
        if int_option == 1:
            pyp.copy(self.bag.wallets[value].pas)
        elif int_option == 2:
            pyp.copy(self.bag.wallets[value].seed)
        elif int_option == 3:
            pyp.copy(self.bag.wallets[value].pkey)

    def cur_select(self):
        return self.listbox.get(self.listbox.curselection())

    def make_pickle(self):
        object_file = open('temp', 'wb+')
        pickle.dump(self.bag.wallets, object_file, protocol=4)
        object_file.close()
        pac.encryptFile('temp', conig.data_n, self.temp_key, self.bsize)
        os.remove('temp')

    def gui_new_wallet(self, n, ps, sd, pk, window):
        thiswallet = new_wallet(n, ps, sd, pk)
        self.bag.add(thiswallet)
        window.destroy()
        self.listbox.delete(0, END)
        for i in self.subframes:
            i.destroy()
        self.wallet_list = list(self.bag.wallets.keys())
        self.make_widgets(self.option_list)
        self.make_pickle()

    def gui_delete_wallet(self):
        wallet = self.listbox.get(self.listbox.curselection())
        self.bag.remove(wallet)
        self.listbox.delete(0, END)
        for i in self.subframes:
            i.destroy()
        self.wallet_list = list(self.bag.wallets.keys())
        self.make_widgets(self.option_list)
        self.make_pickle()

    def gui_add_wallet(self):
        wallet_add_window = Toplevel(self.parent)
        wallet_add_window_frame = Frame(wallet_add_window)
        these_widgets = []
        wallet_add_window.geometry('200x300')
        name = Label(wallet_add_window, text='Name:',
                     anchor=W, justify=LEFT, padx=5, width=21)
        name_entry = Entry(wallet_add_window)
        these_widgets.append(name)
        these_widgets.append(name_entry)
        pas = Label(wallet_add_window, text='Password:',
                    anchor=W, justify=LEFT, padx=5, width=21)
        pas_entry = Entry(wallet_add_window)
        these_widgets.append(pas)
        these_widgets.append(pas_entry)
        seed = Label(wallet_add_window, text='Seed:',
                     anchor=W, justify=LEFT, padx=5, width=21)
        seed_entry = Entry(wallet_add_window)
        these_widgets.append(seed)
        these_widgets.append(seed_entry)
        pkey = Label(wallet_add_window, text='Private Key:',
                     anchor=W, justify=LEFT, padx=5, width=21)
        pkey_entry = Entry(wallet_add_window)
        these_widgets.append(pkey)
        these_widgets.append(pkey_entry)
        new_wallet = Button(wallet_add_window, text='Add Wallet', command=lambda: self.gui_new_wallet(
            name_entry.get(), pas_entry.get(), seed_entry.get(), pkey_entry.get(), wallet_add_window))
        these_widgets.append(new_wallet)

        for i in these_widgets:
            i.pack()
        wallet_add_window_frame.mainloop()

class PassBag():
    def __init__(self, wallets={}):
        if type(wallets) == dict:
            self.wallets = wallets
        else:
            self.wallets = wallets
        return

    def add(self, thiswallet):
        self.wallets[thiswallet.name] = thiswallet
        return

    def remove(self, thiswallet):
        del self.wallets[thiswallet]


def add_from_file(filename, pyname):
    try:
        pickle_file = open(pyname, 'rb')
        loaded_wallet = pickle.load(pickle_file)
        bag = PassBag(loaded_wallet)
        print('Succesfully imported data.')
        print('Skipped readfile, data loaded from secure file.')
        return bag
    except:
        print('No data found, creating blank file.')
        print('Check "config.py" to ensure your data directory is correct.')

if __name__ == '__main__':
    
    bag = PassBag()#dd_from_file(config.file_path, config.pickle_path)
    main_tk = Tk()
    main_app = MainApp(main_tk, bag)
    main_app.mainloop()
