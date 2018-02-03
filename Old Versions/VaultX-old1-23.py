#!/usr/bin/python3
import sys, os
import pyperclip as pyp
import tkinter as tk
from tkinter import W, END, SINGLE, Button, Frame, Entry, Button, Toplevel
import csv 
import pickle

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
		loaded_wallet = pickle.load(pickle_file)
		bag = PassBag(loaded_wallet)
		print('Skipped readfile, data loaded from pickle')
		return bag
	except:
		pass

	with open(filename, 'r') as csvfile:
		dicreader = csv.reader(csvfile)
		bag = PassBag()
		for ls in dicreader:
			bag.add(new_wallet(ls[0],ls[1],ls[2]))

	object_file = open(py_name, 'wb+')
	pickle.dump(bag.wallets, object_file)
	object_file.close()
	return bag

if __name__ == '__main__':

	########
	########
	# IMPORTANT: Follow instructions in documentation to protect your data.
	#			 1. Change 'filepath' to your private, plaintext key file, written
	#            	in the format specified in the docs.
	#			 2. Once you run VaultX once with your private data in a text file.
	#				VaultX will create a secure data file for future use, and
	#				the unsecured text file can be removed from your computer,
	#				or stored in a secure, encrypted location for backup.
	########
	########
	filepath = '/Volumes/Keys/VaultX/data/privdata.txt'
	py_name  = '/Volumes/Keys/VaultX/data/datas.pickle'
	########
	########

	bag = add_from_file(filepath, py_name)	
	main_tk = tk.Tk()
	main_app = MainApp(main_tk, bag)
	main_app.mainloop()