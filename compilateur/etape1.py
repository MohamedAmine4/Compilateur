# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:43:59 2023

@author: Mohamed amine boussoualef
"""
from aide import val_ValRes
from aide import opee
# Liste des mnémoniques pour les instructions
MNEMONIQUES = ["ADD", "SUB", "MUL", "DIV", "EQL", "NEQ", "GTR", "LSS", "GEQ",
               "LEQ", "PRN", "INN", "INT", "LDI", "LDA", "LDV", "STO", "BRN",
               "BZE", "HLT"]
def test():
  PCODE=[("INT",2),("LDA",0),("INN",False),("LDA",1),("LDA",0),("LDV",False),
       ("LDA",1),("LDV",False),("ADD",False),("STO",False),("LDA",0),
       ("LDV",False),("LDI",0),("EQL",False),("BZE",1),("LDA",1),("LDV",False),
       ("PRN",False),("HLT",False)]
  return PCODE

def interpreteur(PCODE):
    MEM = []  # La mémoire
    SP = 0    # Pointeur de pile
    PC = 0    # Pointeur d'instructions
    PS = "EXECUTION"  # Statut du programme

    INST = ""  # Instruction en cours

    while PS != "END":
        INST = PCODE[PC][0]     
        OPERANDE = PCODE[PC][1]
        
        # Déplacement du pointeur d'instructions au prochain si ce n'est pas la fin du programme
        if PC < (len(PCODE) - 1):
            PC += 1

        # Exécution des instructions
        if INST == "ADD":
            MEM[-2] = MEM[-1] + MEM[-2]
            del MEM[-1]
        elif INST == "SUB":
            MEM[-2] = MEM[-2] - MEM[-1]
            del MEM[-1]
        elif INST == "MUL":
            MEM[-2] = MEM[-1] * MEM[-2]
            del MEM[-1]
        elif INST == "DIV":
            MEM[-2] = MEM[-2] / MEM[-1]  
            del MEM[-1]
        elif INST == "EQL":
            MEM[-2] = int(MEM[-1] == MEM[-2])
            del MEM[-1]
        elif INST == "NEQ":
            MEM[-2] = int(MEM[-1] != MEM[-2])
            del MEM[-1]
        elif INST == "GTR":
            MEM[-2] = int(MEM[-2] > MEM[-1])
            del MEM[-1]
        elif INST == "LSS":
            MEM[-2] = int(MEM[-2] < MEM[-1])
            del MEM[-1]
        elif INST == "GEQ":
            MEM[-2] = int(MEM[-2] >= MEM[-1])
            del MEM[-1]
        elif INST == "LEQ":
            MEM[-2] = int(MEM[-2] <= MEM[-1])
            del MEM[-1]
        elif INST == "PRN":
          if opee()=="-":
            MEM[-1]=-MEM[-1]
          result = eval(f"MEM[-1] {opee()} val_ValRes()")
          print(f"B= {result}")

          del MEM[-1]
        elif INST == "INN":
            a = int(input(""))  # Entrer une valeur
            adresse = MEM[-1]
            MEM[adresse] = a
            del MEM[-1]
        elif INST == "INT": 
            MEM += [0] * OPERANDE
            SP += OPERANDE
        elif INST == "LDI":
            MEM += [OPERANDE]
        elif INST == "LDA":
            MEM += [OPERANDE]
        elif INST == "LDV":
            MEM[-1] = MEM[MEM[-1]]
        elif INST == "STO":
            MEM[MEM[-2]] = MEM[-1]
            del MEM[-1]
            del MEM[-1]
        elif INST == "BRN":
            PC = OPERANDE
        elif INST == "BZE":
            if MEM[-1] == 0:
                PC = OPERANDE
            del MEM[-1]
        elif INST == "HLT":
            PS = "END"

  

#interpreteur(test)