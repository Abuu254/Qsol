

// creating a function yale health
function yaleHealth(){

    // setting  variable yalehealth with the latitude and longitude of Yale Health
    var yalehealth ={lat: 41.315816, lng: -72.927817};

    // creating variable map at the divison with id map
    // ccenter of the map being yale health
    var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 18,
        center: yalehealth,
        mapTypeId: 'satellite'
    });

    new google.maps.Marker({
        position: yalehealth,
        map,
        title: "Yale Health",
    });

}