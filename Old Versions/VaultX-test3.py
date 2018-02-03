#!/usr/bin/python3
#VaultX Alpha - Experimental (0.11)
#https://likegeeks.com/python-gui-examples-tkinter-tutorial
'''
#IDEAS
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
import csv, sys, os, pickle
import config

class MainApp(Frame):
	def __init__(self, parent, bag):
		Frame.__init__(self, parent)
		self.parent = parent
		self.option = IntVar()
		self.bag = bag
		self.subframes = []
		self.option_list = ['none', 'Password', 'Seed', 'Private Key']
		self.wallet_list = list(self.bag.wallets.keys())
		self.listbox = None
		self.datafile_name = config.pickle_name
		self.datafile_path = config.pickle_path#'/Volumes/Keys/VaultX/data/data.pickle.aes'
		#self.main_gate()#config.pickle_path
		self.make_widgets(self.option_list, self.wallet_list)
		#self.pack()

def make_widgets(self, option_list, wallet_list):
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
			new_btn = Radiobutton(option_frame, text=option_list[i], variable=self.option, value=i)
			select_btns.append(new_btn)
		for i in wallet_list:
			listbox.insert(END, i)
		button_frame.pack(fill=X)
		new_wallet = Button(option_frame, text='Add New Wallet', command=self.gui_add_wallet)
		remove_wallet = Button(option_frame, text='Remove Selected Wallet', command=lambda: self.gui_delete_wallet())
		copy = Button(option_frame, text='Copy Information', command=lambda: self.cur_select())
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
		value=self.listbox.get(self.listbox.curselection())
		int_option = self.option.get()
		if int_option == 1:
			pyp.copy(self.bag.wallets[value].pas)
		elif int_option == 2:
			pyp.copy(self.bag.wallets[value].seed)
		elif int_option == 3:
			pyp.copy(self.bag.wallets[value].pkey)

	def cur_select2(self):
		return self.listbox.get(self.listbox.curselection())
		
	def make_pickle(self):
		object_file = open(config.pickle_path, 'wb+')
		pickle.dump(bag.wallets, object_file, protocol=4)
		object_file.close()

	def gui_new_wallet(self, n, ps, sd, pk, window):
		thiswallet = new_wallet(n, ps, sd, pk)
		self.bag.add(thiswallet)
		window.destroy()
		self.listbox.delete(0, END)
		for i in self.subframes:
			i.destroy()
		self.wallet_list = list(self.bag.wallets.keys())
		self.make_widgets(self.option_list, self.wallet_list)
		self.make_pickle()

	def gui_delete_wallet(self):
		wallet = self.listbox.get(self.listbox.curselection())
		self.bag.remove(wallet)
		self.listbox.delete(0, END)
		for i in self.subframes:
			i.destroy()
		self.wallet_list = list(self.bag.wallets.keys())
		self.make_widgets(self.option_list, self.wallet_list)
		self.make_pickle()

	def gui_add_wallet(self):
		wallet_add_window = Toplevel(self.parent)
		wallet_add_window.geometry('200x300')
		name = Label(wallet_add_window, text='Name:', anchor=W, justify=LEFT, padx=5, width=21)
        #name.pack()
		name_entry = Entry(wallet_add_window)
		#name_entry.pack()
		pas = Label(wallet_add_window, text='Password:', anchor=W, justify=LEFT, padx=5, width=21)
        #pas.pack()
		pas_entry = Entry(wallet_add_window)
		#pas_entry.pack()
		seed = Label(wallet_add_window, text='Seed:', anchor=W, justify=LEFT, padx=5, width=21)
        #seed.pack()
		seed_entry = Entry(wallet_add_window)
		#seed_entry.pack()
		pkey = Label(wallet_add_window, text='Private Key:', anchor=W, justify=LEFT, padx=5, width=21)
        #pkey.pack()
		pkey_entry = Entry(wallet_add_window)
        #pkey_entry.pack()
        new_wallet = Button(wallet_add_window, text='Add Wallet', command=lambda: self.gui_new_wallet(name_entry.get(), pas_entry.get(), seed_entry.get(), pkey_entry.get(), wallet_add_window))
        #new_wallet.pack()
        wallet_add_window.pack()
		wallet_add_window.mainloop()

	#def encript_data(self, data, key): #TODO: encript/decrypt pickle file
	#	bufferSize = 64 * 1024
	#	password = "foopassword"
	#	pyAesCrypt.encryptFile("data.pickle", "data.pickle.aes", password, bufferSize)
	#	pyAesCrypt.decryptFile("data.pickle.aes", "dataout.txt", password, bufferSize)
	#	pass

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

