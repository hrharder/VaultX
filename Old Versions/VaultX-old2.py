#!/usr/bin python3

import sys, os
import pyperclip as pyp
import tkinter as tk
from tkinter import W, END, SINGLE
import csv 

class new_wallet():
	def __init__(self, name, passw, seed, privkey = 'none'):
		self.name = str(name)
		self.pas = str(passw)
		self.seed = str(seed)
		self.pkey = str(privkey)
		return

	def key(self):
		print(self.pas)
		return

	def seed(self):
		print(self.seed)
		return

class PassBag():
	def __init__(self):
		self.wallets = {}
		return

	def add(self, thiswallet):
		self.wallets[thiswallet.name] = thiswallet
		return

	def add_from_file(self, filename):
		with open(filename, 'r') as csvfile:
			dicreader = csv.reader(csvfile)
			for ls in dicreader:
				bag.add(new_wallet(ls[0],ls[1],ls[2]))

if __name__ == '__main__':
	bag = PassBag()
	########
	########
	filepath = '/Volumes/Keys/VaultX/data/privdata.txt'
	########
	# Change to your private data file
	########

	bag.add_from_file(filepath)
	main = tk.Tk()
	main.title='Vault x (0.0)'
	option = tk.IntVar()

	option_list = ['null', 'Password', 'Seed', 'Private Key']
	wallet_list = list(bag.wallets.keys())

	def ButtonCmd(i):
		int_option = i 

	def CurSelect(evt):
		value=mylistbox.get(mylistbox.curselection())
		int_option = option.get()
		if int_option == 1:
			pyp.copy(bag.wallets[value].pas)
		elif int_option == 2:
			pyp.copy(bag.wallets[value].seed)
		elif int_option == 3:
			pyp.copy(bag.wallets[value].pkey)

	mylistbox = tk.Listbox(main)
	mylistbox.bind('<<ListboxSelect>>', CurSelect)

	for i in range(1, len(option_list)):
		tk.Radiobutton(main, text=option_list[i], variable=option, value=i).pack(anchor=W)

	for i in wallet_list:
		mylistbox.insert(END, i)

	mylistbox.pack()
	main.mainloop()

