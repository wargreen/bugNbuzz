#!/usr/bin/python3

# Copyright : Felix GENSOLLEN

# This file is part of BugnBuzz.
#
# BugnBuzz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BugnBuzz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BugnBuzz.  If not, see <https://www.gnu.org/licenses/>.


import jack
import os, sys
import time

from connection_list import ConnectionList

listedesconnections = ConnectionList()


if '--help' in sys.argv:
	print('Options :')
	print('    --connectonly	:	Refait les connections jack sans ouvrir reaper')



if not '--connectonly' in sys.argv:
	print("Lancement du logiciel d'enregistrement ...")

	os.popen('reaper -template Rec\\ BugNBuzz.RPP', 'r', 1)

	print("ok")

	time.sleep(5)

print('Connection des ports Jack..."')

listedesconnections.connect()


print('ok')
print('exit...')

