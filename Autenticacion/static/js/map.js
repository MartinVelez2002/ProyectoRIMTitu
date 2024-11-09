function initMap(){
    const map = new google.maps.Map(document.getElementById("map"),{
        center: { lat: -2.13396, lng: -79.59337 },
        zoom: 10,
    });

    map.addListener("click", (e))
}