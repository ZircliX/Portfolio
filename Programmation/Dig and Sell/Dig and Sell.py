from random import *
import numpy as np
import pickle
from time import *

################################################################

def sauvegarde_save(inv, name, energie):
	path = "Saves/"+name+'.pkl'
	save = [inv, energie]
	with open(path, 'wb') as path:
		pickle.dump(save, path)

def sauvegarde_load(name):
	path = "Saves/"+name+'.pkl'
	with open(path, 'rb') as path:
		save = pickle.load(path)
	return save[0], save[1]

################################################################

def menu():
	debut = 0
	print("\nBienvenue à la grotte du Mont-Ku !\n")
	while debut != 1 and debut != 2:
		while True:
			try:
				debut = int(input("Êtes-vous un nouveau mineur :\n 1 - Oui (Nouvelle partie)\n 2 - Non (Reprendre une progression)\n"))
				break
			except:
				print("Choix non valide !\n")
	if debut == 2:
		while True:
			try:
				name = input("Quel est votre nom : ")
				if name == 'Quitter':
					break
				inv, energie = sauvegarde_load(name)
				break
			except:
				print("Erreur !")
		return inv, name, energie
	else:
		while True:
			try:
				name = input("Quel est votre nom : ")
				break
			except:
				print("Choix non valide !\n")
		inv = {'xp' : 0, 'lvl' : 0, 'Benny' : 0, 'ores' : {'Charbon' : 0, 'Fer' : 0, 'Cuivre' : 0, 'Or' : 0, 'Diamant' : 0, 'Rubis' : 0, 'Météore' : 0}, 'Force' : 0, 'Boisson' : 1}
		energie = 0
		sauvegarde_save(inv, name, energie)
		return inv, name, energie

def game(inv, name, energie):
	ore = ['Charbon','Fer','Cuivre','Or','Rubis','Diamant','Météore']
	while True:
		if inv['lvl'] == 0:
			proba = [0.4, 0.3, 0.15, 0.1, 0.035, 0.01, 0.005]
		elif inv['lvl'] == 1:
			proba = [0.38, 0.28, 0.145, 0.1, 0.045, 0.04, 0.01]
		elif inv['lvl'] == 2:
			proba = [0.36, 0.28, 0.14, 0.1, 0.055, 0.05, 0.015]
		elif inv['lvl'] == 3:
			proba = [0.34, 0.27, 0.135, 0.1, 0.065, 0.07, 0.02]
		elif inv['lvl'] == 4:
			proba = [0.32, 0.26, 0.13, 0.1, 0.075, 0.09, 0.025]
		elif inv['lvl'] == 5:
			proba = [0.3, 0.25, 0.125, 0.1, 0.085, 0.11, 0.03]
		elif inv['lvl'] == 6:
			proba = [0.28, 0.24, 0.12, 0.1, 0.095, 0.13, 0.035]
		elif inv['lvl'] == 7:
			proba = [0.26, 0.23, 0.115, 0.1, 0.105, 0.15, 0.04]
		elif inv['lvl'] == 8:
			proba = [0.24, 0.22, 0.11, 0.1, 0.115, 0.17, 0.045]
		elif inv['lvl'] == 9:
			proba = [0.22, 0.21, 0.105, 0.1, 0.125, 0.19, 0.05]
		elif inv['lvl'] == 10:
			proba = [0.2, 0.2, 0.1, 0.1, 0.135, 0.21, 0.055]
		try:
			entrée = int(input("Que voulez vous faire :\n 0 - Quitter\n 1 - Aller à la taverne\n 2 - Miner dans la grotte\n 3 - Voir son profil\n 4 - Utiliser un objet\n"))
		except:
			print("Choix non valide !\n")
		if entrée == 0:
			print('Fin de partie !')
			sauvegarde_save(inv, name, energie)
			break
		if entrée == 1:
			inv=shop(inv)
		elif entrée == 2:
			ore_p = np.random.choice(ore, p=proba)
			if energie >= 1 :
				reduc = (inv['Force']*0.05) + 0.05
			else:
				reduc = (inv['Force'])*0.05
			p,e='...','     '
			for i in range(3):
				print(e[:-(i+1)]+p[0:i+1]+"Minage"+p[0:i+1], end='\r')
				sleep(.8 - reduc)
			print(f"\nVous venez de miner 1 minerais de {ore_p} !")
			inv['ores'][ore_p] += 1
			inv = upgrade(inv, ore_p)
			if energie > 0:
				energie -= 1
				print(f"Coup(s) restants : {energie} !\n")
		elif entrée == 3:
			print(f"Voici la carte du mineur {name} :\n - Ce mineur possède {inv['Benny']} Bennies.\n - Son EXP est de : {inv['xp']} et est au niveau {inv['lvl']} !\n - Il possède {inv['Force']} amélioration(s) de pioche sur 14\n - Sac à dos : {inv['Boisson']} Boisson énergisante.\n - Coups restants de la boisson : {energie}\n")
			if inv['Force'] == 7:
				print(' Sa pioche est au niveau maximum !\n')
		elif entrée == 4:
			energie, inv = use_object(energie, inv)
		sauvegarde_save(inv, name, energie)

def upgrade(inv, ore):
	ores = ['Charbon', 'Fer', 'Cuivre', 'Or', 'Diamant', 'Rubis', 'Météore']
	exp = (5, 25, 35, 60, 125, 200, 500)
	inv['xp'] += exp[ores.index(ore)]
	print(f"Vous avez gagné {exp[ores.index(ore)]} d'exp\n")
	paliers = [0, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]
	for palier in paliers:
		if palier*2 >= inv['xp'] >= palier and int(inv['lvl']) < paliers.index(palier):
			print(f"Vous passez au niveau {paliers.index(palier)} !\n")
			inv['lvl'] = paliers.index(palier)
	if inv['lvl'] == paliers[-1]:
		print("Wouaw ! Quel mineur ... tu mérites un nerf-\n")
	return inv

def use_object(energie, inv):
	while True:
		try:
			consommable = int(input(f"Quel objet souhaitez-vous utiliser (0 --> Annuler) ?\n 1 - Boisson énergisante (accélère la vitesse de la pioche) : {inv['Boisson']} / "))
			nbr = int(input(" Combien voulez-vous en utiliser ?\n"))
			break
		except:
			print("Vous ne possédez pas cet objet !\n")
	if consommable == 1 and inv['Boisson'] >= nbr:
		for i in range(nbr):
			inv['Boisson'] -= 1
			energie += 20
		print(f'Vous utilisez {nbr} boisson(s) énergisante, vous vous sentez plus fort ({20*nbr} coups)\n')
	return energie, inv

def shop(inv):
	debut = -1
	print("Vous entrez dans la taverne de Tonton Bernard !\n")
	while debut != 0 and debut != 1 and debut != 2 and debut != 3:
		while True:
			try:
				debut = int(input("Que voulez-vous faire :\n 0 - Partir de la taverne\n 1 - Vendre des minerais\n 2 - Acheter des items\n"))
				break
			except:
				print("Choix non valide !\n")
	if debut == 0:
		return inv
	elif debut == 1:
		nbr, choix = 1, 1
		prix = [10, 50, 70, 120, 250, 400, 1000]
		while True:
			index = 0
			print("Vous avez :")
			for i in inv['ores']:
				esp = (11 - len(i)) * ' '
				print(f" {index+1} - {i} : {esp}{inv['ores'][i]} / {prix[index]}")
				index += 1
			while True:
				try:
					choix = int(input(f"\nQue voulez vous vendre (0 = Quitter) : "))
					nbr = int(input("Combien voulez vous en vendre : "))
					break
				except:
					print("Choix non valide !\n")
			if choix == 0 or nbr == 0:
				return inv
			if choix == 1:
				if nbr > inv['ores']['Charbon']:
					print("Vous n'avez pas assez de Charbon !\n")
				else:
					inv['ores']["Charbon"] -= nbr
					inv["Benny"] += 10*nbr
					print(f"Tu viens de vendre {nbr} Charbon pour {10*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 2:
				if nbr > inv['ores']['Fer']:
					print("Vous n'avez pas assez de Fer !\n")
				else:
					inv['ores']["Fer"] -= nbr
					inv["Benny"] += 50*nbr
					print(f"Tu viens de vendre {nbr} Fer pour {50*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 3:
				if nbr > inv['ores']['Cuivre']:
					print("Vous n'avez pas assez de Cuivre !\n")
				else:
					inv['ores']["Cuivre"] -= nbr
					inv["Benny"] += 70*nbr
					print(f"Tu viens de vendre {nbr} Cuivre pour {70*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 4:
				if nbr > inv['ores']['Or']:
					print("Vous n'avez pas assez d'Or !\n")
				else:
					inv['ores']["Or"] -= nbr
					inv["Benny"] += 120*nbr
					print(f"Tu viens de vendre {nbr} Or pour {120*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 5:
				if nbr > inv['ores']['Diamant']:
					print("Vous n'avez pas assez de Diamant !\n")
				else:
					inv['ores']["Diamant"] -= nbr
					inv["Benny"] += 250*nbr
					print(f"Tu viens de vendre {nbr} Diamant pour {250*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 6:
				if nbr > inv['ores']['Rubis']:
					print("Vous n'avez pas assez de Rubis !\n")
				else:
					inv['ores']["Rubis"] -= nbr
					inv["Benny"] += 400*nbr
					print(f"Tu viens de vendre {nbr} Rubis pour {400*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
			if choix == 7:
				if nbr > inv['ores']['Météore']:
					print("Vous n'avez pas assez de Météore !\n")
				else:
					inv['ores']["Météore"] -= nbr
					inv["Benny"] += 1000*nbr
					print(f"Tu viens de vendre {nbr} Météore pour {1000*nbr} Bennies !\nVous avez maintenant {inv['Benny']} Bennies !\n")
	elif debut == 2:
		achat = int()
		while True:
			try:
				achat = int(input(f"\nTonton Bernard : Voilà mon stock, fait gaffe je t'ai à l'oeil ... :\n(Tu as une bourse de {inv['Benny']} Bennies !) --- ( 0 = Quitter )\n     1 - Amélioration de pioche {inv['Force']*11**3} ({inv['Force']} / 14)\n     2 - Boisson énergisante 200 ({inv['Boisson']})\n"))
				nbr = int(input("Combien voulez vous en acheter : "))
			except:
				print("Choix non valide !\n")
			if achat == 1:
				if inv['Benny'] < nbr*(inv['Force']*11**3):
					print("\nTonton Bernard : T'as pas un sous ! Misérable ...")
				elif inv['Force']==14:
					print("Tonton Bernard : Mais j'ai plus rien moi arrête de m'embêter !")
				elif inv['Benny'] >= nbr*(inv['Force']*11**3) + inv['Force']*11 and inv['Force']<=13:
					for i in range(nbr):
						inv['Force'] += 1
						inv['Benny'] -= (inv['Force']-1)*11**3
					print(f"\nVous venez d'acheter {nbr} Amélioration(s) de pioche au Tonton Bernard pour {nbr*((inv['Force']-1)*11**3)} Bennies !")
			if achat == 0:
				return inv
			if achat == 2:
				if inv['Benny'] < nbr*200:
					print("\nTonton Bernard : T'as pas un sous ! Misérable ...")
				elif inv['Benny'] >= nbr*200:
					for i in range(nbr):
						inv['Boisson'] += 1
						inv['Benny'] -= 200
					print(f"Vous venez d'acheter {nbr} Boisson(s) énergisante au Tonton Bernard pour {200*nbr} Bennies !")

################################################################
if __name__ == '__main__':
	inv, name, energie = menu()
	game(inv, name, energie)