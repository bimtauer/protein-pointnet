



# from pypdb.pypdb import *
from pypdb import *


pdb_file = get_pdb_file('4lza', filetype='cif', compression=True)
print(pdb_file[:200])