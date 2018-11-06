import smtplib
import random
import string
from storage_db import *


def envoi_mail(id_utilisateur, serie, num_dernier_episode):
    gmail_user = "envoi.mail.pooa@gmail.com"
    gmail_pwd = "Pooa2019"
    TO = id_utilisateur
    SUBJECT = "Notification : nouvel episode de la serie {}".format(serie)
    TEXT = "L'épisode {} de la série {} est à présent disponible. Rendez-vous sur notre plateforme pour en savoir plus".format(
        num_dernier_episode, serie)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_user,
                        'Subject: %s' % SUBJECT,
                        '', TEXT]).encode('utf-8')

    server.sendmail(gmail_user, [TO], BODY)
    print('email sent')


def generate_password():
    l = str()
    for i in range(1):
        l += random.choice(string.ascii_uppercase)
    for i in range(5):
        l += random.choice(string.ascii_lowercase)
    for i in range(2):
        l += random.choice("123456789")
    return l


def send_password_mail(user_mail, new_password):
    gmail_user = "envoi.mail.pooa@gmail.com"
    gmail_pwd = "Pooa2019"
    TO = user_mail
    SUBJECT = "Changement de mot de passe"
    TEXT = "Votre nouveau mot de passe est {}".format(new_password)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_user,
                        'Subject: %s' % SUBJECT,
                        '', TEXT]).encode('utf-8')

    server.sendmail(gmail_user, [TO], BODY)
    print('email sent')


def time_counter(list_of_series):
    counter = 0
    duration = ""
    for element in list_of_series:
        counter += element.number_of_episodes * element.episode_run_time[0]
    days = counter // (24 * 60)
    hours = (counter % (24 * 60)) // 60
    mins = counter % 60
    if days:
        duration = str(days) + " days "
    if hours:
        duration = duration + str(hours) + " hours "
    if mins:
        duration = duration + str(mins) + " minutes"

    if duration:
        return duration
    else:
        return "0 mins"


def join_networks(series):
    network_names = []
    for i in range(len(series.networks)):
        network_names.append(series.networks[i]["name"])

    return " &".join(network_names)
