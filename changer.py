#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 01:11:30 2021

@author: math
"""

import csv
import re

with open("email.7.csv",) as f:
    file=csv.reader(f, delimiter=",")
    Nom_Prenom=[]
    Status=[]
    Id_mail=[]
    
    Mail_Indice_dico={}
    Mail=[]
    Indice=[]
    
    Nom=[]
    i=1
    for row in file:
        Nom.append(row[0])
        Nom_Prenom.append(row[0]+' '+row[1])
        Status.append(row[2])
        Id_mail.append(i)
        T=row[3].split(',')
        for k in range(len(T)):
            Mail_Indice_dico[T[k]]=i
            
            Indice.append(i)
            Mail.append(T[k])
        i+=1
   
f.close()

with open("tableau.csv") as f:
    file=csv.reader(f, delimiter=",")
    Id_message=[]
    Auteur=[]
    Destinataire=[]
    Reponse=[]
    Date=[]
    k=0
    for row in file:
        print(k)
        if k>0:
            if row[1] not in Mail:
                aut=0
                if '@' in row[1]:
                    if row[1].split('@')[1]!='enron.com':
                        aut=0
                        # Contact extérieur
                    elif row[1].split('@')[1]=='enron.com':
                        Nom_Prenom.append(row[1].split('@')[0])
                        Status.append('')
                        
                        Mail_Indice_dico[row[1]]=i
                        
                        aut=i
                        Id_mail.append(i)
                        
                        Indice.append(i)
                        Mail.append(row[1])
                        
                        i+=1

            else:
                aut=Mail_Indice_dico.get(row[1])

            if row[2] not in Mail:
                des=0
                if '@' in row[2]:
                    if row[2].split('@')[1]!='enron.com':
                        des=0
                    #Destinataire.append(0) Contact extérieur
                
                    elif row[2].split('@')[1]=='enron.com':
                        Nom_Prenom.append(row[2].split('@')[0])
                        Nom.append(row[2].split('@')[0])
                        Status.append('')
                        
                        Mail_Indice_dico[row[2]]=i
                        des=i
                        Id_mail.append(i)
                        
                        Indice.append(i)
                        Mail.append(row[2])
                
                        i+=1

            else:
                des=Mail_Indice_dico.get(row[2])
                    
            if des!=0 or aut!=0:
                Id_message.append(row[0])
                Reponse.append(row[3])
                Date.append(row[4])
                Auteur.append(aut)
                Destinataire.append(des)
        k+=1
    
    Mail_indice={}  
    Mail_indice['Mail']=Mail[1:] #Mail de l'employee
    Mail_indice['Id_mail']=Indice[1:] #Identité numerique de l'employee
    
    Employee={}
    Employee['Id_Employee']=Nom_Prenom[1:] #Nom+Prenom
    Employee['Status']=Status[1:] #Status
    Employee['Id_mail']=Id_mail[1:] #Identité numerique de l'employee   
    
    Tableau={}
    Tableau['Id_message']=Id_message[1:]
    Tableau['Auteur']=Auteur[1:]
    Tableau['Destinataire']=Destinataire[1:]
    Tableau['Reponse']=Reponse[1:]
    Tableau['Date']=Date[1:]
    
    import pandas as pd
    df1=pd.DataFrame(Mail_indice)
    df2=pd.DataFrame(Employee)
    df3=pd.DataFrame(Tableau)

f.close()
print(df1)
print(df2)   
print(df3)

df1.to_csv(r'/home/math/Documents/prototype/list_employee_mail.csv',index=False,header=True)
df2.to_csv(r'/home/math/Documents/prototype/list_employee.csv',index=False,header=True)
df3.to_csv(r'/home/math/Documents/prototype/mailbox_enron.csv',index=False,header=True)
