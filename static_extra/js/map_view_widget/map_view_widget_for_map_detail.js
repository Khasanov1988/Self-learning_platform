function initKMZLayer(name, map){
    let kmzLayer = new google.maps.KmlLayer({
        url: 'https://geotest.tech/media/' + name + '?hash=${timestamp}',
        map: map,
        suppressInfoWindows: true,
        preserveViewport: false,
    });

    const toggleKmlLayerButton = document.createElement('button');
    toggleKmlLayerButton.textContent = `Toggle ${name} map Layer`;
    toggleKmlLayerButton.classList.add('custom-map-control-button');
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(toggleKmlLayerButton);


    toggleKmlLayerButton.addEventListener('click', function () {
        if (kmzLayer.getMap() === null) {
            kmzLayer.setMap(map);
            toggleKmlLayerButton.textContent = `Hide ${name} map Layer`;
        } else {
            kmzLayer.setMap(null);
            toggleKmlLayerButton.textContent = `Show ${name} map Layer`;
        }
    });
}

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 3,
        center: {lat: -28.024, lng: 140.887},
        mapTypeId: 'satellite',
    });

    initKMZLayer(mapFileName, map);

    const infoWindow = new google.maps.InfoWindow({
        content: "",
        disableAutoPan: true,
    });
}

window.initMap = initMap;