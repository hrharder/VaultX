#!/usr/bin/python3
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/
import sys, os
import pyperclip as pyp
import tkinter as tk
from tkinter import* as tk# W, END, SINGLE, Button, Frame, Entry, Button, Toplevel
import csv, sys, os
import pickle as 
import config

class MainApp(Frame):
	def __init__(self, parent, bag):
		Frame.__init__(self, parent)
		self.parent = parent
		self.option = tk.IntVar()
		self.pack()
		self.bag = bag
		option_list = ['none', 'Password', 'Seed', 'Private Key']
		wallet_list = list(self.bag.wallets.keys())
		self.listbox = None
		self.make_widgets(option_list, wallet_list)

	def make_widgets(self, option_list, wallet_list):
		self.winfo_toplevel().title('VaultX Alpha')
		listbox = tk.Listbox(self)
		self.listbox = listbox
		for i in range(1, len(option_list)):
			tk.Radiobutton(self, text=option_list[i], variable=self.option, value=i).pack(anchor=W)
		for i in wallet_list:
			listbox.insert(END, i)
		self.listbox.bind('<<ListboxSelect>>', self.cur_select)
		self.listbox.pack()

	def cur_select(self, evt):
		value=self.listbox.get(self.listbox.curselection())
		int_option = self.option.get()
		if int_option == 1:
			pyp.copy(self.bag.wallets[value].pas)
		elif int_option == 2:
			pyp.copy(self.bag.wallets[value].seed)
		elif int_option == 3:
			pyp.copy(self.bag.wallets[value].pkey)

	#TODO: Add ability to add new wallets from in app
	#def gui_add_wallet(self):
	#	wallet_add_window = Toplevel(self.parent)
	#	name_entry = Entry(wallet_add_window)
	#	name_entry.pack()


class new_wallet():
	def __init__(self, name, passw, seed, privkey = 'none'):
		self.name = str(name)
		self.pas = str(passw)
		self.seed = str(seed)
		self.pkey = str(privkey)
		return

class PassBag():
	def __init__(self, wallets=None):
		if type(wallets) == dict:
			self.wallets = wallets
		else:
			self.wallets = {}
		return

	def add(self, thiswallet):
		self.wallets[thiswallet.name] = thiswallet
		return 

def add_from_file(filename, pyname):
	try:
		pickle_file = open(pyname, 'rb')
		loaded_wallet = pickle.load(pickle_file, pickle.HIGHEST_PRO)
		bag = PassBag(loaded_wallet)
		print('Succesfully imported data.')
		print('Skipped readfile, data loaded from secure file.')
		return bag
	except:
		with open(filename, 'r') as csvfile:
			dicreader = csv.reader(csvfile)
			bag = PassBag()
			for ls in dicreader:
				bag.add(new_wallet(ls[0],ls[1],ls[2]))

	object_file = open(py_name, 'wb+')
	pickle.dump(bag.wallets, object_file, protocol=4)
	object_file.close()
	return bag

if __name__ == '__main__':

	########
	########
	filepath = '/Volumes/Keys/VaultX/data/privdata.txt'
	py_name  = '/Volumes/Keys/VaultX/data/datas.pickle'
	########
	########

	bag = add_from_file(filepath, py_name)	
	main_tk = tk.Tk()
	main_app = MainApp(main_tk, bag)
    #main_app.gui_add_wallet()
	main_app.mainloop()

