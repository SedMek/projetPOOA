const POSTER_PATH="https://image.tmdb.org/t/p/w200/";
let result = null;

$.getJSON("/storage", function (data) {result = data});

function show_info_by_id(series_id) {
    let series = result[series_id];
    let networks = "";
    for (var i = 0; i < series.networks.length; i++) {
        networks = networks + series.networks[i].name;
    };

    $("#poster").attr("src", POSTER_PATH + series.poster_path);
    $("#title").text(series.name);
    $("#networks").text(networks);

    $("#overview").text(series.overview);

    $(".series_info_block").show();
}