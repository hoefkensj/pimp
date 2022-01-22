#!/usr/bin/env python
import os
import colorama
import pimp.lib as lib
Fore			=			colorama.Fore
Style			=			colorama.Style
pkg				=			lib.pkg.pkg

def lsR(cd,pyscrs_all):
	dirs_nodots										=		[d for d in lib.fs.ls_dirs(cd) if not os.path.split(d)[1].startswith('.')]
	dirs_nodots_nopycache					=		[d for d in dirs_nodots if not os.path.split(d)[1]						==	'__pycache__']
	dirs_nodots_nopycache_novenv	=		[d for d in dirs_nodots_nopycache if not os.path.split(d)[1]	==	'venv']
	pyscrs_all+= [os.path.join(cd, file) for file in lib.fs.ls_files(cd) if pkg.is_module(file)]
	for dir in dirs_nodots_nopycache_novenv:
		lsR(dir,pyscrs_all)
	return pyscrs_all

def find_masterpkg(path):
	masterpkg=pkg.find_masterpkg(path)
	return masterpkg

def show(cd='.'):
	path=pkg.find_masterpkg(cd)
	all_py=lsR(path,[])
	lines=[]
	files=[]
	lst_path_base=path.split('/')
	newfile=True
	lib_py={}
	colorhl={
		'from'		:			f'{Fore.LIGHTBLUE_EX}from{Style.RESET_ALL}'		,
		'import'	: 		f'{Fore.BLUE}import{Style.RESET_ALL}'					,
		'as'			:			f'{Fore.GREEN}as{Style.RESET_ALL}' 				,
		'dot'			:			f'{Fore.LIGHTGREEN_EX}.{Style.RESET_ALL}' 				,
	}
	for idx,py in enumerate(all_py):
		filenr=idx+1
		#print(py,':\t')
		shortpath= os.path.join('~','/'.join([d for d in py.split('/') if d not in lst_path_base]))
		lines+=[f'{filenr}:\t{shortpath}']
		files+=[[f'{filenr}:\t{shortpath}'],]
		n=0
		s=0
		i=0
		with open(py,'r') as f:
			contents= f.readlines()
		file={
			'idx' : idx,
			'path' : shortpath,
			'contents' : contents,
			}
		lib_py[py]=file
		

		
	for py in all_py:
		error=False
		print(lib_py[py]['idx'],lib_py[py]['path'])
		if os.path.split(lib_py[py]['path'])[1][:-3]== '__init__':
			for line in lib_py[py]['contents']:
				line=line.strip()
				line=line.split(' ')
				if line[0] == 'import':
					error=True
					
				for idx,item in enumerate(line):
					if item == 'from':
						item =  colorhl['from']
					elif item == 'import':
						item =  colorhl['import']
					elif item == 'as':
						item =  colorhl['as']
					elif item == '.':
						item	=	colorhl['dot']
				line[idx]=item
				line=' '.join(line)
				if error :
					line=f"\033[0E{Fore.RED}ERROR:\t{Style.RESET_ALL}{line}"
				print(f'\t|- {line}')
		# if len(lib_py[py]['contents']) > 0:
		# 	print(f"\t{Fore.LIGHTCYAN_EX}{lib_py[py]['contents'][0].strip()}{Style.RESET_ALL}")
		for line in lib_py[py]['contents']:
			if line.startswith('import') or line.startswith('from'):
				line=line.strip()
				line=line.split(' ')
				for idx,item in enumerate(line):
					if item == 'from':
						item =  colorhl['from']
					if item == 'import':
						item =  colorhl['import']
					if item == 'as':
						item =  colorhl['as']
					line[idx]=item
				line=' '.join(line)
				print(f'\t|- {line}')



				
		# for line in lines:
		# 	started=False
		# 	if line.startswith('#!') :
		# 		files[idx] += [f'{Fore.LIGHTCYAN_EX}{line.strip()}{Style.RESET_ALL}']
		# 		s+=1
		# 		started=True
		# 		newfile=False
		#
		# 	if newfile:
		# 		files[idx]+=[f'{Fore.RED}[WARNING]{Style.RESET_ALL} : #! MISSING']
		# 		newfile=False
		#

def loc(cd):
	path=pkg.find_masterpkg(cd)
	all_py=lsR(path,[])
	totloc=0
	subloc=0
	lines=[]
	files=[]
	lst_path_base=path.split('/')
	lib_py={}
	colorhl={
		'from'		:			f'{Fore.LIGHTBLUE_EX}from{Style.RESET_ALL}'		,
		'import'	: 		f'{Fore.BLUE}import{Style.RESET_ALL}'					,
		'as'			:			f'{Fore.GREEN}as{Style.RESET_ALL}' 				,
	}
	
	for idx,py in enumerate(all_py):
		filenr=idx+1
		#print(py,':\t')
		shortpath= os.path.join('~','/'.join([d for d in py.split('/') if d not in lst_path_base]))
		lines+=[f'{filenr}:\t{shortpath}']
		files+=[[f'{filenr}:\t{shortpath}'],]
		n=0
		s=0
		i=0
		with open(py,'r') as f:
			contents= f.readlines()
		file={
			'idx' : idx,
			'path' : shortpath,
			'contents' : contents,
			}
		lib_py[py]=file
		
	for py in all_py:
		print(lib_py[py]['idx'],lib_py[py]['path'])
		if len(lib_py[py]['contents']) > 0:
			print(f"Lines of code: {Fore.LIGHTCYAN_EX}{len(lib_py[py]['contents'])}{Style.RESET_ALL}")
			totloc+=len(lib_py[py]['contents'])
	print(f'TOTAL LINES OF CODE:{Fore.LIGHTGREEN_EX}{totloc}{Style.RESET_ALL}')

