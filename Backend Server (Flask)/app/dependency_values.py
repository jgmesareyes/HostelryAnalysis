'''
Created on 8 de may. de 2016

@author: Jose
'''

import re



def searchOnlyNounsAdjectives():
    """Procesa los sustantivos y adjetivos del archivo de dependencias
    
    """
    f3 = open('out-dep.txt', 'r', encoding='UTF-8')
    deep = 0
    nounFlag = -1
    noun = ""
    nounAdjList = []
    nounPrepList = []
#    prepList = []
    for line in f3:
        line = line.strip()
        if re.search("NC", line) and str(line).endswith("["):
            noun = line[line.find('(') + 1:line.find(')')].split()[0]
            nounFlag = deep
        if nounFlag != -1:
            if (nounFlag + 1) == deep:
                if re.search("AQ", line):
                    nounAdjList.append([noun, line[line.find('(') + 1:line.find(')')].split()[0]])
        if str(line).endswith("["):
            deep += 1
        elif str(line).endswith("]"):
            deep -= 1
            if nounFlag == deep:
                nounFlag = -1
                noun = ""
    
    for item in nounAdjList:
        print (item)

    for item in nounPrepList:
        print (item)
    
    


def searchGroupsGenreLemmasData(globalData, regionData, descriptionDocName):
    """Procesa las características de la descripción de un hotel en Español.
    
    Se extrae la información a partir del archivo de descripción del hotel con
    dependencias funcionales generado por la librería Freeling, y se analiza
    para la búsqueda de patrones sustantivo-complementos.
    Se ha mejorado el algoritmo resultante del procesado de Freeling dando
    solución a los problemas mencionados en la memoria del proyecto.
    
    Parámetros:
    globalData -- registro global de características de todos los hoteles
    descriptionDocName -- nombre del archivo de dependencias con la descripción
    
    Resultado:
    finalValues -- lista de pares {sustantivo: complementos} extraídos.
    
    """
    f = open(descriptionDocName, 'r', encoding='UTF-8')
    deep = 0
    noun = ""
    nounCode = ""
    nounFlag = -1
    newNoun = True
    adj = ""
    adjCode = ""
    adjFlag = -1
    verb = ""
    verbFlag = -1
    prep = ""
    prepFlag = -1
    prepValues = []
    adjValues = []
    adjValuesDic = {}
    nounValues = {}
    finalValues = {}
    for line in f:
        line = line.strip()
        if not str(line).endswith(']'):
            if re.search("grup-verb", line) and verbFlag == -1:
                verbFlag = deep
            elif re.search("VM", line) and verbFlag != -1 and verb == "":
                verbData = line[line.rfind('(') + 1:line.rfind(')')].split()
                verb = verbData[1]
                if verb not in globalData['verb'].keys():
                    globalData['verb'][verb] = 1
                else:
                    globalData['verb'][verb] = globalData['verb'].get(verb) + 1
            elif re.search("grup-nom", line) and nounFlag == -1 and verb != "":
                nounFlag = deep
            elif (re.search("NC", line) or re.search("TV", line)) and nounFlag != -1 and prepFlag == -1 and newNoun == True:
                if noun != "":
                    if adjValuesDic:
                        adjValues = [adj for adj, code in adjValuesDic.items() if (noun == "TV" or (code[4] == nounCode[3] and (code[3] == nounCode[2] or code[3] == 'C')))]
                    nounValues[noun] = [item.strip() for item in adjValues + prepValues if (item != "")]
                    adjValuesDic.clear()
                    adjValues.clear()
                    prepValues.clear()
                nounData = line[line.rfind('(') + 1:line.rfind(')')].split()
                noun = nounData[1]
                nounFlag = deep
                newNoun = False
                nounCode = nounData[2]
            elif re.search("s-a", line) and adjFlag == -1:
                adjFlag = deep
            elif re.search("AQ", line) and adjFlag != -1 and adj == "" and prepFlag == -1:
                adjData = line[line.rfind('(') + 1:line.rfind(')')].split()
                adj = adjData[1]
                adjCode = adjData[2]
            elif (re.search("grup-sp", line) or re.search("sp-", line)) and prepFlag == -1 and nounFlag != -1 and noun != "":
                prepFlag = deep
            elif (re.search("Fc", line) or re.search("CC", line)) and nounFlag != -1:
                newNoun = True
            if str(line).endswith(')') and prepFlag != -1:
                prepData = line[line.rfind('(') + 1:line.rfind(')')].split()
                prep += prepData[0] + " "
        if str(line).endswith('['):
            deep += 1
        elif str(line).endswith(']'):
            deep -= 1
            if verbFlag == deep:
                if adjValuesDic and noun != "":
                    adjValues = [adj for adj, code in adjValuesDic.items() if (noun == "TV" or (code[4] == nounCode[3] and (code[3] == nounCode[2] or code[3] == 'C')))]
                complements = [item.strip() for item in adjValues + prepValues if (item != "")]
                if noun != "":
                    if noun not in finalValues.keys():
                        finalValues[noun] = complements.copy()
                    else:
                        currentFinalValues = finalValues.get(noun)
                        currentFinalValues += [item for item in complements if (item not in currentFinalValues)]
                        finalValues[noun] = currentFinalValues
                    if noun not in globalData['noun'].keys():
                        globalData['noun'][noun] = 1
                    else:
                        globalData['noun'][noun] = globalData['noun'].get(noun) + 1
                    if noun not in regionData['noun'].keys():
                        regionData['noun'][noun] = 1
                    else:
                        regionData['noun'][noun] = regionData['noun'].get(noun) + 1
                    for item in complements:
                        if item not in globalData['complement'].keys():
                            globalData['complement'][item] = 1
                        else:
                            globalData['complement'][item] = globalData['complement'].get(item) + 1
                        if item not in regionData['complement'].keys():
                            regionData['complement'][item] = 1
                        else:
                            regionData['complement'][item] = regionData['complement'].get(item) + 1
                        bothValues = noun + " " + item
                        if bothValues not in globalData['global'].keys():
                            globalData['global'][bothValues] = 1
                        else:
                            globalData['global'][bothValues] = globalData['global'].get(bothValues) + 1
                        if bothValues not in regionData['global'].keys():
                            regionData['global'][bothValues] = 1
                        else:
                            regionData['global'][bothValues] = regionData['global'].get(bothValues) + 1
                for nounValue, complementValue in nounValues.items():
                    complementValue = [item for item in complementValue if (item != "")]
                    if nounValue not in finalValues.keys():
                        finalValues[nounValue] = complementValue.copy()
                    else:
                        currentFinalValues = finalValues.get(nounValue)
                        currentFinalValues += [item for item in complementValue if (item not in currentFinalValues)]
                        finalValues[nounValue] = currentFinalValues
                    if nounValue not in globalData['noun'].keys():
                        globalData['noun'][nounValue] = 1
                    else:
                        globalData['noun'][nounValue] = globalData['noun'].get(nounValue) + 1
                    if nounValue not in regionData['noun'].keys():
                        regionData['noun'][nounValue] = 1
                    else:
                        regionData['noun'][nounValue] = regionData['noun'].get(nounValue) + 1
                    for item in complementValue:
                        if item not in globalData['complement'].keys():
                            globalData['complement'][item] = 1
                        else:
                            globalData['complement'][item] = globalData['complement'].get(item) + 1
                        if item not in regionData['complement'].keys():
                            regionData['complement'][item] = 1
                        else:
                            regionData['complement'][item] = regionData['complement'].get(item) + 1
                        bothValues = nounValue + " " + item
                        if bothValues not in globalData['global'].keys():
                            globalData['global'][bothValues] = 1
                        else:
                            globalData['global'][bothValues] = globalData['global'].get(bothValues) + 1
                        if bothValues not in regionData['global'].keys():
                            regionData['global'][bothValues] = 1
                        else:
                            regionData['global'][bothValues] = regionData['global'].get(bothValues) + 1
                verb = ""
                verbFlag = -1
                noun = ""
                nounValues.clear()
                nounCode = ""
                nounFlag = -1
                newNoun = True
                adj = ""
                adjValues.clear()
                adjValuesDic.clear()
                adjCode = ""
                adjFlag = -1
                prep = ""
                prepValues.clear()
                prepFlag = -1
                complements.clear()
            if adjFlag == deep:
                #adjValues.append(adj.strip())
                if adj != "":
                    adjValuesDic[adj] = adjCode
                adj = ""
                adjCode = ""
                adjFlag = -1
            if prepFlag == deep:
                prepValues.append(prep.strip())
                prep = ""
                prepFlag = -1

    return finalValues.copy()



def searchGroupsGenreLemmasDataEnglish(globalData, regionData, descriptionDocName):
    """Procesa las características de la descripción de un hotel en Inglés.
    
    Parámetros:
    globalData -- registro global de características de todos los hoteles
    descriptionDocName -- nombre del archivo de dependencias con la descripción
    
    Resultado:
    finalValues -- lista de pares {sustantivo: complementos} extraídos.
    
    """
    f = open(descriptionDocName, 'r', encoding='UTF-8')
    deep = 0
    noun = ""
    nounCode = ""
    nounFlag = -1
    adj = ""
    adjCode = ""
    adjValuesDic = {}
    adjFlag = -1
    nounChunkFlag = -1
    nounValues = {}
    nounList = []
    finalValues = {}
    for line in f:
        line = line.strip()
        if not str(line).endswith(']'):
            if re.search("sn-chunk", line) and nounChunkFlag == -1:
                nounChunkFlag = deep
            elif re.search("sn-chunk", line) and nounChunkFlag != -1 and nounFlag == -1 and adjFlag == -1:
                nounChunkFlag = deep
            elif (re.search("NN", line) or re.search("TV", line) or re.search("wi-fi", line)) and nounChunkFlag != -1:
                if nounFlag == -2:
                    nouns = ""
                    for noun in nounValues.keys():
                        nouns += noun + " "
                    if nouns not in finalValues.keys():
                        finalValues[nouns] = [comp for comp in adjValuesDic.keys()]
                    else:
                        currentValues = finalValues.get(nouns)
                        for comp in adjValuesDic.keys():
                            if comp not in currentValues:
                                currentValues.append(comp)
                    adjValuesDic.clear()
                    if nouns not in globalData['noun'].keys():
                        globalData['noun'][nouns] = 1
                    else:
                        globalData['noun'][nouns] = globalData['noun'].get(nouns) + 1
                    if nouns not in regionData['noun'].keys():
                        regionData['noun'][nouns] = 1
                    else:
                        regionData['noun'][nouns] = regionData['noun'].get(nouns) + 1
                    nounValues.clear()
                nounData = line[line.rfind('(') + 1:line.rfind(')')].split()
                noun = nounData[1]
                nounCode = nounData[2]
                nounFlag = deep
                nounValues[noun] = nounCode
            elif re.search("JJ", line):
                adjData = line[line.rfind('(') + 1:line.rfind(')')].split()
                adj = adjData[1]
                adjCode = adjData[2]
                adjFlag = deep
                adjValuesDic[adj] = adjCode
            elif re.search("VB", line) and nounValues:
                nounValues.clear()
            elif re.search("Fc", line) and nounFlag != -1:
                nounFlag = -2
        if str(line).endswith('['):
            deep += 1
        elif str(line).endswith(']'):
            deep -= 1
            if nounChunkFlag == deep:
                nouns = ""
                for key in nounValues.keys():
                    nouns += key + " "
                nouns = nouns.strip()
                if nouns not in finalValues.keys():
                    finalValues[nouns] = [comp for comp in adjValuesDic.keys()]
                else:
                    currentValues = finalValues.get(nouns)
                    for comp in adjValuesDic.keys():
                        if comp not in currentValues:
                            currentValues.append(comp)
                    finalValues[noun] = currentValues
                if nouns not in globalData['noun'].keys():
                    globalData['noun'][nouns] = 1
                else:
                    globalData['noun'][nouns] = globalData['noun'].get(nouns) + 1
                if nouns not in regionData['noun'].keys():
                    regionData['noun'][nouns] = 1
                else:
                    regionData['noun'][nouns] = regionData['noun'].get(nouns) + 1
                for noun in nounList:
                    if noun not in finalValues.keys():
                        finalValues[noun] = [comp for comp in adjValuesDic.keys()]
                    else:
                        currentValues = finalValues.get(noun)
                        for comp in adjValuesDic.keys():
                            if comp not in currentValues:
                                currentValues.append(comp)
                        finalValues[noun] = currentValues
                    if noun not in globalData['noun'].keys():
                        globalData['noun'][noun] = 1
                    else:
                        globalData['noun'][noun] = globalData['noun'].get(noun) + 1
                    if noun not in regionData['noun'].keys():
                        regionData['noun'][noun] = 1
                    else:
                        regionData['noun'][noun] = regionData['noun'].get(noun) + 1
                
                adjValuesDic.clear()
                nounValues.clear()
                nounChunkFlag = -1
                adjFlag = -1
                nounFlag = -1
    
    for key, values in finalValues.items():
        if key not in globalData['noun'].keys():
            globalData['noun'][key] = 1
        else:
            globalData['noun'][key] = globalData['noun'].get(key) + 1
        if key not in regionData['noun'].keys():
            regionData['noun'][key] = 1
        else:
            regionData['noun'][key] = regionData['noun'].get(key) + 1
        for value in values:
            if value not in globalData['complement'].keys():
                globalData['complement'][value] = 1
            else:
                globalData['complement'][value] = globalData['complement'].get(value) + 1
            if value not in regionData['complement'].keys():
                regionData['complement'][value] = 1
            else:
                regionData['complement'][value] = regionData['complement'].get(value) + 1
            bundle = key + " " + value
            if bundle not in globalData['global'].keys():
                globalData['global'][bundle] = 1
            else:
                globalData['global'][bundle] = globalData['global'].get(bundle) + 1
            if bundle not in regionData['global'].keys():
                regionData['global'][bundle] = 1
            else:
                regionData['global'][bundle] = regionData['global'].get(bundle) + 1  

    return finalValues.copy()
