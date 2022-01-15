#!/usr/bin/env python
import sys
import os
import types


def is_module(path) -> bool:
	"""
	checks if given path is a python module valid or not according to the following tests:
	True if (one or more of):
	-file and .py extention
	-file #! and python on its first line
	Note:
		-directories that end in .py return False
		-links to files that valid also return False
	Note2:
		-pyc returns False
	 
	:param path: path to the file for testing
	:return: Boolean :True for module false for anything else
	"""
	if not os.path.exists(path):
		ismodule		=	False
	elif not os.path.isfile(path):
		ismodule		=	False
	else:
		ismodule_py	= True if os.path.split(os.path.abspath(path))[1].split('.')[-1]=='py' else False
		with open(os.path.abspath(path),'r') as file:
			l0=file.readline()
		l0_hashbang	= True if l0.startswith('#!') else False
		l0_python		= True if 'python' in l0	else False
		ismodule		=	any([ismodule_py,l0_hashbang,l0_python])
		#True if True in [True for item in os.listdir(path) if  item == "__init__.py" ] else False
	return ismodule

def is_pkg(path):
	"""
	
	:param path: path to test for it being a python package (has __init__.py)
	:return: boolean (true for is package false if not )
	# True if True in [True for item in os.listdir(dirpath) if  item == "__init__.py" ] else False =>>>
	# test = any([True for item in os.listdir(dirpath) if  item == "__init__.py" ]) =>>>
	"""
	ispkg=False
	if not os.path.islink(path) and os.path.isdir(os.path.abspath(path)):
		ispkg= any(["__init__.py" in os.listdir(path)])
	return ispkg

def find_masterpkg():
	"""
	!!! warning breaks when __init__. is in everyfolder of the path up until /  !!!
	gets the folder(path) that is the highest up in the path that still is a python package
	"""
	path=sys.argv[0]
	lst_pdps=os.path.split(os.path.abspath(path))[0].split('/')
	os.chdir(os.path.split(sys.argv[0])[0])
	return [pkg[0] for pkg in ([path,is_pkg(path) ] for path in  ['/'.join(lst_pdps[:(len(lst_pdps)-idx)]) for idx, folder in enumerate(reversed(lst_pdps)) if os.path.exists('/'.join(lst_pdps[:(
		len(lst_pdps)-idx)]))][:-1])if pkg[1] == True][-1]

def pkg():
	pkg=types.SimpleNamespace()
	pkg.is_module					=	is_module
	pkg.is_pkg						=	is_pkg
	pkg.find_masterpkg		=	find_masterpkg
	return pkg
pkg=pkg()
	
