import pyperclip as pyp
class wallet():
	def __init__(self, name, passw, seed, pkey = 'none'):
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

def run(bag):
	ask = 'Ready: '
	inp = input(ask)
	while inp != '.':
		if inp in bag.wallets.keys():
			pyp.copy(bag.wallets[inp].pas)
		else:
			print('Wallet not found. Add wallet or try again')
		inp = input(ask)
	return

if __name__ == "__main__":
	bag = PassBag()
	bag.add(wallet(input('Ask (see docs for usage):'))
	run(bag)

