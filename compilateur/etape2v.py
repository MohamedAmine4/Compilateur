# -*- coding: utf-8 -*-
"""
Created on Man Oct 28 12:40:11 2023
@author: Mohamed Amine Boussoualef
"""
# Import du module Python "re" pour les opérations de correspondance de motifs (expressions régulières)
import re
from aide import analyseur_lexical
# Liste des tokens réservés du langage que le programme analyse
TOKENS = ["program", "begin", "end", "read", "write", "if", "while", "(", ")"]

# Initialisation de l'indice du token actuel
i = 0

# Expressions régulières pour les identifiants et les nombres
ID = '[a-zA-Z][a-zA-Z_0-9]*'
NUM = '[0-9]+'


PROGRAM = ""
with open("MonCode.code", 'r') as f:
    for ligne in f:
        for lettre in ligne:
            if lettre == ";":
                PROGRAM += " ; "
            elif lettre == ",":
                PROGRAM += " , "
            elif lettre == "\n":
                PROGRAM += " "
            else:
                PROGRAM += lettre

# Suppression des commentaires
PROGRAM = re.sub("\(\*(.*?)\*\)", "", PROGRAM)
# Séparation des mots et réassemblage des différentes instructions
PROGRAM = PROGRAM.split(" ")
PROGRAM = [mot for mot in PROGRAM if mot != '']

#print(PROGRAM)
# Programme d'exemple à analyser (représentation simplifiée)
# Initialisation du token actuel
token = PROGRAM[0]

# Longueur du programme
length = len(PROGRAM)

# Fonction pour avancer au prochain token
def next_token():
    global i, token
    if i < (len(PROGRAM) - 1):
        i += 1
        token = PROGRAM[i]

# Fonction pour gérer les erreurs
def erreur(exp_token, given_token):
    print("ERREUR ", "expected: ", exp_token, " given: ", given_token)

# Fonction pour tester un token
def teste(test_token):
    if test_token == token or re.match(test_token, token):
        next_token()
        return 1
    else:
        erreur(test_token, token)
       # next_token()    cela en commentaire 

# Fonction pour gérer les constantes
def consts():
    teste("const")
    while re.match(ID, token) and token != 'var':
        teste(ID)
        teste("=")
        teste(NUM)
        teste(";")

# Fonction pour gérer les variables
var=[]
def Vars():
    teste("var")
    teste(ID)
    while token == ",":
        next_token()
        teste(ID)
    teste(";")
# Fonction pour gérer les facteurs
def fact():
    if re.match(ID, token) or re.match(NUM, token):
        next_token()
    else:
        teste("(")
        expr()
        teste(")")

# Fonction pour gérer les termes
def term():
    fact()
    while token in ["*", "/"]:
        next_token()
        fact()

# Fonction pour gérer les expressions
def expr():
    term()
    while token in ["+", "-"]:
        next_token()
        term()

# Fonction pour gérer les conditions
def cond():
    expr()
    if token in ["==", "<>", "<", ">", "<=", ">="]:
        next_token()
        expr()

# Fonction pour gérer les affectations
def affec():
    teste(ID)
    teste(":=")
    expr()

# Fonction pour gérer les instructions "if"
def si():
    teste("if")
    cond()
    teste("then")
    inst()

# Fonction pour gérer les boucles "while"
def tantQue():
    teste("while")
    cond()
    teste("do")
    inst()

# Fonction pour gérer les instructions "write"
def ecrire():
    teste("write")
    teste("(")
    expr()
    while token == ",":
        next_token()
        expr()
    teste(")")

# Fonction pour gérer les instructions "read"
def lire():
    teste("read")
    teste("(")
    teste(ID)
    while token == ",":
        next_token()
        teste(ID)
    teste(")")

# Fonction pour gérer les blocs d'instructions
def insts():
    teste("begin")
    inst()
    while token == ";":
        next_token()
        inst()
    teste("end")

# Fonction pour gérer les instructions
def inst():
    if token == "if":
        si()
    elif token == "while":
        tantQue()
    elif token == "begin":
        insts()
    elif token == "write":
        ecrire()
    elif token == "read":
        lire()
    elif re.match(ID, token) and token not in TOKENS:
        affec()

# Fonction pour gérer les blocs de code
def block():
    if token == "const":
        consts()
    if token == "var":
        Vars()
    insts()

# Fonction pour gérer le programme principal
def program():
    teste("program")
    teste(ID)
    teste(";")
    block()
    if token != ".":
        erreur(".", token)

# Appel de la fonction principale pour analyser le programme
program()
