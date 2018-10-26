const POSTER_PATH="https://image.tmdb.org/t/p/w200/";
let result = null;


/*
var stringData = $.ajax({
                    url: "notify",
                    async: false,
                    dataType: "json",
                 }).responseText;

  //Split values of string data
//var stringArray = stringData.split(",");
alert(stringData);




$.getJSON("/storage", function (data) {result = data});
*/

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
