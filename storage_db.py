#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:56:43 2018

@author: souheillassouad
"""

from mongoengine import connect, DynamicDocument, StringField, BooleanField, ListField, IntField, DoesNotExist
import datetime
import our_tmdb

connect('pooa_project_db', host='localhost', port=27017)  # pour l'instant localhost, voir comment changer par la suite


class UserNotFoundException(Exception):
    pass


class IncorrectPasswordException(Exception):
    pass


class LoginAlreadyUsedException(Exception):
    pass

    # Création d'une base de données utilisateurs, voir avec le groupe comment elle sera implémenté


class User(DynamicDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    login = StringField(required=True)
    password = StringField(required=True)
    favourite_series = ListField(IntField(default=[]))
    email_notifications = BooleanField(required=True)
    browser_notifications = BooleanField(required=True)


class SeriesData(DynamicDocument):
    id_serie = StringField(required=True)
    liste_utilisateur = ListField(StringField(default=[]))
    nombre_episode = IntField(min_value=0)


# Fonction ajoutant un utilisateur ainsi que ses infos à la base de donnée
def ajout_infos_user(first_name, last_name, log, passw):
    if User.objects.filter(login=log).count() == 0:
        user = User(first_name=first_name, last_name=last_name, login=log, password=passw, favourite_series=[],
                    email_notifications=True, browser_notifications=True)
        user.save()
    else:
        raise LoginAlreadyUsedException("This login is already used. Please use another one!")


def update_user_fav_series(tmdb_user):
    try:
        l = User.objects.get(login=tmdb_user.login)
        l.favourite_series = tmdb_user.favourite_series
        l.save()
    except DoesNotExist:
        raise UserNotFoundException("l'utilisateur n'exite pas")


# Fonction rajoutant une série à la liste de séries favoris d'un utilisteur
def ajout_id_serie_to_fav(id_serie, login_user):
    try:
        l = User.objects.get(login=login_user)

        if id_serie in l.favourite_series:  # if the id already exists, remove it
            l.favourite_series.remove(id_serie)

        l.favourite_series.insert(0, id_serie)  # always add it in first position
        l.save()
    except DoesNotExist:
        raise UserNotFoundException("l'utilisateur n'exite pas")


# Fonction authentification qui renvoie message d'erreur si le login ou le mot de passe est faux

def authent(log, mot_de_passe):
    try:
        a = User.objects.get(login=log)
        if a.password != mot_de_passe:
            raise IncorrectPasswordException("le mot de passe est incorrect")
        else:
            return a
    except DoesNotExist:
        raise UserNotFoundException("l'utilisateur n'exite pas")


# Fonction qui cherche dans la collection série si une série et crée, la crée si elle existe pas
# et rajoute l'identifiant de l'utilisateur à la liste  liste_utilisateur      

def ajout_serie_utilisateur(idSerie, idUtilisateur):
    if SeriesData.objects.filter(id_serie=idSerie).count() == 0:
        a = our_tmdb.Series(idSerie).number_of_episodes
        s = SeriesData(id_serie=idSerie, liste_utilisateur=[idUtilisateur], nombre_episode=a)
        s.save()

    else:
        l = SeriesData.objects.filter(id_serie=idSerie)
        l.liste_utilisateur.append(idUtilisateur)
        l.save()


def update_password_in_db(user_id, new_password):
    user = User.objects.get(login=user_id)
    user.password = new_password
    user.save()


def update_notification_settings(tmdb_user):
    try:
        l = User.objects.get(login=tmdb_user.login)
        l.email_notifications = tmdb_user.email_notifications
        l.browser_notifications = tmdb_user.browser_notifications
        l.save()
    except DoesNotExist:
        raise UserNotFoundException("l'utilisateur n'exite pas")