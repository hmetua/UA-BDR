from django.shortcuts import render
from django.http import HttpResponse
from monappli.models import MessageInfo,EmployeeEnron,DateEnvoi
from django.db import connection

# Create your views here.

#def index(request):
#    return HttpResponse("<header> Accueil </header>")

def	accueil(request):
	return render(request,"accueil.html")



"""
def question1(request):
	return render(request,"question1.html",{'resultat':DateEnvoi.objects.all()})

	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')

		not_this_year = DateEnvoi.objects.filter(timestamp__lte="10-02-2002")
		
		return render(request,"question1.html",{'resultat':not_this_year})
	else:
"""
		


def question1a(request):
	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		searchresult1=EmployeeEnron.objects.raw('SELECT id_mail,nom_prenom,status,number FROM employee_enron JOIN (SELECT auteur,COUNT(*) AS number FROM (SELECT auteur,destinataire FROM (SELECT id_message FROM date_envoi WHERE date_p BETWEEN %s and %s) AS att1,message_info AS m WHERE m.id_message=att1.id_message) AS att2 WHERE att2.auteur !=0 AND att2.destinataire!=0 GROUP BY att2.auteur ORDER BY number DESC) AS att ON id_mail=att.auteur ORDER BY number DESC',[fromdate,todate])

		return render(request,"question1a.html",{'resultat':searchresult1})
	else:
		return render(request,"question1a.html")

def question1b(request):
	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		searchresult=EmployeeEnron.objects.raw('select id_mail,nom_prenom,status,number from employee_enron join (select auteur,count(*) as number from (select auteur,destinataire from (select id_message from date_envoi where date_p between %s and %s) as att1,message_info as m where m.id_message=att1.id_message and m.reponse=1) as att2 where att2.auteur!=0 and att2.destinataire!=0 group by att2.auteur order by number desc) as att on id_mail=att.auteur order by number desc',[fromdate,todate])
		return render(request,"question1b.html",{'resultat':searchresult})
	else:
		return render(request,"question1b.html")

def question1c(request):
	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		searchresult=EmployeeEnron.objects.raw('select id_mail,nom_prenom,status,number from employee_enron join (select auteur,count(*) as number from (select auteur,destinataire from (select id_message from date_envoi where date_p between %s and %s) as att1,message_info as m where m.id_message=att1.id_message and m.reponse=0) as att2 where att2.auteur!=0 and att2.destinataire!=0 group by att2.auteur order by number desc) as att on id_mail=att.auteur order by number desc',[fromdate,todate])
		return render(request,"question1c.html",{'resultat':searchresult})
	else:
		return render(request,"question1c.html")

def question2(request):
	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		cursor = connection.cursor()
		cursor.execute('select c1.nom_prenom as mp,c2.nom_prenom as mo,number from employee_enron c1, employee_enron c2, (select least(tab.auteur,tab.destinataire) as n1,greatest(tab.destinataire,tab.auteur) as n2,count(*) as number from (select auteur,destinataire from (select id_message from date_envoi where date_p between %s and %s) as att1,message_info as m where m.id_message=att1.id_message and m.reponse=0) as tab where tab.auteur!=0 and tab.destinataire!=0 group by n1,n2 order by number desc) as tabf where tabf.n1=c1.id_mail and tabf.n2=c2.id_mail order by number desc',[fromdate,todate])
		searchresult=cursor.fetchall()
		return render(request,"question2.html",{'couple_tableau':searchresult})
	else:
		return render(request,"question2.html")

def question3(request):
	if request.method=="POST":
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		cursor = connection.cursor()
		cursor.execute('select DATE(date_p) as mp,count(*) as number from (select id_message,date_p from date_envoi where date_p between %s and %s) as att group by date_p order by number desc',[fromdate,todate])
		searchresult=cursor.fetchall()
		return render(request,"question3.html",{'date_tableau':searchresult})
	else:
		return render(request,"question3.html")

def question4(request):
	if request.method=="POST":
		nom=request.POST.get('nom')

		cursor = connection.cursor() 
		cursor.execute('select avg(tab11.ml) from (select date(att1.date_p) as mp, avg(att1.moy_mail) as ml from (select date_p,avg(att.mail) as moy_mail from date_envoi,(select distinct id_message as mail from message_info where auteur=(select id_mail from employee_enron where nom_prenom=%s) and reponse=1) as att where id_message=att.mail group by date_p order by date_p desc) as att1 group by date(att1.date_p) order by date(att1.date_p) desc) as tab11',[nom])
		searchresult4a = cursor.fetchall()

		cursor = connection.cursor()
		cursor.execute('select distinct count(*) from message_info where auteur=(select id_mail from employee_enron where nom_prenom=%s) and destinataire=0 or auteur=0 and destinataire=(select id_mail from employee_enron where nom_prenom=%s)',[nom,nom])
		searchresult4b = cursor.fetchall()

		cursor = connection.cursor() #les contacts internes de l'employé : les destinataires de tous ces mails
		cursor.execute('select nom_prenom from employee_enron as att1,(select distinct destinataire from message_info where destinataire!=0 and auteur=(select id_mail from employee_enron where nom_prenom=%s) group by destinataire order by destinataire desc) as att where att.destinataire=att1.id_mail',[nom])
		searchresult4c = cursor.fetchall()

		cursor = connection.cursor() #nom_prenom de l'employé
		cursor.execute('select nom_prenom,status from employee_enron where nom_prenom=%s',[nom])
		searchresult4 = cursor.fetchall()

		cursor = connection.cursor() #emails de l'employée
		cursor.execute('select email from email_employee_info where id_mail=(select id_mail from employee_enron where nom_prenom=%s)',[nom])
		searchresultemail = cursor.fetchall()
		#searchresult4a=DateEnvoi.objects.raw('select identity(integer,1,1) as id,date(att1.date_p) as mp, avg(att1.moy_mail) as ml into newtable from (select date_p,avg(att.mail) as moy_mail from date_envoi,(select distinct id_message as mail from message_info where auteur=(select id_mail from employee_enron where nom=%s)) as att where id_message=att.mail group by date_p order by date_p desc) as att1 group by date(att1.date_p) order by date(att1.date_p) desc',[nom])
		return render(request,"question4.html",{'quest4email':searchresultemail,'quest4a':searchresult4a,'quest4b':searchresult4b,'quest4c':searchresult4c,'quest4premier':searchresult4})
	else:
		return render(request,"question4.html")

def show(request):	
    return render(request,"show.html",{'employees':EmployeeEnron.objects.all()})