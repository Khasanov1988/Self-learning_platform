function mapMaker(infoPointLatitude, infoPointLongitude) {
    // Make map window from map_iframe with marker with special coordinates
    let map = document.getElementById('map_iframe');
    map.src = `https://www.google.com/maps/embed/v1/place?key=AIzaSyBLm1b3FFisaX7FvbChYS_MkI9MhqifCJI&q=${infoPointLatitude},${infoPointLongitude}&maptype=satellite`;
}

function mapMultyPointMaker() {
    // Make map window from map field with markers with special coordinates

}

function infoSpotMaker(item, infoSpotData) {
    // Prepare infoSpot data for panorama
    const currentInfoSpot = infoSpotData
    const title_text = currentInfoSpot['title'];
    const description = currentInfoSpot['description'];
    const figures_3d_id = currentInfoSpot['figure_3d_id'];
    const figures_thin_section_id = currentInfoSpot['figure_thin_section_id'];
    const preview = currentInfoSpot['preview'];
    const youtube = currentInfoSpot['youtube_for_iframe'];
    const figures_thin_section_preview = currentInfoSpot['figure_thin_section_preview'];
    const figures_3d_link_for_iframe = currentInfoSpot['figure_3d_link_for_iframe'];

    let infoSpot = new PANOLENS.Infospot(200, PANOLENS.DataImage.Info);
    infoSpot.position.set(item['coord_X'], item['coord_Y'], item['coord_Z']);

    if (description || figures_3d_id || figures_thin_section_id || preview || youtube) {
        // Getting a reference to DOM elements
        let container = document.getElementById('desc-container').cloneNode(true);
        let figures_3d = container.querySelector('#desc-container .wrapper');
        let figures_thin_section = container.querySelector('#desc-container .md_image-container_for_window');
        let image = container.querySelector('#desc-container .preview_image');
        let iframe = container.querySelector('#desc-container .youtube_iframe');
        let title = container.querySelector('#desc-container .title');
        let text = container.querySelector('#desc-container .text');
        let thin_section_link = container.querySelector('#figures_thin_section_window .md_image-container_href');
        let thin_section_img = container.querySelector('#figures_thin_section_window .md_image');
        let figures_3d_iframe = container.querySelector('#desc-container .figure_3d_iframe_class');

        // Adding text to tags with the title and text classes
        if (figures_3d_id) {
            figures_3d_iframe.src = figures_3d_link_for_iframe + '+spin+bg-2b3035ff+dl,share,link,border-hidden';
        } else {
            figures_3d.style.display = 'none';
        }
        // Adding figures_thin_section
        if (figures_thin_section_id) {
            thin_section_link.href = `/applications/virtual_microscope/${figures_thin_section_id}/`;
            thin_section_img.src = '/media/' + figures_thin_section_preview;
        } else {
            figures_thin_section.style.display = 'none';
        }
        // Changing the src of the img tag
        if (preview) {
            image.src = '/media/' + preview;
        } else {
            image.style.display = 'none';
        }
        // Changing the src of the iframe tag
        if (youtube) {
            iframe.src = youtube;
            iframe.title = title;
        } else {
            iframe.style.display = 'none';
        }
        // Adding text to tags with the title and text classes
        title.textContent = title_text;
        if (description) {
            text.textContent = description;
        } else {
            text.style.display = 'none';
        }
        infoSpot.addHoverElement(container, 270);
    } else {
        infoSpot.addHoverText(title_text);
    }
    return infoSpot;
}

function panoramaMaker(imagePath, panoramaId, infoSpotCoordList, infoSpotDict, linkSpotCoordList = null) {
    // Prepare panorama for Viewer
    let panorama = new PANOLENS.ImagePanorama(imagePath);
    let linkSpotsIdDict = {};
    if (infoSpotCoordList) {
        for (let item of infoSpotCoordList) {
            if (item['panorama_id'] == panoramaId) {
                let infoSpotData = infoSpotDict[item['info_spot_id']];
                let infoSpot = infoSpotMaker(item, infoSpotData);
                panorama.add(infoSpot);
            }
        }
    }
    if (linkSpotCoordList) {
        for (let linkSpot of linkSpotCoordList) {
            if (linkSpot['panorama_from_id'] == panoramaId) {
                linkSpotsIdDict[linkSpot['panorama_to_id']] = {
                    'id': linkSpot['panorama_to_id'],
                    'coord_X': linkSpot['coord_X'],
                    'coord_Y': linkSpot['coord_Y'],
                    'coord_Z': linkSpot['coord_Z'],
                }

            }
        }
    }
    return {
        panorama: panorama,
        linkSpotsIdDict: linkSpotsIdDict,
        linkSpotsIdList: Object.values(linkSpotsIdDict)
    };
}

const logoPathToAirPano = '/media/decor/marker_air.png';
const logoPathToGroundPano = '/media/decor/marker_air.png';
const logoPathToOtherPano = '/media/decor/marker_air.png';
const logoPathToInfoSpot = '/media/decor/marker_info_spot.png';
let viewerPanoDict = {};

let viewersList = [];

if (panoramaDict) {
    // Situation for MaterialDetailView
    const panoramaWindows = document.querySelectorAll('.pano-image');
    panoramaWindows.forEach((panoramaWindow) => {

        const currentFigureId = panoramaWindow.id.split('_')[1];
        let mainPanoramaId;


        for (let item of material_photos_list) {
            if (item.pk == currentFigureId) {
                mainPanoramaId = item.fields.pano_view;
            }
        }

        const mainPanoramaPath = panoramaDict[mainPanoramaId].view
        for (let item of panoramaList) {
            let panoramaId = item['pk'];
            let panoramaPath = item['view'];
            viewerPanoDict[panoramaId] = panoramaMaker(panoramaPath, panoramaId, infoSpotCoordList, infoSpotDict, linkSpotCoordList)
        }

        let viewerPanoList2 = Object.values(viewerPanoDict);
        for (let panoFrom of viewerPanoList2) {
            if (panoFrom.linkSpotsIdList) {
                for (let panorama_to of panoFrom.linkSpotsIdList) {
                    let logo_path;
                    if (panoramaDict[panorama_to.id].pano_type === 'air') {
                        logo_path = logoPathToAirPano;
                    } else if (panoramaDict[panorama_to.id].pano_type === 'ground') {
                        logo_path = logoPathToGroundPano;
                    } else {
                        logo_path = logoPathToOtherPano;
                    }
                    panoFrom.panorama.link(viewerPanoDict[panorama_to.id].panorama, new THREE.Vector3(panorama_to.coord_X, panorama_to.coord_Y, panorama_to.coord_Z), 350);
                }
            }
        }

        let viewer = new PANOLENS.Viewer({
            container: panoramaWindow, // A Element container
            autoRotate: true,
            autoRotateSpeed: 0.2,
            controlBar: true, // Vsibility of bottom control bar
            controlButtons: ['fullscreen', 'video'], // Buttons array in the control bar. Default to ['fullscreen', 'setting', 'video']
            autoHideControlBar: false, // Auto hide control bar
            autoHideInfospot: true, // Auto hide infospots
            horizontalView: false, // Allow only horizontal camera control
            cameraFov: 70, // Camera field of view in degree
            reverseDragging: false, // Reverse orbit control direction
            enableReticle: false, // Enable reticle for mouseless interaction
            dwellTime: 1500, // Dwell time for reticle selection in millisecond
            autoReticleSelect: true, // Auto select a clickable target after dwellTime
            viewIndicator: true, // Adds an angle view indicator in upper left corner
            indicatorSize: 60, // Size of View Indicator
            output: 'console' // Whether and where to output infospot position. Could be 'console' or 'overlay'
        });

        let finalPanoramas = [];
        let viewerPanoList = Object.values(viewerPanoDict);
        for (let obj of viewerPanoList) {
            const panorama = obj.panorama; // Получаем значение по ключу panorama
            finalPanoramas.push(panorama); // Собираем все панорамы в массив
        }
        // We rebuild the list so that the initial panorama is at the end and thus is ordered by default
        let finalPanoramasSwapped = [];
        let temp;
        for (let item of finalPanoramas) {
            if (item.src === mainPanoramaPath) {
                temp = item;
            } else {
                finalPanoramasSwapped.push(item);
            }
        }
        finalPanoramasSwapped.unshift(temp)
        viewer.add(...finalPanoramasSwapped);
        viewersList.push(viewer);
    });


} else {
    // Situation for 360viewDetailView
    let viewerPanoDict = {};
    viewerPanoDict[imgId] = panoramaMaker(imgPath, imgId, infoSpotCoordList, infoSpotDict);
    const mapForm = document.getElementById('map_iframe')
    if (mapForm) {
        mapMaker(infoPointLatitude, infoPointLongitude)
    }

    const panoramaWindow = document.querySelector('.pano-image');
    const viewer = new PANOLENS.Viewer({
        container: panoramaWindow, // A Element container
        autoRotate: true,
        autoRotateSpeed: 0.2,
        controlBar: true, // Vsibility of bottom control bar
        controlButtons: ['fullscreen', 'video'], // Buttons array in the control bar. Default to ['fullscreen', 'setting', 'video']
        autoHideControlBar: false, // Auto hide control bar
        autoHideInfospot: true, // Auto hide infospots
        horizontalView: false, // Allow only horizontal camera control
        cameraFov: 70, // Camera field of view in degree
        reverseDragging: false, // Reverse orbit control direction
        enableReticle: false, // Enable reticle for mouseless interaction
        dwellTime: 1500, // Dwell time for reticle selection in millisecond
        autoReticleSelect: true, // Auto select a clickable target after dwellTime
        viewIndicator: true, // Adds an angle view indicator in upper left corner
        indicatorSize: 60, // Size of View Indicator
        output: 'console' // Whether and where to output infospot position. Could be 'console' or 'overlay'
    });

    let finalPanoramas = [];
    let viewerPanoList = Object.values(viewerPanoDict);
    for (let obj of viewerPanoList) {
        const panorama = obj.panorama; // Получаем значение по ключу panorama
        finalPanoramas.push(panorama); // Собираем все панорамы в массив
    }

    viewer.add(...finalPanoramas);
    viewersList.push(viewer);

}

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 3,
        center: {lat: -28.024, lng: 140.887},
        mapTypeId: 'satellite',
    });
    const infoWindow = new google.maps.InfoWindow({
        content: "",
        disableAutoPan: true,
    });
    // Create an array of alphabetical characters used to label the markers.
    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    // Add some markers to the map.
    const markers = my_markers.map((my_marker, i) => {
        const label = labels[i % labels.length];
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
                icon_path = 'M47.04,14.27c-0.31-0.15-0.67-0.13-0.96,0.06s-0.47,0.5-0.47,0.85l0,11.7c0,0.55,0.45,1,1,1c0.55,0,1-0.45,1-1l0-10.05  c3.45,1.98,5.39,4.49,5.39,7.02c0,0,0,0,0,0.01v0.04c-0.04,5.96-10.56,10.98-23,10.98c-12.43,0-22.93-5.02-23-10.96v-0.05  c0,0,0-0.01,0-0.01c0.01-2.53,1.95-5.03,5.39-7.01l0,10.05c0,0.55,0.45,1,1,1c0.55,0,1-0.45,1-1l0-11.7c0-0.34-0.18-0.66-0.47-0.85  s-0.66-0.2-0.96-0.06C7.83,16.73,5,20.13,5,23.85c0,0.02,0,0.04,0,0.06v17.95c0,7.3,10.98,13.02,25,13.02c14.02,0,25-5.72,25-13.02  V23.89c0-0.01,0-0.03,0-0.04C55,20.13,52.17,16.73,47.04,14.27z M53,41.86c0,5.97-10.53,11.02-23,11.02S7,47.83,7,41.86V29.04  c3.78,4.64,12.54,7.82,23,7.82c10.45,0,19.22-3.18,23-7.82V41.86z M17.54,17.58c0,6.87,5.59,12.46,12.46,12.46s12.46-5.59,12.46-12.46S36.87,5.12,30,5.12S17.54,10.71,17.54,17.58z   M40.46,17.58c0,5.77-4.69,10.46-10.46,10.46s-10.46-4.69-10.46-10.46S24.23,7.12,30,7.12S40.46,11.81,40.46,17.58z M27.12,12.13c-0.33,0.17-0.53,0.51-0.53,0.88v9.14c0,0.37,0.2,0.71,0.53,0.88c0.15,0.08,0.31,0.12,0.47,0.12  c0.19,0,0.39-0.06,0.56-0.17l6.82-4.57c0.28-0.19,0.44-0.5,0.44-0.83s-0.17-0.65-0.44-0.83l-6.82-4.57  C27.84,11.97,27.44,11.95,27.12,12.13z M28.59,14.88l4.03,2.7l-4.03,2.7V14.88z';
                icon_scale = 0.8;
                icon_anchor = new google.maps.Point(22, 38);
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
            fillColor: "rgb(255,255,255)",
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
        if (my_marker.panoramaPk) {
            marker.addListener("click", function () {
                // Получить идентификатор панорамы, связанной с этим маркером
                const panoramaId = my_marker.panoramaPk;
                // Сменить панораму во viewer
                viewersList[0].setPanorama(viewerPanoDict[panoramaId].panorama);

            });
        }
        return marker;
    });

    // Add a marker clusterer to manage the markers.
    //new MarkerClusterer({markers, map});
    const markerCluster = new markerClusterer.MarkerClusterer({map, markers});

    let bounds = new google.maps.LatLngBounds();
    locations.forEach(position => {
        bounds.extend(position);
    });

    map.fitBounds(bounds);
}

let my_markers = [];
let locations = [];

for (let item of panoramaList) {
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

for (let item of Object.values(infoSpotDict)) {
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

window.initMap = initMap;