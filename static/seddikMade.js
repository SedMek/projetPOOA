const POSTER_PATH="https://image.tmdb.org/t/p/w200/";

console.log("hey")





var notif_json = $.ajax({
                    url: "/notify",
                    async: false

                 }).responseText;

// var current_user= $.ajax({
//                     url: "/who",
//                     async: false
//
//                  }).responseText;


var dico = JSON.parse(notif_json);

let i=0;
let seen=0;

/*
alert("Trois notifications de démonstration vont arriver dans peu de temps ! Le reste des notifications va dépendre de vos ajouts de séries ;) Cliquez sur la cloche pour les visualiser et  " +
    " voir le fichier static/notify.json et le fichier venv/notifications_observer_pattern pour comprendre le système de notification");
*/

//var notif=setInterval(new_notif, 1000);







function new_notif() {

    if (i<=2) {
    var demo = "demo_" + i.toString();

    alert(eval("dico." + demo));
    i++
    }


}



function fill_series_info(series) {
    /* presentation vue */
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

    /* seasons vue */
    $("#mySidenav").empty();
    for (var i = 0; i < series.seasons.length; i++) {
        let season = $("<a>", {href: "#", onclick: "show_season_info("+ JSON.stringify(series.seasons[i]) +")"} );
        season.text("Season "+i);
        $("#mySidenav").append(season);
    };
}

function fill_season_info(season) {
    $("#season_poster").attr("src", POSTER_PATH + season.poster_path);
    $("#season_title").text(season.name);
    if (season.air_date){
        $("#season_air_date").text(season.air_date);
    }else {
        $("#season_air_date").text('To be announced');
    }
    if (season.overview){
        $("#season_overview").text(season.overview);
    }else {
        $("#season_overview").text("No overview has been announced");
    }

}

function show_series_info(series) {
    fill_series_info(series);
    $("#main").hide();
    $("#presentation").show();
    $(".series_info_block").show();
}

let notification_badge = 1;

var main = function() {
  $('.notification img').click(function() {
    $('.notification-menu').toggle();
    document.getElementById("notification").removeAttribute("data-badge");
    document.getElementById("notification").removeAttribute("data-badge");
  });

  $('.post .btn').click(function() {
    $(this).toggleClass('btn-like');
  });
};
$(document).ready(main);


let current_user="demo_user";
let number_of_notifications=eval("dico."+current_user+".length");


window.onload = function() {


   document.getElementById("notification").setAttribute("data-badge", number_of_notifications);

    console.log("dico." + current_user+"[0]");
   for (var i=0; i<eval("dico."+current_user+".length"); i++)
    {
        var block_to_insert ;
        var container_block ;
        block_to_insert = document.createElement( 'li');
        block_to_insert.innerHTML = "<b id=\"notif_0\">"+eval("dico." + current_user + "[" + i.toString() + "][0]")+"</b>\n" +
            "<p + style='text-align: right;'>"+eval("dico." + current_user + "[" + i.toString() + "][1]")+"</p>" ;
        block_to_insert.setAttribute("class","menu-item");

        container_block = document.getElementById( 'notification-menu' );
        container_block.appendChild( block_to_insert );

        // document.getElementById("notif_"+i.toString()).innerHTML = eval("dico." + current_user + "[" + i.toString() + "][0]");
    }
}

function show_season_info(season) {
    fill_season_info(season);
    $("#main").show();
}

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function display_seasons() {
    $("#presentation").hide();
    /* $("#main").show(); */
    openNav();
};

function display_presentation() {
    closeNav();
    $("#main").hide();
    $("#presentation").show();

}

function hide_info_block() {
    display_presentation();
    $("#presentation").hide();
    $("#main").hide();
    $(".series_info_block").hide();
}


