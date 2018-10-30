const POSTER_PATH="https://image.tmdb.org/t/p/w200/";

console.log("hey")



var stringData = $.ajax({
                    url: "/notify",
                    async: false

                 }).responseText;
var dico = JSON.parse(stringData);

let i=0;

alert("Trois notifications de démonstration vont arriver dans peu de temps ! Le reste des notifications va dépendre de vos ajouts de séries ;) " +
    " Voir le fichier static/notify.json et le fichier venv/notifications_observer_pattern pour comprendre le système de notification");


var notif=setInterval(new_notif, 7000);

function new_notif() {

    if (i<=2) {
    var user = "user_" + i.toString();

    alert(eval("dico." + user));
    i++
    }

}



function show_series_info(series) {
    let networks = "";
    for (var i = 0; i < series.networks.length; i++) {
        networks = series.networks[i].name + " & " + networks;
    };
    networks = networks.substring(0, networks.length-3);

    let genres = "";
    for (var i = 0; i < series.genres.length; i++) {
        genres = series.genres[i].name + " & " + genres;
    };
    genres = genres.substring(0, genres.length-3);

    let remove_link = $("#remove-link").attr("href");
    remove_link = remove_link.substring(0, remove_link.lastIndexOf("/")+1) + series.id;

    $("#poster").attr("src", POSTER_PATH + series.poster_path);
    $("#title").text(series.name);
    $("#networks").text(networks);
    $("#genres").text(genres);
    $("#overview").text(series.overview);
    $("#remove-link").attr("href", remove_link);

    $(".series_info_block").show();
}
