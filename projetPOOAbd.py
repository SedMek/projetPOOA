#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:56:43 2018

@author: souheillassouad
"""

from mongoengine import connect
import datetime
import our_tmdb
connect('mydb',host='localhost',port=27017) #pour l'instant localhost, voir comment changer par la suite 

#Création d'une base de données utilisateurs, voir avec le groupe comment elle sera implémenté 

class users(DynamicDocument):
    
    firstname = StringField(required = True)
    lastname = StringField(required = True)
    birthday = DateTimeField(required = True)
    login = StringField(required = True)
    password = StringField(required = True)
    favouritemovies = ListField(StringField(default=[]))
    

class seriesData(DynamicDocument):
    
    id_serie=StringField(required=True)
    liste_utilisateur=ListField(StringField(default=[]))
    nombre_episode=IntField(min_value=0)
    
class UserNotFoundException(Exception):
    def __init__(self):
        super.__init__(self)

class IncorrectPasswordException(Exception):
    def __init__(self):
        super.__init__(self)

    
    


#Fonction ajoutant un utilisateur ainsi que ses infos à la base de donnée 
def ajout_infos_user(first_name,last_name,birthday_day,birthday_month,birthday_year,log,passw):
    birthday_day=int(birthday_day)
    birthday_month=int(birthday_month)
    birthday_year=int(birthday_year)
    user=users(firstname=first_name,lastname=last_name,birthday=datetime.datetime(birthday_year,birthday_month,birthday_day),login=log,password=passw,favouritemovies="")
    user.save()

#Fonction rajoutant une série à la liste de séries favoris d'un utilisteur
def ajout_id_serie(id_serie,login_user):
    
    l=users.objects.filter(login=login_user)
    l.favouritemovies.append(id_serie)
    
    l.save()

#Fonction authentification qui renvoie message d'erreur si le login ou le mot de passe est faux 

def authent(log,mot_de_passe):
    
    a=Users.objects.filter(login=log).count()
    
    if a == 0 :
        raise UserNotFoundException("l'utilisateur n'exite pas")
   
    else :
        l=Users.objects.filter(login=log)
        
        if l.password != mot_de_passe:
            raise IncorrectPasswordException("le mot de passe est incorrect")
        
        else:
            return l
        

# Fonction qui cherche dans la collection série si une série et crée, la crée si elle existe pas 
# et rajoute l'identifiant de l'utilisateur à la liste  liste_utilisateur      

def ajout_serie_utilisateur(idSerie,idUtilisateur):
    
    if seriesData.objects.filter(id_serie=idSerie).count()==0:
        a=our_tmdb.Series(idSerie).number_of_episodes
        s=seriesData(id_serie=idSerie,liste_utilisateur=[idUtilisateur],nombre_episode)
        s.save()
    
    else:
        l=seriesData.objects.filter(id_serie=idSerie)
        l.liste_utilisateur.append(idUtilisateur)
        l.save()
        

        
        
        



        

    
    


    
    




