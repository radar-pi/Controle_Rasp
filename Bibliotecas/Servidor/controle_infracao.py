# -*- coding: utf-8 -*-
import random
def controle_infra():
	infracao1 = 0
	vm = int(random.randrange(20,150))
	vr = int(random.randrange(40,80,20))

	if vm >= 27 and vm <= 107:
		vc = vm - 7
	elif vm >= 108 and vm <= 121:
		vc = vm - 8
	elif vm >= 122 and vm <= 135:
		vc = vm - 9
	elif vm >= 136 and vm <= 150:
		vc = vm - 10
	elif vm >= 151 and vm <= 161:
		vc = vm - 11
	else:
		vc = vm

	vinte = int (vr + ((20*40)/100))	
	cinquenta = vr + ((50*40)/100)

	if  vc >= vr and vc <= vinte:
		infracao1 = 1
		penalidade = True

	elif vc > vinte and vc <= cinquenta:
		infracao1 = 2
		penalidade = True

	elif vc > cinquenta:
		infracao1 = 3
		penalidade = True
	else:
		infracao = 0
		penalidade = 0	
	lista = [vm, vc, infracao1, penalidade,vr]
	return lista

