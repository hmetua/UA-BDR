#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:59:08 2021

@author: math
"""
#IMPORTER FICHIER XML

import xml.etree.ElementTree as ET
content = ET.parse("employes_enron.xml")
root = content.getroot()

#FICHIER CSV

import csv

doc = open("email.csv","w",newline='',encoding='utf-8')
write = csv.writer(doc)

#CREATION

#entete = ['Nom','Prenom','Status','MailBox','Emails']
entete = ['Nom','Prenom','Status','Emails']
write.writerow(entete)

for i in root.findall("./employee"):
    T=[]
    #Nom
    nom = i.find('lastname')
    nom = nom.text
    T.append(nom)
    #Prenom
    prenom = i.find('firstname')
    prenom = prenom.text
    T.append(prenom)    
    #Status
    status = i.get('category')
    T.append(status)

    M=[]
    mail=''
    for n in i.iter('email'):
        #Emails
        mail = mail + n.get('address') + ','
    T.append(mail[:-1])
    write.writerow(T)
doc.close()

import pandas as pd

dataframe = pd.read_csv("email.csv")

print(dataframe)

