#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 23:26:56 2021

@author: math
"""
import re
import os
from email.parser import Parser
import pandas as pd
import email.utils

def dossier():
    files = []
    for r,d,f in os.walk('maildir'):
        for file in f:
            if '.' in file:
                files.append(os.path.join(r,file))
    return files

def func1(fichier):
    with open(fichier,encoding="iso-8859-1") as f:
        return f.read()
    
if __name__=='__main__':
    Files=dossier()
    dico={}
    ID=[]
    Date=[]
    From=[]
    To=[]
    Sub=[]
    i=0
    for File in Files:
        df=func1(File)
        email=Parser().parsestr(df)
        
        destinataire=[]
        for key in ['To','Cc','Cci','Bcc']:
            val=email[key]
            if val is not None:
                val=val.replace("\n","")
                val=val.replace("\t","")
                val=re.sub(r'\s+','',val)
                val=val.split(',')
                destinataire=destinataire+val
        
        uniq=set(destinataire)
        tab=list(uniq)
        
        for empl in tab:

            message_id=email['Message-ID']
            if message_id is not None:
                ID.append(i)
            else:
                ID.append(message_id)
            
            now_date=email['Date']
            tab1=now_date.split(' ')
            Date.append(' '.join(tab1[1:5]))
            auteur=email['From']
            From.append(auteur.replace(" ",""))
            destinataire=empl
            To.append(destinataire.replace(" ",""))
        
            txt=email['Subject']
            if txt is not None:
                sub=re.sub(r"\s+","",txt)
                sub=sub[:2]            
                if sub in ["Re","RE"]:
                    Sub.append(1) #Réponse à un mail 1
                else:
                    Sub.append(0) #Pas une réponse à un mail 0
            else:
                Sub.append(sub)
        print(i)
        i+=1
    dico['ID_mail']=ID
    dico['Auteur']=From
    dico['Destinataire']=To
    dico['Reponse']=Sub
    dico['Date_envoi']=Date
    df=pd.DataFrame(dico)
    df.to_csv(r'/home/math/Documents/prototype/tableau.csv',index=False,header=True)
    print(df)
