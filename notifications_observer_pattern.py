
"""ce script est responsable de la generation des notifications dans le cas d'une nouvelle episode par exemple

il est cense etre execute regulierement (toutes les secondes ou toutes les minutes ....) afin de generer

les notifications presque en temps reel

En fonction de son output, ce script alimente le fichier /static/json.notify qui lui même alimente le menu de notifications
dans la page web

"""

import os
import abc
import datetime
import json
import our_tmdb
import storage_db


os.chdir('static')
try: os.chdir('data')
except:
    os.mkdir('data')
    os.chdir('data')

try: os.chdir('notifications_data')
except:
    os.mkdir('notifications_data')
    os.chdir('notifications_data')

series_users=dict()
for e in storage_db.User.objects:
    for s in e.favourite_series:
        if s in series_users.keys(): series_users[s].append(e.login)
        else: series_users[s]=[e.login]

#on va remplir les deux dictionnaires suivants apres le definition des classes
old=dict()
new=dict()


#definition generale du modele observeur-observable pour les notifications
class Subject:

    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    def subject_state_comparator(self):
        """generer une notification dans le cas où old est different de new
        voir definition de old et new ci-dessous
        """
        if old!=new:
            print("New update")
            self._subject_state = new
            self._notify()
        else: print("No new update")


class Observer(metaclass=abc.ABCMeta):

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class ConcreteObserver(Observer):

    def update(self, arg):
        self._observer_state = arg
        f=open("notify.json","r")
        d=eval(f.read())
        f.close()
        for e in series_users.keys():
            try:
                if old[e]!=new[e]:
                    for user in series_users[e]:
                        # le signe @ pose des problèmes pour JS dans les  navigateurs web
                        print(user)
                        d[user.split('@')[0]]=["Nouvelle épisode de %s ! "%our_tmdb.Series(e).name,
                                 str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)]
                        print(d)
            except: pass
        f=open("notify.json","w")
        f.write(json.dumps(d))
        f.close()




#dictionnaire old: informations sur les series stockes dans notre serveur, à comparer avec new ci-dessous
for e in series_users.keys():
    try:
        f=open(str(e),'r')
        old[e]=eval(f.read())["number_of_episodes"]
        f.close()
    except:
        pass

#new l'etat actuel des informations sur les series
for e in series_users.keys():
    new[e]=our_tmdb.Series(e).number_of_episodes


#faire appel aux classes
subject = Subject()
concrete_observer = ConcreteObserver()
subject.attach(concrete_observer)
subject.subject_state_comparator()

#mise à jour notre cache: remplacer les donnees "old" par les nouvelles donnees pour une future comparaison
for e in series_users.keys():
    f=open(str(e),"w")
    f.write(str(our_tmdb.Series(e).series_info))
    f.close()