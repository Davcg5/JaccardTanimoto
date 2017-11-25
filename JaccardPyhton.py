import threading
import time 
"""Este programa calcula coeficiente jaccard/tanimoto """
def calculojt(formula1, formula2):
    """Esta funcion envia las formulas a comparador y obtiene el coeficiente"""
    #print formulaA, formulaB
    diccionario1 = {}
    diccionario2 = {}
    diccionario3 = {}
    na = 0
    nb = 0
    nc = 0
    coefjt = 0

#    t1 = threading.Thread(target=comparador, args=(formula1, diccionario1,))
#    t2 = threading.Thread(target=comparador, args=(formula2, diccionario2,))
#    t1.start()
#    t2.start()
#    t1.join()
#    t2.join()
    
    diccionario1 = comparador(formula1)    
    diccionario2 = comparador(formula2)
    
    for i in range (0, len(diccionario1)):
        if diccionario2.has_key(diccionario1.keys()[i])==1:
            a = diccionario1.get(diccionario1.keys()[i])
            b = diccionario2.get(diccionario1.keys()[i])
            c = min(a, b)
            
            diccionario3.update({diccionario1.keys()[i]:c})
#	    print diccionario3

    for i in range(0, len(diccionario1.values())):
        na += diccionario1.values()[i]
       # print diccionario1.values()[i]
    for i in range(0, len(diccionario2.values())):
        nb += diccionario2.values()[i]
    for i in range(0, len(diccionario3.values())):
        nc += diccionario3.values()[i]
    
    coefjt = nc/(float(na+nb-nc))
    
    return coefjt


def coeficiente(formula1, formula2):
    """ Esta funci[on permite imprimir los resultados, en la lista elm se adjuntaran las 2 formulas y el coeficiente mediant una llaada  """
    listaelm = []
 
    listaelm.append([formula1, formula2,round(calculojt(formula1, formula2),2)])
    
    
   # print listaelm
   	
   
    return listaelm

def comparador (formula):
    """En esta clase se recorre la formula y se acumulan en el diccionario  """
    diccionario = {} 
    for i in range(0, len(formula)):
        if formula[i] == '@':
            diccionario.update({formula[i]:1})
        elif diccionario.get(formula[i])>=1:
            diccionario.update({formula[i]:1+diccionario[formula[i]]})
        else: 
            diccionario.update({formula[i]:1}) 
    return diccionario 

ARCHIVO = open("ZINC_chemicals.tsv", "r")
FORMULA = []
START = time.time()
for linea in ARCHIVO.readlines():
    lineas = ARCHIVO.readlines()
    FORMULA.append((linea.split('\t'))[0].strip('\n'))
ARCHIVO.close() 


 
def main(x, y):
    """Esta funcion crea la matriz que se va a recorrer e invoca a la funcion coeficiente en donde se ingresa la formula en x con la formula en y  """
    for i in range(1, y):
        for j in range(i+1,y):
            #print i, j
 #	print formula[i],formula[j]
            print (FORMULA[i])
            coef=(coeficiente(FORMULA[i], FORMULA[j]))
            f=open("Resultados.tsv", "a")
             
            c = str(coef)
            f.write(c +"\n")
            end=time.time()
            print end-START
     
#main(0, 12423)			
T3 = threading.Thread(target=main, args=(0, 6072,))
T4 = threading.Thread(target=main, args=(6073, 8587,))
T5 = threading.Thread(target=main, args=(8588, 10517,))
T6 = threading.Thread(target=main, args=(10518, 12423,))
T3.start()
T4.start()
T5.start()
T6.start()
T3.join()
T4.join()
T5.join()
T6.join()


