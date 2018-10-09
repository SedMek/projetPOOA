import tmdbsimple as tmdb
from pprint import pprint
from PIL import Image
import urllib.request as urllib
import io
import users

tmdb.API_KEY = "f3e96aa12213aa6d0925d98470ba6fec"


def show_image(path):
    try:
        fd = urllib.urlopen("https://image.tmdb.org/t/p/w500/" + path)
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
    except:  # if there is no poster, just create a white photo
        pass
        im = Image.new("RGB", (500,500), "white")
    finally:
        im.show()


def search_series_by_title(title, **kwargs):
    display = bool(kwargs["display"])
    search = tmdb.Search()
    response = search.tv(query=title)
    nb_results = len(response["results"])
    print("{} series were found!".format(nb_results))
    if nb_results > 0:
        for result_counter in range(nb_results):
            pprint("- id: {}, name: {}".format(response["results"][result_counter]["id"],
                                               response["results"][result_counter]["name"]))
            if display:
                show_image(response["results"][result_counter]["poster_path"])
        to_add = int(input("which series do you want to add. Please enter the id > "))
        return to_add
    else:
        pass


def main():
    seddik = users.User("Seddik", "Mekki", "SedMek", [])
    command = str(input("enter series name > "))
    while command != "quit":
        series = search_series_by_title(command, display=1)
        seddik.add_series(series)
        command = str(input("enter series name > "))
    print(seddik)


if __name__ == "__main__":
    main()
