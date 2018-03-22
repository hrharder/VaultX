#!/usr/bin/python3
# VaultX Alpha - Experimental (0.4.2)
import pyperclip as pyp
import pyAesCrypt as pac
from tkinter import*
import csv
import sys
import os
import pickle
import config

from gate import Gate


class new_wallet():
    def __init__(self, name, passw, seed, privkey='none'):
        self.name = str(name)
        self.pas = str(passw)
        self.seed = str(seed)
        self.pkey = str(privkey)
        return

class PassBag():
    def __init__(self, wallets={}):
        self.wallets = wallets
        return

    def add(self, wallet):
        self.wallets[wallet.name] = wallet
        return

    def remove(self, wallet):
        del self.wallets[wallet]

class MainApp(Frame):
    def __init__(self, parent, bag):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.parent.geometry('{}x{}'.format(400, 200))
        self.winfo_toplevel().title('VaultX (Experimental)')
        self.bag = bag
        self.subframes = []
        self.option_list = config.option_list
        self.bsize = 64*1024
        self.wallet_list = None
        self.listbox = None
        door = Gate(self.parent, self.bag, self)

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


if __name__ == '__main__':
    os.chdir(config.data_dir)
    bag = PassBag()
    main_tk = Tk()
    main_app = MainApp(main_tk, bag)
    main_app.mainloop()
