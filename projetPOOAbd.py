#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:56:43 2018

@author: souheillassouad
"""

from mongoengine import connect
import datetime
connect('mydb',host='localhost',port=27017) #pour l'instant localhost, voir comment changer par la suite 

#Création d'une base de données utilisateurs, voir avec le groupe comment elle sera implémenté 

class Users(DynamicDocument):
    
    firstname = StringField(required = True)
    lastname = StringField(required = True)
    birthday = DateTimeField(required = True)
    login = StringField(required = True)
    password = StringField(required = True)
    favouritemovies = ListField(StringField(default=[]))
    


    


#Fonction ajoutant un utilisateur ainsi que ses infos à la base de donnée 
def ajout_infos_user(first_name,last_name,birthday_day,birthday_month,birthday_year,email,log,passw):
    birthday_day=str(birthday_day)
    birthday_month=str(birthday_month)
    birthday_year=str(birthday_year)
    user=Users(firstname=first_name,lastname=last_name,birthday=datetime.datetime(birthday_year,birthday_month,birthday_day),login=log,password=passw,favouritemovies="")
    user.save()

#Fonction rajoutant une série à la liste de séries favoris d'un utilisteur
def ajout_id_serie(id_serie,login_user):
    
    l=Users.objects.filter(login=login_user)
    l.favouritemovies.append(id_serie)
    
    l.save()

#Fonction authentification qui renvoie message d'erreur si le login ou le mot de passe est faux 

def authent(log,mot_de_passe):
    
    a=Users.objects.filter(login=log).count()
    
    if a != 0 :
        print("Cet identifiant n'existe pas")
   
    else :
        l=Users.objects.filter(login=log)
        
        if l.password != mot_de_passe:
            ("Le mot de passe est incorrect")
        
        else:
            return l
        
        



        

    
    


    
    




