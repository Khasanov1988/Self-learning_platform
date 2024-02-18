function initKMZLayer(title, file_name, map) {
    // Get the current host and protocol
    const host = window.location.host;
    const protocol = window.location.protocol;

    // Generate a URL to the KML file based on the current host and protocol
    const kmlUrl = `${protocol}//${host}/media/${file_name}`;
    let kmzLayer = new google.maps.KmlLayer({
        url: kmlUrl,
        map: map,
        suppressInfoWindows: true,
        preserveViewport: true,
    });


    const toggleKmlLayerButton = document.createElement('button');
    toggleKmlLayerButton.textContent = `Toggle ${title} map Layer`;
    toggleKmlLayerButton.classList.add('custom-map-control-button');
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(toggleKmlLayerButton);
    kmzLayer.setMap(null);


    toggleKmlLayerButton.addEventListener('click', function () {
        if (kmzLayer.getMap() === null) {
            kmzLayer.setMap(map);
            toggleKmlLayerButton.textContent = `Hide ${title} map Layer`;
        } else {
            kmzLayer.setMap(null);
            toggleKmlLayerButton.textContent = `Show ${title} map Layer`;
        }
    });


}

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 3,
        center: {lat: -28.024, lng: 140.887},
        mapTypeId: 'satellite',
    });

    map_list.forEach((customMap) => {

        let title = customMap['fields']['title'];
        let file_name = customMap['fields']['map_file'];
        initKMZLayer(title, file_name, map);

    });


    const infoWindow = new google.maps.InfoWindow({
        content: "",
        disableAutoPan: true,
    });
    // Add some markers to the map.
    const markers = my_markers.map((my_marker, i) => {
        const position = my_marker.coords;
        const title = my_marker.title;
        const type = my_marker.type;
        let icon_path;
        let icon_scale;
        let icon_anchor;
        switch (type) {
            case 'air':
                icon_path = 'M256.115,255.272c-7.784,0.01-14.438,2.782-19.96,8.321      c-5.539,5.521-8.315,12.175-8.322,19.959c0.007,7.802,2.783,14.475,8.322,20.017c5.522,5.519,12.176,8.273,19.96,8.262      c7.806,0.012,14.478-2.743,20.021-8.262c5.519-5.542,8.274-12.215,8.263-20.017c0.012-7.784-2.744-14.438-8.263-19.959      C270.593,258.055,263.921,255.282,256.115,255.272z M278.986,189.171h1.339c10.268,0.242,19.211,1.89,26.828,4.946      c7.759,3.14,14.14,7.756,19.146,13.848h90.086v-26.067c-11.027-0.209-21.211-0.714-30.552-1.513      c-6.636-0.569-12.842-1.287-18.623-2.154c-16.513-2.431-24.775-5.359-24.792-8.786c0.017-3.409,8.279-6.338,24.792-8.786      c13.956-2.02,30.349-3.184,49.175-3.491v-1.222c-0.018-1.436,0.196-2.773,0.64-4.016c0.565-1.758,1.536-3.349,2.909-4.771      c2.41-2.394,5.319-3.578,8.729-3.55c3.451-0.028,6.401,1.156,8.848,3.55c2.323,2.355,3.544,5.167,3.664,8.437      c0,0.116,0,0.232,0,0.351v1.222c6.393,0.179,12.503,0.47,18.331,0.873c9.955,0.558,19.053,1.431,27.295,2.618      c0.474,0.089,0.939,0.186,1.396,0.291c15.626,2.372,23.462,5.203,23.512,8.495c-0.05,3.33-7.886,6.181-23.512,8.554      c-0.457,0.085-0.923,0.162-1.396,0.232c-13.051,1.961-28.259,3.144-45.626,3.55v26.185H452c3.431,0.012,6.36,1.233,8.788,3.666      c2.433,2.408,3.655,5.318,3.665,8.729c-0.007,2.427-0.628,4.599-1.862,6.517c-2.114,2.812-5.181,4.789-9.195,5.935      c-33.984,8.146-67.97,16.293-101.957,24.439l38.934,81.582c0.226,0.402,0.439,0.812,0.639,1.221      c9.332,26.235,2.833,47.242-19.495,63.019c-2.808,2.014-5.89,2.753-9.252,2.212c-3.325-0.616-5.965-2.341-7.915-5.181      c-2.017-2.798-2.756-5.882-2.212-9.251c0.584-3.343,2.273-6,5.064-7.971c12.017-8.617,15.49-20.062,10.416-34.331      l-40.911-85.362l-10.65,2.618v42.534c0.005,3.035-0.753,5.867-2.269,8.497v0.057c-1.534,2.613-3.61,4.669-6.227,6.169      l-42.948,24.729v0.06c-2.655,1.509-5.487,2.267-8.497,2.269c-3.023-0.025-5.856-0.8-8.495-2.328l-42.89-24.789l-0.118-0.057      c-2.585-1.536-4.621-3.611-6.11-6.226c-1.519-2.63-2.273-5.444-2.269-8.438v-42.478l-10.707-2.618l-40.912,85.362      c-5.073,14.27-1.603,25.714,10.416,34.331c2.792,1.971,4.48,4.628,5.063,7.971c0.546,3.369-0.193,6.453-2.209,9.251      c-1.951,2.84-4.59,4.564-7.916,5.181c-3.362,0.541-6.446-0.198-9.252-2.212c-22.328-15.776-28.827-36.783-19.495-63.019      c0.2-0.409,0.414-0.818,0.639-1.221l38.934-81.582c-33.987-8.146-67.972-16.293-101.959-24.439      c-4.015-1.146-7.079-3.123-9.193-5.935c-1.234-1.918-1.855-4.09-1.864-6.517c0.011-3.41,1.232-6.32,3.667-8.729      c2.428-2.433,5.358-3.654,8.789-3.666h10.823V181.78c-17.368-0.406-32.576-1.589-45.624-3.55      c-0.473-0.07-0.939-0.147-1.396-0.232c-15.626-2.373-23.462-5.224-23.512-8.554c0.05-3.292,7.886-6.123,23.512-8.495      c0.457-0.105,0.923-0.202,1.396-0.291c8.243-1.188,17.34-2.061,27.292-2.618c5.831-0.403,11.941-0.694,18.332-0.873v-1.222      c0-0.118,0-0.234,0-0.351c0.123-3.27,1.344-6.081,3.667-8.437c2.446-2.394,5.394-3.578,8.845-3.55      c3.413-0.028,6.322,1.156,8.729,3.55c1.375,1.423,2.346,3.014,2.91,4.771c0.446,1.242,0.659,2.58,0.641,4.016v1.222      c18.827,0.308,35.22,1.472,49.175,3.491c16.513,2.448,24.776,5.377,24.792,8.786c-0.016,3.427-8.279,6.355-24.792,8.786      c-5.781,0.867-11.989,1.585-18.622,2.154c-9.344,0.799-19.527,1.304-30.553,1.513v26.067h90.086      c5.004-6.092,11.387-10.708,19.146-13.848c7.618-3.057,16.561-4.704,26.829-4.946h1.339c1.173-0.039,2.373-0.039,3.607,0h38.524      C276.61,189.132,277.813,189.132,278.986,189.171z M256.058,269.413c3.901,0.014,7.238,1.411,10.01,4.188      c2.76,2.751,4.137,6.069,4.133,9.951c0.004,3.901-1.373,7.237-4.133,10.009c-2.771,2.759-6.108,4.137-10.01,4.13      c-3.883,0.007-7.199-1.371-9.952-4.13c-2.78-2.771-4.176-6.107-4.189-10.009c0.014-3.882,1.409-7.2,4.189-9.951      C248.858,270.824,252.175,269.427,256.058,269.413z';
                icon_scale = 0.08;
                icon_anchor = new google.maps.Point(256, 256);
                break;
            case 'ground':
                icon_path = 'M73.428,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211s10.211-4.581,10.211-10.211\n' +
                    '\t\tC83.639,268.592,79.058,264.011,73.428,264.011z M286.789,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211\n' +
                    '\t\tc5.63,0,10.211-4.581,10.211-10.211C297,268.592,292.419,264.011,286.789,264.011z M179.84,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211c5.63,0,10.211-4.581,10.211-10.211\n' +
                    '\t\tC190.051,268.592,185.47,264.011,179.84,264.011z M94.103,111.86c0.356-2.829-0.427-5.682-2.177-7.933l-4.649-5.984l42.611-28.407h103.158\n' +
                    '\t\tc5.936,0,10.749-4.813,10.749-10.749V23.315c0-5.936-4.813-10.749-10.749-10.749H126.634c-5.936,0-10.749,4.813-10.749,10.749\n' +
                    '\t\tv29.718L74.054,80.921l-3.89-5.008c-3.64-4.688-10.394-5.536-15.081-1.895L4.156,113.574c-2.252,1.749-3.717,4.32-4.072,7.149\n' +
                    '\t\tc-0.356,2.829,0.427,5.682,2.177,7.933l21.763,28.013c2.118,2.728,5.289,4.155,8.495,4.155c2.304,0,4.626-0.737,6.586-2.26\n' +
                    '\t\tl50.927-39.555C92.283,117.26,93.749,114.688,94.103,111.86z M204.951,117.829h-50.222L75.972,249.091c7.668,0.77,14.336,4.985,18.428,11.069l17.037-28.395h57.654v19.605\n' +
                    '\t\tc3.264-1.541,6.906-2.407,10.749-2.407s7.485,0.866,10.749,2.407v-19.605h57.654l17.297,28.828\n' +
                    '\t\tc3.977-6.18,10.571-10.518,18.206-11.44L204.951,117.829z M169.091,210.268h-44.755l44.755-74.592V210.268z M190.588,210.268\n' +
                    '\t\tv-74.592l44.755,74.592H190.588z M226.059,94.257v-6.898c0-2.75-2.25-5-5-5H138.62c-2.75,0-5,2.25-5,5v6.898c0,5.936,4.813,10.749,10.749,10.749h70.941\n' +
                    '\t\tC221.246,105.005,226.059,100.192,226.059,94.257z';
                icon_scale = 0.1;
                icon_anchor = new google.maps.Point(150, 100);
                break;
            case 'info_spot':
                icon_path = 'm48,9c-21.54,0-39,17.46-39,39s17.46,39 39,39 39-17.46 39-39-17.46-39-39-39zm6.117,53.349c-2.943,4.419-5.937,7.824-10.974,7.824-3.438-.561-4.851-3.024-4.107-5.535l6.48-21.462c.159-.525-.105-1.086-.585-1.257-.477-.168-1.413,.453-2.223,1.341l-3.918,4.713c-.105-.792-.012-2.1-.012-2.628 2.943-4.419 7.779-7.905 11.058-7.905 3.117,.318 4.593,2.811 4.05,5.55l-6.525,21.567c-.087,.486 .171,.981 .612,1.137 .48,.168 1.488-.453 2.301-1.341l3.915-4.71c.105,.792-.072,2.178-.072,2.706zm-.873-28.032c-2.478,0-4.488-1.806-4.488-4.464s2.01-4.461 4.488-4.461 4.488,1.806 4.488,4.461c0,2.661-2.01,4.464-4.488,4.464z';
                icon_scale = 0.3;
                icon_anchor = new google.maps.Point(48, 48);
                break;
            // other
            default:
                break;
        }

        const svgMarker = {
            path: icon_path,
            fillColor: "rgb(96,7,7)",
            fillOpacity: 0.85,
            strokeWeight: 0,
            rotation: 0,
            scale: icon_scale,
            anchor: icon_anchor,
        };

        const marker = new google.maps.Marker({
            position: position,
            title: title,
            icon: svgMarker,
        });
        // markers can only be keyboard focusable when they have click listeners
        // open info window when marker is clicked
        marker.addListener("mouseover", () => {
            const contentString = `<div style="color: black;">${title}</div>`;
            infoWindow.setContent(contentString);
            infoWindow.open(map, marker);
        });
        marker.addListener("mouseout", () => {
            infoWindow.close();
        });
        // Mark first panorama
        if (my_marker.panoramaPk == mainPanorama) {
            currentMarker = marker;
            currentMarker.setIcon({
                path: currentMarker.icon.path,
                fillColor: "rgb(7,7,96)",
                fillOpacity: currentMarker.icon.fillOpacity,
                strokeWeight: currentMarker.icon.strokeWeight,
                rotation: currentMarker.icon.rotation,
                scale: marker.icon.scale * 1.4,
                anchor: currentMarker.icon.anchor,
            });
        }
        // Make click event
        if (my_marker.panoramaPk) {
            marker.addListener("click", function () {
                // Get the identifier of the panorama associated with this marker
                const panoramaId = my_marker.panoramaPk;
                if (currentMarker) {
                    currentMarker.setIcon({
                        path: currentMarker.icon.path,
                        fillColor: "rgb(96,7,7)",
                        fillOpacity: currentMarker.icon.fillOpacity,
                        strokeWeight: currentMarker.icon.strokeWeight,
                        rotation: currentMarker.icon.rotation,
                        scale: currentMarker.icon.scale / 1.4,
                        anchor: currentMarker.icon.anchor,
                    });
                }
                currentMarker = marker;
                currentMarker.setIcon({
                    path: currentMarker.icon.path,
                    fillColor: "rgb(7,7,96)",
                    fillOpacity: currentMarker.icon.fillOpacity,
                    strokeWeight: currentMarker.icon.strokeWeight,
                    rotation: currentMarker.icon.rotation,
                    scale: marker.icon.scale * 1.4,
                    anchor: currentMarker.icon.anchor,
                });
                // Change the panorama in the viewer
                viewersList[0].setPanorama(viewerPanoDict[panoramaId].panorama);
            });
        }
        viewerPanoDict[my_marker.panoramaPk] = {
            ...viewerPanoDict[my_marker.panoramaPk], // save all existing attributes
            'map_marker': marker // add a new attribute with the key 'marker' and the value marker
        };
        return marker;
    });

    // Add a marker clusterer to manage the markers.
    //new MarkerClusterer({markers, map});
    const markerCluster = new markerClusterer.MarkerClusterer({map, markers});

    // Create a new instance of google.maps.LatLngBounds() to represent a rectangular geographical area.
    let bounds = new google.maps.LatLngBounds();

    // Iterate over each position in the locations array.
    locations.forEach(position => {
        // Extend the bounds to include the current position.
        bounds.extend(position);
    });

    // Adjust the map viewport to fit the bounds, ensuring that all included positions are visible.
    map.fitBounds(bounds);
}

let my_markers = [];
let locations = [];
let currentMarker;

if (panoramaList.length === 0) {
    panoramaList.push({
        'latitude': Number(infoPointLatitude),
        'longitude': Number(infoPointLongitude),
        'title': infoPointTitle,
        'pano_type': infoPointPanoType,
        'pk': imgId,
    });
}

for (let item of panoramaList) {
    if (item.latitude && item.longitude) {
        locations.push({
            lat: item.latitude,
            lng: item.longitude
        });
        my_markers.push({
            title: item.title,
            type: item.pano_type,
            panoramaPk: item.pk,
            infoSpotPk: null,
            coords: {
                lat: item.latitude,
                lng: item.longitude
            }
        });
    }
}
if (Object.keys(infoSpotDict).length > 0) {
    for (let item of Object.values(infoSpotDict)) {
        if (item.latitude && item.longitude) {
            locations.push({
                lat: item.latitude,
                lng: item.longitude
            });
            my_markers.push({
                title: item.title,
                type: 'info_spot',
                panorama_pk: null,
                infoSpotPk: item.id,
                coords: {
                    lat: item.latitude,
                    lng: item.longitude
                }
            })
        }
    }

}

window.initMap = initMap;