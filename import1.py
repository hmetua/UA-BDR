#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import csv
from psycopg2.extras import execute_values

conn=psycopg2.connect(host="data",database="hmetua",user="hmetua",password="712483")
cur=conn.cursor()

data=[]

with open("list_employee_mail.csv","r",newline="",encoding="utf-8") as f:
	lignes=csv.reader(f,delimiter=",",quotechar='"')
	next(lignes)
	for l in lignes:
		data.append(l)

texte = """
INSERT INTO infiltration.list_employee_mail_original(
mail,id_mail)
VALUES %s 
"""

with psycopg2.connect(host="data",database="hmetua",user="hmetua",password="712483") as conn:
	with conn.cursor() as cur:
		execute_values(cur,texte,data)
