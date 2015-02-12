'''
Created on Dec 9, 2013

@author: Makobyte
Makoto Yuan
'''
'''

CS 565 PA2
Author Name Disabiguation 
'''


import csv
import unicodedata as uni
import re
from collections import OrderedDict
import itertools as iter

#Creates dictionary paperAuthorList[authorID] = [list of names], 
def paperAuthorGather():
    paperAuthorList = {}
    firstLine = True
    
    #Opens PaperAuthor.csv and grabs author name and ID
    with open('PaperAuthor.csv') as csvfile: 
        paperAuthor = csv.reader(csvfile, delimiter=',')
        
        for row in paperAuthor:
            
            if firstLine:
                firstLine = False
            authorId = row[1].strip()
            authorName = row[2].lower()
            
            if paperAuthorList.get(authorId) != None:
                paperAuthorList[authorId].append(authorName)
            else:
                paperAuthorList[authorId] = [authorName]
            
    return paperAuthorList
            
#Returns a dictionary of usersID| authorlist[authorID] = name
def authorGather(paperList):
    authorList = {}
    idList = {}
    firstLine= True
    
    #Opens Author.csv file| Grabs author name and ID
    with open('Author.csv') as csvfile:
        author = csv.reader(csvfile, delimiter=',')
        #for every row in train.csv read in author name and ID
        for row in author:
            
            if firstLine:
                firstLine = False
            
            else:       
                authorId= row[0].strip()
                #Cleans up random characters
                #name = uni.normalize('NFKD',unicode(row[1])).encode('ascii','ignore') 
                name = re.sub('[.\'-*~,]','', row[1].upper())
                authorName= name.lower()
                idList[authorId] = authorName
                #authorList[authorName] = authorId

                #Checks if exact string match in authorList pre-exists in authorList
                

                if paperList.get(authorId) != None:
                    if authorName == "":
                        pass
                    else:
                        if authorList.get(authorName) != None:
                            authorList[authorName].append(authorId)
                        else:
                            authorList[authorName] = [authorId]

    return authorList, idList

def genNames(author):
    theNameList = []
    theNameList.append(author)
    names = author.split(" ")
    lastName = names[-1]
    squishedName = ""
    initials = []
    init = []

    #Grabs all initials of names
    for name in names:
        if name == "":
            name = " "
        initials.append(name[0])
        squishedName += name
    for x in range(len(names)):
        init.append(False)
    
    #skip empty names
    if len(names) == 1:
        pass
    else:
        for starting in range(len(names)-1):
            for middle in (starting, len(names)-2):
                init[middle] = True
                
                curName = ""
                for letter in range(len(names)):
                    if init[letter]:
                        curName += initials[letter] + " "
                    else:
                        curName += names[letter] + " "
                if curName.strip() not in theNameList:
                    theNameList.append(curName.strip())
            
            for x in range(len(names)):
                init[x] = False   


    '''
    for daName in theNameList:
        curName = daName.split(" ")
        axe = list(iter.permutations(curName))
        for wordCombo in axe:
            addName = ""
            for namez in wordCombo:
                addName += namez + " "
            addName = addName.strip()
            if addName not in allPermList:
                allPermList.append(addName)
    '''
    #Creates all orderings of subnames
    allPermList = []
    axe = list(iter.permutations(names))
    for tree in axe:
        reconName = ""
        for wood in tree:
            reconName += wood + " "
        if reconName not in allPermList:
            allPermList.append(reconName.strip())
    
        
    #Generates all permutations of names with subnames removed
    remList = []
    for elemental in theNameList:
        
        curGen = elemental.split(" ")
        for letterOmit in range(len(curGen)-1):
            genName = ""
            for curLetter in range(len(curGen)):
                if curLetter == letterOmit:
                    pass
                else:
                    genName += curGen[curLetter] + " "
            if genName.strip() not in remList:
                remList.append(genName.strip())
    
    #Generates all combination of elements for a given name
    #i.e Thommas John Hob -> ThommasJohn Hob, Thommas JohnHob, TJohn Hob...
    permList = []
    for elem in theNameList:
        newName = ""    
        curElem = elem.split(" ")
        for spark in range(len(curElem)-1):
            newName = ""
            for let in range(len(curElem)-1):
                if let == spark:
                    newName += curElem[let] + curElem[let+1] + " "
                elif let == len(curElem)-1:
                    newName += curElem[let]
                elif let == spark+1:
                    pass
                else:
                    newName += curElem[let] + " "
            permList.append(newName.strip())
        for permute in permList:
            if permute not in theNameList:
                theNameList.append(permute)
    #appends generated names to namelist
    for generatedName in remList:
        if generatedName not in theNameList:
            theNameList.append(generatedName)
    
    for generatedName in allPermList:
        if generatedName not in theNameList:
            theNameList.append(generatedName)
            
    theNameList.append(squishedName)
    
    return theNameList

def compileList(authoList, idList, papeList):
    dupeList = {}
    curNameList = []
    total = len(idList.keys())
    counter = 0.0
    for allId, theName in idList.iteritems():
        dupeList[allId] = [allId]
    for eyed, name in idList.iteritems():
        counter += 1.0
        if papeList.get(eyed) != None:
            if authoList.get(name) != None:
                allIds = authoList[name]
                #print allIds
                #grabs list of ids from author list
                #dupeList[ids] = authoList[name]
                
                curNameList = genNames(name.strip())
                for test in curNameList:
                    if authoList.get(test) != None:
                        for theId in authoList[test]:
                            if theId not in dupeList[eyed]:
                                dupeList[eyed].append(authoList[test][0])
                            if eyed not in authoList[test]:    
                                dupeList[authoList[test][0]].append(eyed)
                        
                    dupeList[eyed] = allIds
            else:
                dupeList[eyed] = [eyed]
        else:
            dupeList[eyed] = [eyed]
        print counter/total
    return dupeList

#Old compile
def simpleCompile(authorList, idList, papeList):
    dupeList = {}
    for curId, curName in idList.iteritems():
        if papeList.get(curId) != None:
            if authorList.get(curName) != None:
                dupeList[curId] = authorList[curName]
            else:
                dupeList[curId] = [curId]
        else:
            dupeList[curId] = [curId]
    return dupeList

def printcsv(inputFile):
    answers = open( "answers.csv", "wb")
    writer = csv.writer(answers)
    writer.writerow(["AuthorId", "DuplicateAuthorIds"])
    
    for key, value in inputFile.iteritems():
        idlist = ""
        for ids in value:
            idlist = idlist + ids + " "
        writer.writerow([key, idlist.strip()])


paperAuthor = paperAuthorGather()
print "Paper Author Done"


author, ids = authorGather(paperAuthor)

#initial = initialsList(ids)

listz = ["this", "is", "a", "test"]



print "Author Gather Done" 
answer = compileList(author, ids, paperAuthor)
#answer = simpleCompile(author, ids, paperAuthor)
print "List Compiled"
printcsv(answer)


