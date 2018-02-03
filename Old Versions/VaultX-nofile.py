#!/usr/bin/python3
#VaultX Alpha - Experimental (0.11)
#https://likegeeks.com/python-gui-examples-tkinter-tutorial
#IDEAS
# - 
import pyperclip as pyp
import pyAesCrypt as pac
from tkinter import*
import csv, sys, os, pickle
import config

class MainApp(Frame):
	def __init__(self, parent, bag):
		Frame.__init__(self, parent)
		self.parent = parent
		self.option = IntVar()#tk.IntVar()
		self.bag = bag
		self.widget_list = []
		self.option_list = ['none', 'Password', 'Seed', 'Private Key']
		self.wallet_list = list(self.bag.wallets.keys())
		self.listbox = None
		self.datafile_name = config.pickle_name
		self.datafile_path = config.pickle_path
		self.make_widgets(self.option_list, self.wallet_list)
		self.pack()

	def make_widgets(self, option_list, wallet_list):
		self.winfo_toplevel().title('VaultX Alpha (0.3)')
		listbox = Listbox(self)
		self.listbox = listbox
		for i in range(1, len(option_list)):
			new_btn = Radiobutton(self, text=option_list[i], variable=self.option, value=i)
			self.widget_list.append(new_btn)
			new_btn.pack(anchor=W)
		for i in wallet_list:
			listbox.insert(END, i)
		new_wallet = Button(self, text='Add New Wallet', command=self.gui_add_wallet)
		self.widget_list.append(new_wallet)
		new_wallet.pack()
		self.widget_list.append(listbox)
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

	def make_pickle(self):
		object_file = open(config.picklename, 'wb+')
		pickle.dump(bag.wallets, object_file, protocol=4)
		bject_file.close()

	def gui_new_wallet(self, n, ps, sd, pk, window):
		thiswallet = new_wallet(n, ps, sd, pk)
		self.bag.add(thiswallet)
		window.destroy()
		self.listbox.delete(0, END)
		for i in self.widget_list:
			i.destroy()
		self.wallet_list = list(self.bag.wallets.keys())
		self.make_widgets(self.option_list, self.wallet_list)
		make_pickle()

	def gui_add_wallet(self):
		wallet_add_window = Toplevel(self.parent)
		wallet_add_window.geometry('200x300')
		name = Label(wallet_add_window, text='Name:', anchor=W, justify=LEFT, padx=5, width=21)
		name.pack()
		name_entry = Entry(wallet_add_window)
		name_entry.pack()
		pas = Label(wallet_add_window, text='Password:', anchor=W, justify=LEFT, padx=5, width=21)
		pas.pack()
		pas_entry = Entry(wallet_add_window)
		pas_entry.pack()
		seed = Label(wallet_add_window, text='Seed:', anchor=W, justify=LEFT, padx=5, width=21)
		seed.pack()
		seed_entry = Entry(wallet_add_window)
		seed_entry.pack()
		pkey = Label(wallet_add_window, text='Private Key:', anchor=W, justify=LEFT, padx=5, width=21)
		pkey.pack()
		pkey_entry = Entry(wallet_add_window)
		pkey_entry.pack()
		new_wallet = Button(wallet_add_window, text='Add Wallet', command=lambda: self.gui_new_wallet(name_entry.get(), pas_entry.get(), seed_entry.get(), pkey_entry.get(), wallet_add_window))
		new_wallet.pack()
		wallet_add_window.mainloop()

	def gui_delete_wallet(self): #TODO: write GUI delete wallet function
		pass

	def encript_data(self, data, key): #TODO: encript/decrypt pickle file
		bufferSize = 64 * 1024
		password = "foopassword"
		pyAesCrypt.encryptFile("data.pickle", "data.pickle.aes", password, bufferSize)
		pyAesCrypt.decryptFile("data.pickle.aes", "dataout.txt", password, bufferSize)
		pass

	def decrypt_data(self, data, key):
		pass

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
		print('Succesfully imported data.')
		print('Skipped readfile, data loaded from secure file.')
		return bag
	except:
		with open(filename, 'r') as csvfile:
			dicreader = csv.reader(csvfile)
			bag = PassBag()
			for ls in dicreader:
				bag.add(new_wallet(ls[0],ls[1],ls[2]))
			make_pickle()
			return bag

if __name__ == '__main__':

	bag = add_from_file(config.file_path, config.pickle_path)	
	main_tk = Tk()
	main_app = MainApp(main_tk, bag)
	main_app.mainloop()

