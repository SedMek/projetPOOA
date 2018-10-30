#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:50:55 2018

@author: souheillassouad
"""

import smtplib
import random
import string

def envoi_mail(id_utilisateur,serie,num_dernier_episode):
    
    gmail_user = "envoi.mail.pooa@gmail.com"
    gmail_pwd = "Pooa2019"
    TO = id_utilisateur
    SUBJECT = "Notification : nouvel episode de la serie {}".format(serie)
    TEXT = "L'épisode {} de la série {} est à présent disponible. Rendez-vous sur notre plateforme pour en savoir plus".format(num_dernier_episode,serie)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
        'From: %s' % gmail_user,
        'Subject: %s' % SUBJECT,
        '', TEXT]).encode('utf-8')

    server.sendmail(gmail_user, [TO], BODY)
    print ('email sent')
    
    

def generation_mot_de_passe(id_utilisateur):
    l=str()
    for i in range(1):
        l+=random.choice(string.ascii_uppercase)
    for i in range(5):
        l+=random.choice(string.ascii_lowercase)
    for i in range(2):
        l+=random.choice("123456789")
    return l 

def envoi_mail_changement_mot_de_passe(id_utilisateur):
    
    gmail_user = "envoi.mail.pooa@gmail.com"
    gmail_pwd = "Pooa2019"
    TO = id_utilisateur
    SUBJECT = "Changement de mot de passe"
    TEXT = "Votre nouveau mot de passe est {}".format(generation_mot_de_passe(id_utilisateur))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
        'From: %s' % gmail_user,
        'Subject: %s' % SUBJECT,
        '', TEXT]).encode('utf-8')

    server.sendmail(gmail_user, [TO], BODY)
    print ('email sent')
    

    



    
