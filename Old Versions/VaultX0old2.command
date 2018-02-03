#!/usr/bin/env python3
import pyperclip as pyp
from appJar import gui

class new_wallet():
	def __init__(self, name, passw, seed = 'none', pkey = 'none'):
		self.name = str(name)
		self.pas = str(passw)
		self.seed = str(seed)
		if pkey != 'none':
			self.pkey = str(pkey)
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
'''
def run(bag):
	ask = 'Ready (see docs for usage): ' #TODO: write docs
	inp = input(ask)
	while inp != '.':
		if inp in bag.wallets.keys():
			pyp.copy(bag.wallets[inp].pas)
			print('Success')
		else:
			print('Wallet not found. Add wallet or try again: ')
		inp = input(ask)
	return
'''
if __name__ == "__main__":
    bag = PassBag()
    bag.add(new_wallet('EDEN', 'mT2<Pk7zT(E[Q:}1', 'fringe trial pledge drip crawl embark taxi copper laugh lizard chicken retire'))
    bag.add(new_wallet('BTC', 'fuh8BE5wjF', 'asthma describe pair enlist expire crash obscure misery throw since weird float'))
    bag.add(new_wallet('VTC', 'cRO2rpVWPFjYpM5m', 'member half host repeat beyond travel network vessel real camp odor perfect'))
    bag.add(new_wallet('LTC', '4/b7e]13ec0f6480Xe7', 'solution grunt orphan mirror casual garlic move segment evoke fine help lonely'))
    bag.add(new_wallet('ADA', '{jWRb5!o[fgb5@Q', 'cram cube crew amused speed trial second surprise spider quick strike owner'))
    bag.add(new_wallet('SIA','exotic inorganic space invoke mystery twice riots vixen bounced sample layout hectare earth nobody lower hippo liar hinder pinched react heels roster goblet firm bodies dwarf fishing thaw afraid'))
    #run(bag)


	app = gui()
	'''
	for i in bag.wallets:
		app.addButton(i, pyp.copy(bag.wallets[i].pas))
	'''

	wallet_name_list = list(bag.wallets.keys())
	app.addLabelOptionBox("Wallets", wallet_name_list)
	app.go()
