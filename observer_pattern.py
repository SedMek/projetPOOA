import os
import abc
import our_tmdb

os.chdir('static')
try: os.chdir('data')
except:
    os.mkdir('data')
    os.chdir('data')

try: os.chdir('notifications_data')
except:
    os.mkdir('notifications_data')
    os.chdir('notifications_data')


f=open("1425","r")
old=eval(f.read())
f.close()
new=our_tmdb.Series(1425).series_info

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
        # ...


subject = Subject()
concrete_observer = ConcreteObserver()
subject.attach(concrete_observer)
subject.subject_state_comparator()