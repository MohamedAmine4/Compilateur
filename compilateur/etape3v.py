# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:39:25 2023
@author: Mohamed Amine Boussoualef
"""

# Import du module Python "re" pour les opérations de correspondance de motifs (expressions régulières)
import re

# Liste des tokens réservés du langage que le programme analyse
TOKENS = ["program", "begin", "end", "read", "write", "if", "while", "(", ")", "var"]

# Initialisation de l'indice du token actuel
i = 0

# Expressions régulières pour les identifiants (ID) et les nombres (NUM)
ID = '[a-zA-Z][a-zA-Z_0-9]*'
NUM = '[0-9]+'

# Programme d'exemple à analyser (représentation simplifiée)
PROGRAM = ["program", 'abc', ';', 'const', 'C', '=', '10', ';', 'D', '=', '8', ';', 'var', 'A', ',', 'B', ';',
          'begin',
          'A', ':=', '0', ';',
          'B', ':=', '0', ';',
          'while', 'A', '<>', '0', 'do',
          'begin',
          'read', '(', 'A', ')', ';',
          'B', ':=', 'A', '+', 'B', ';',
          'end', ';',
          "write", '(', 'B', ')', ';',
          'end', '.']

# Initialisation du token actuel
token = PROGRAM[0]

# Offset et TABLESYM pour gérer la table des symboles
offset = 0
TABLESYM = []

# Fonction pour entrer un symbole dans la table des symboles
def entrerSym(classe, value):
    global TABLESYM, offset
    if classe == 'constant':
        value = PROGRAM[i + 1]
    TABLESYM += [(PROGRAM[i - 1], classe, value)]
    offset += 1 

# Fonction pour chercher un symbole dans la table des symboles
def chercherSym(sym):
    global TABLESYM
    res = False
    for s in TABLESYM:
        if s[0] == sym:
            res = s
    if res:
        return res
    else:
        erreur_dec(sym)

# Fonction pour avancer au prochain token
def next_token():
    global i, token
    if i < (len(PROGRAM) - 1):
        i += 1
        token = PROGRAM[i]

# Fonction pour gérer les erreurs de déclaration
def erreur_dec(sym):
    print("variable {} not declared".format(sym))

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
        next_token()
        return 0

# Fonction pour tester un token et entrer le symbole dans la table des symboles
def test_et_entre(test_token, classe):
    global offset
    if teste(test_token) == 1:
        entrerSym(classe, value=offset)

# Fonction pour tester un token et chercher le symbole dans la table des symboles
def test_et_cherche(test_token):
    tok = token
    if teste(test_token) == 1:
        chercherSym(tok)

# Fonction pour gérer les constantes
def consts():
    teste("const")
    while re.match(ID, token) and token != 'var':
        test_et_entre(ID, "constant")
        teste("=")
        teste(NUM)
        teste(";")

# Fonction pour gérer les variables
def Vars():
    teste("var")
    test_et_entre(ID, 'variable')
    while token == ",":
        next_token()
        test_et_entre(ID, 'variable')
    teste(";")

# Fonction pour gérer les facteurs
def fact():
    if re.match(ID, token):
        test_et_cherche(ID)
    elif re.match(NUM, token):
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
    test_et_cherche(ID)
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
    test_et_cherche(ID)
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

# Fonction principale pour gérer le programme
def program():
    teste("program")
    test_et_entre(ID, 'program')
    teste(";")
    block()
    if token != ".":
        erreur(".", token)

# Appel de la fonction principale pour exécuter le programme
program()
