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

function show_info_by_id(series_id) {
    let series = result[series_id];
    let networks = "";
    for (var i = 0; i < series.networks.length; i++) {
        networks = networks + series.networks[i].name;
    };

    let remove_link = $("#remove-link").attr("href");
    remove_link = remove_link.substring(0, remove_link.lastIndexOf("/")+1) + series.id;

    $("#poster").attr("src", POSTER_PATH + series.poster_path);
    $("#title").text(series.name);
    $("#networks").text(networks);

    $("#overview").text(series.overview);
    $("#remove-link").attr("href", remove_link);

    $(".series_info_block").show();
}
