#!/usr/bin/env python
import os
from . import pimp
import click as C

@C.group()
def cli():
	"""
	help for this
	"""
	pass

@C.command()
@C.argument('path',required=True,type=str)
def find_master(path):
	"""
	find master pkg
	"""
	C.echo(pimp.find_masterpkg(path))
	
@C.command()
@C.argument('path',required=True,type=str)
def show(path) -> None:
	"""
	display all imports for every script in master package
	"""
	pimp.show(path)

@C.command()
@C.argument('path',nargs=-1, required=True,type=str)
def loc(path) -> None:
	"""
	display all imports for every script in master package
	"""
	for p in path:
		pimp.loc(p)
	
cli.add_command(show)
cli.add_command(find_master)
cli.add_command(loc)