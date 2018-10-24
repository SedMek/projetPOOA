import os
os.chdir('static')
try: os.chdir('data')
except:
    os.mkdir('data')
    os.chdir('data')

try: os.chdir('series_users')
except:
    os.mkdir('series_users')
    os.chdir('series_users')

def save(series_id,unique_name):
    """crée ou met à jour un fichier contenant les utilisateurs intéressés par une série"""
    try: f = open("series_users", "r")
    except: f=open("series_users","a"); f.write("{}"); f.close(); f = open("series_users", "r")
    d=f.read()
    f.close()
    d=eval(d)
    if series_id in d.keys(): d[series_id].add(unique_name)
    else: d[series_id]=set(); d[series_id].add(unique_name)
    f=open("series_users","w")
    f.write(str(d))
    f.close()

class User:
    """
    This class defines user objects
    """
    id_counter = 0

    def __init__(self, unique_name, first_name, last_name, login, fav_series=None):
        self.id = User.id_counter + 1  # TODO Maybe we should use Hash code for the id
        User.id_counter += 1
        self.unique_name=unique_name
        self.login = login  # TODO Maybe we should use Hash code for login
        # TODO Should we store the password in the user instance, or keep it in a seperate file
        self.first_name = first_name
        self.last_name = last_name
        self.fav_series = fav_series
        
    def add_series(self, series_id):
        if series_id == 0:  # if the user doesn't want to add any series
            pass
        else:
            self.fav_series.append(series_id)
            save(int(series_id),self.unique_name)

    def __repr__(self):
        return "id: {}\nfirst_name: {}\nlast_name: {}\nlogin: {}\nfav_series: {}".format(self.id, self.first_name,
                                                                                         self.last_name, self.login,
                                                                                         self.fav_series)

    def __str__(self):
        return self.__repr__()


