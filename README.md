## VaultX
###### Locally encrypt and store private data on your machine.

I created this program to manage my private keys for my various cryptocurrency wallets, being frustrated with the software that was available, and not wanting to spend money on a hardware wallet.

___
##### Directions:

1. Install dependencies (see below)
2. Modify   ```config.py``` by replacing ```"/"``` in ```line 9``` with the full file path for a blank directory somewhere on your computer. This will be the data directory where VaultX stores your encrypted data.
3. Launch VaultX
	- Launch from command line: ```python3 VaultX.py```
	- Make VaultX.py executable with ```chmod``` ([here](https://en.wikibooks.org/wiki/Python_Programming/Creating_Python_Programs))
	- Package into EXE/.APP executable
		- [py2exe](http://www.py2exe.org/index.cgi/Tutorial) for Windows
		- [py2app](https://py2app.readthedocs.io/en/latest/) for macOS

4. The first time you launch VaultX, enter a secure password when promted and click ```"Create new Vault,"``` and that's it!

___
##### Required modules (from PyPI):

I recommend  running VaultX in a ```virtualenv``` running Python3.x with these dependencies installed.

- PyPerClip ([PyPI link](https://pypi.org/project/pyperclip/)): used to copy data to the clipboard. Install with:

	```pip install pyperclip```

- PyAesCrypt ([PyPI link](https://pypi.org/project/pyAesCrypt/)): used to encrypt and decrypt data using the AES-256-CBC standard. Install with:

	```pip intall pyAesCrypt```

___

##### Description/Specs:
- Two main python classes; one for handling encryption/decryption and file system access, and one for the VaultX GUI.
  - ```VaultX.py``` - main program, creates a simple GUI using the ```tkinter``` module bundled with Python3, allowing cross platform execution.
  - ```vault.py``` - encryption/decryption class that uses the following python modules:
  	- ```pickle``` - included with Python3.x, this is the data structure used to dump data into a local file.
  	- ```pyAesCrypt``` - uses industry-standard AES-256 encryption to secure private data file with your password.
  	- ```pyperclip``` - used to copy data to clipboard

___
