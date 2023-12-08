import re
from itertools import chain

def is_ID(id:str):
    return True if re.match("[a-zA-Z_][a-zA-Z_0-9]*", id) else False

def analyseur_lexical(fichier:str):
    # Lecture du fichier avec séparation des ; et \n
    global listConst,listVar,code
    code = ""
    with open(fichier,'r') as f:
        for ligne in f:
            for lettre in ligne:
                if lettre== ";":
                    code += " ; "
                elif lettre == ",":
                    code += " , "
                elif lettre=="\n":
                    code+= " "
                else:
                    code += lettre
                    
    # Suppression des commentaires
    code = re.sub("\(\*(.*?)\*\)", "", code)
    
    # Séparation des mots et réassemblement des différentes instructions
    code=code.split(" ")

    code=[value for value in code if value != '']
    
    instructions = []
    instruction_courante = []
    for mot in code:
        if mot == ";":
            instruction_courante.append(mot)
            instructions.append(instruction_courante)
            instruction_courante = []
        elif mot == "begin" or mot == "end" or mot == "repeat":
            if instruction_courante != []:
                instructions.append(instruction_courante)
            instructions.append([mot])
            instruction_courante = []
        else:
            instruction_courante.append(mot)
    instructions.append(instruction_courante)
    code=[instruction for instruction in instructions if instruction != []]
  
    #print(instructions)
########################################################""
    # Analyse du lexique

    # Program
    instruction = instructions[0]
    assert instruction[0] == "program", "SyntaxError: Missing program declaration in header"
    assert re.match("[a-zA-Z_][a-zA-Z_0-9]*", instruction[1], re.IGNORECASE), "SyntaxError: Missing program name in header"    
    assert instruction[2] == ";", "SyntaxError: Missing semicolon in header declaration"

    #Bloc

    fin_des_consts = False
    fin_des_vars = False
    listConst=[]
    listValConst=[]
    for instruction in instructions:
      if instruction[0] == "const":
        assert not fin_des_consts, "SyntaxError: Can't declare const after var"
        nom_const = instruction[1]
        #erreur
        # assert re.match("[a-zA-Z_][a-zA-Z_0-9]*", nom_const), f"SyntaxError: \"{nom_const}\" is not a legal const name"
        # assert instruction[2] == "=", f"SyntaxError: Expected '=' in const declaration"
        valeur_const = instruction[3]
        # assert re.match("[+-]?[0-9]+", valeur_const), f"ValueError: \"{valeur_const}\" Expected integer in const affectation"
        # assert instruction[4] == ";", f"SyntaxError: Expected semicolon"
        
        # Ajout de la constante à la liste listConst
        listConst.append(nom_const)
        listValConst.append(valeur_const)
        # Déclaration VARS
      elif instruction[0] == "var":
            #assert not fin_des_vars, "SyntaxError: Cant declare var after an INSTS"
            fin_des_consts = True
           # assert instruction[1] != ";", "SyntaxError: excepted variable name"
            i = 1
            listVar=[]
            nom_variable_attendu = True # A la prochaine instruction
            while instruction[i] != ";":
                if nom_variable_attendu:
                    assert re.match("[a-zA-Z_][a-zA-Z_0-9]*", instruction[i]), f"SyntaxError: \"{instruction[i]}\" is not a legal variable name"
                    listVar.append(instruction[i])  # Ajoute le nom de la variable à la liste
                    nom_variable_attendu = False
                else: # , attendu
                   # assert instruction[i] == ",", f"SyntaxError: \"{instruction[i]}\" expected comma between 2 variable"
                    nom_variable_attendu = True
                i+=1
           # assert nom_variable_attendu == False, f"SyntaxError: \"{instruction[i-1]}\" expected variable after a comma"
            # print(listVar)
            # print(listConst)
            # print(listValConst)
        # INSTS
      assert ['begin'] in instructions, "SyntaxError: BEGIN expected"
      # Affec        
      if instruction == ['begin']:
            fin_des_vars = True

    # Verification que le BLOC finisse bien par end
    a = instructions.index(['begin'])
    c = len(instructions)
    for i in range(a+1, c):
     for element in instructions[i]:
        if len(element) == 1 and element.isalpha():
          assert element in listVar or element in listConst, f"SyntaxError: '{element}' variable not declared"


    assert code[-2] == ['end'], "SyntaxError: expected \"end\" at the end of BLOCK "
        # . Verification que le programme finisse par un point
    assert code[-1] == ["."], "SyntaxError: expected \'.\' at the end of the program"
    #print(instructions)


analyseur_lexical("MonCode.code")

code=list(chain.from_iterable(code))
def listvarConst():
  return listVar,listConst

valeur=[]
def listValeur():
 for token in range(len(code)):
  if (code[token]==":=" or code[token]=="=" )and code[token+1].isdigit() :
     valeur.append( code[token-1])
     valeur.append( code[token+1])
opera=[]
def operations():
   for token in range(len(code)):
     if (code[token] in listVar or code[token] in listConst) and (code[token+1]==":=") and (code[token+2] in listVar or code[token+2] in listConst) :
            valfinal=code[token]
            op=code[token+3]
            i=token
            while code[i]!=";":
                  opera.append(code[i])
                  i=1+i  
   return valfinal,op,opera

listValeur()
valeur_Var_Res,ope,opera=operations()
opera.remove(":=")

def opee():
  return ope
def val_ValRes():
    for token in range(len(valeur)):
        if valeur[token]==valeur_Var_Res:
          return int(valeur[token+1]) 
        
from etape1 import test
def aidee():
  return test()