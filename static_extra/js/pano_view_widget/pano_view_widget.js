function infoSpotMaker(item, infoSpotData, infoSpotSizeCorrection) {
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

    let infoSpot = new PANOLENS.Infospot(infoSpotSizeCorrection, customInfoSpotIcon);
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

function panoramaMaker(imagePath, panoramaId, infoSpotCoordList, infoSpotDict, viewer, linkSpotCoordList = null, panoramaWindow = null) {
    // Prepare panorama for Viewer
    let panorama = new PANOLENS.ImagePanorama(imagePath);
    let linkSpotsIdDict = {};
    let koefA;
    let koefB;
    let type;
    if (infoSpotCoordList) {
        for (let item of infoSpotCoordList) {
            if (item['panorama_id'] == panoramaId) {
                let infoSpotData = infoSpotDict[item['info_spot_id']];
                if (panoramaDict) {
                    type = panoramaDict[panoramaId]['pano_type'];
                } else {
                    type = infoPointPanoType;
                }
                if (type === 'air') {
                    koefA = -9 / 70000;
                    koefB = 79 / 70;
                } else {
                    koefA = -1 / 10;
                    koefB = 3 / 2;
                }
                let infoSpotSizeCorrection = 200 * Math.max(0.5, Math.min((item['distance'] * koefA + koefB), 1.2));
                let infoSpot = infoSpotMaker(item, infoSpotData, infoSpotSizeCorrection);
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
                    'distance': linkSpot['distance'],
                }

            }
        }
    }
    let intertretatoinCardsList = []
    if (panoramaDict && panoramaInterpretationDict[panoramaId]) {
        const path = '/media/';
        // Add card for original panorama
        let photo = document.createElement('div');
        let url = imagePath;
        photo.classList.add('photo');
        photo.style.backgroundImage = 'url(' + url + ')';
        photo.texture = new THREE.TextureLoader().load(url);
        photo.setAttribute('title-text', 'Original Panorama');
        photo.addEventListener('click', function () {
            viewerPanoDict[panoramaId]['panorama'].updateTexture(this.texture);
        });
        intertretatoinCardsList.push(photo);
        // Add cards for interpretations
        for (let item of panoramaInterpretationDict[panoramaId]) {
            let photo = document.createElement('div');
            let url = path + item['view'];
            photo.classList.add('photo');
            photo.style.backgroundImage = 'url(' + url + ')';
            photo.texture = new THREE.TextureLoader().load(url);
            photo.setAttribute('title-text', `${item['title']} by ${item['autor']}`);
            photo.addEventListener('click', function () {
                viewerPanoDict[panoramaId]['panorama'].updateTexture(this.texture);
            });
            intertretatoinCardsList.push(photo);
        }
    }

    panorama.addEventListener('enter', function () {
        // Get all .photo elements inside the parent element
        const photoElements = panoramaWindow.querySelectorAll('.photo');

        // Loop through the array of elements and remove each of them
        photoElements.forEach(photoElement => {
            photoElement.remove();
        });

        if (viewerPanoDict[panoramaId]['interpretationCards'].length > 0) {
            for (let item of viewerPanoDict[panoramaId]['interpretationCards']) {
                panoramaWindow.appendChild(item);
            }

        }

        viewer.options.panoramaAngleCorrection = panoramaDict[panoramaId].north_correction_angle
    });

    return {
        panorama: panorama,
        linkSpotsIdDict: linkSpotsIdDict,
        linkSpotsIdList: Object.values(linkSpotsIdDict),
        interpretationCards: intertretatoinCardsList,
    };
}

const customAirPanoIcon = 'data:image/png;base64,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';
const customGroundPanoIcon = 'data:image/png;base64,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';
const customOtherPanoIcon = undefined;
const customInfoSpotIcon = 'data:image/png;base64,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';
let viewerPanoDict = {};
let viewersList = [];
const startLookingVector = new THREE.Vector3(-3780.73, -2023.19, -2555.35);

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

            let viewer = new PANOLENS.Viewer({
                container: panoramaWindow, // A Element container
                autoRotate: true,
                autoRotateSpeed: 0.15,
                autoRotateActivationDuration: 10000, // Duration before auto rotatation when no user interactivity in ms
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
                output: 'console', // Whether and where to output infospot position. Could be 'console' or 'overlay'
                initialLookAt: startLookingVector, // Initial looking at vector
                panoramaAngleCorrection: panoramaDict[mainPanoramaId].north_correction_angle, // Angle correcting north direction (if necessary)
            });

            const mainPanoramaPath = panoramaDict[mainPanoramaId].view
            for (let item of panoramaList) {
                let panoramaId = item['pk'];
                let panoramaPath = item['view'];
                viewerPanoDict[panoramaId] = panoramaMaker(panoramaPath, panoramaId, infoSpotCoordList, infoSpotDict, viewer, linkSpotCoordList, panoramaWindow)
            }

            let viewerPanoList2 = Object.values(viewerPanoDict);
            let koefA;
            let koefB;
            for (let panoFrom of viewerPanoList2) {
                if (panoFrom.linkSpotsIdList) {
                    for (let panorama_to of panoFrom.linkSpotsIdList) {
                        let logo_path;
                        if (panoramaDict[panorama_to.id].pano_type === 'air') {
                            logo_path = customAirPanoIcon;
                            koefA = -9 / 70000;
                            koefB = 79 / 70;
                        } else if (panoramaDict[panorama_to.id].pano_type === 'ground') {
                            logo_path = customGroundPanoIcon;
                            koefA = -1 / 10;
                            koefB = 3 / 2;
                        } else {
                            logo_path = customOtherPanoIcon;
                            koefA = -1 / 10;
                            koefB = 3 / 2;
                        }
                        let infoSpotSizeCorrection = 350 * Math.max(0.5, Math.min((panorama_to.distance * koefA + koefB), 1.2));
                        console.log(infoSpotSizeCorrection);
                        panoFrom.panorama.link(viewerPanoDict[panorama_to.id].panorama, new THREE.Vector3(panorama_to.coord_X, panorama_to.coord_Y, panorama_to.coord_Z), infoSpotSizeCorrection, logo_path);

                        // Get the last created Infospot (assuming it is at the end of the linkedSpots array)
                        let spot = panoFrom.panorama.linkedSpots[panoFrom.panorama.linkedSpots.length - 1];

                        // Add our own logic for processing the 'click' event to the Infospot object
                        spot.addEventListener('click', function () {
                            // Logic for processing the 'click' event
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
                            currentMarker = viewerPanoDict[panorama_to.id]['map_marker'];
                            currentMarker.setIcon({
                                path: currentMarker.icon.path,
                                fillColor: "rgb(7,7,96)",
                                fillOpacity: currentMarker.icon.fillOpacity,
                                strokeWeight: currentMarker.icon.strokeWeight,
                                rotation: currentMarker.icon.rotation,
                                scale: currentMarker.icon.scale * 1.4,
                                anchor: currentMarker.icon.anchor,
                            });

                        });

                    }
                }
            }

            let finalPanoramas = [];
            let viewerPanoList = Object.values(viewerPanoDict);
            for (let obj of viewerPanoList) {
                const panorama = obj.panorama; // Get the value from the panorama key
                finalPanoramas.push(panorama); // Collect all panoramas into an array
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
        }
    )
    ;


} else {
    // Situation for 360viewDetailView
    let viewerPanoDict = {};
    const panoramaWindow = document.querySelector('.pano-image');
    const viewer = new PANOLENS.Viewer({
        container: panoramaWindow, // A Element container
        autoRotate: true,
        autoRotateSpeed: 0.15,
        autoRotateActivationDuration: 10000, // Duration before auto rotatation when no user interactivity in ms
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
        output: 'console', // Whether and where to output infospot position. Could be 'console' or 'overlay'
        initialLookAt: startLookingVector, // Initial looking at vector
        panoramaAngleCorrection: infoPointCorrectionAngle, //Angle correcting north direction (if necessary)
    });
    viewerPanoDict[imgId] = panoramaMaker(imgPath, imgId, infoSpotCoordList, infoSpotDict, viewer);
    const mapForm = document.getElementById('map_iframe')
    if (mapForm) {
        mapMaker(infoPointLatitude, infoPointLongitude)
    }

    if (panoramaInterpretationDict[imgId].length > 0) {
        const path = '/media/';
        // Add card for original panorama
        let photo = document.createElement('div');
        let url = imgPath;
        photo.classList.add('photo');
        photo.style.backgroundImage = 'url(' + url + ')';
        photo.texture = new THREE.TextureLoader().load(url);
        photo.setAttribute('title-text', 'Original Panorama');
        photo.addEventListener('click', function () {
            viewerPanoDict[imgId]['panorama'].updateTexture(this.texture);
        });
        panoramaWindow.appendChild(photo);
        // Add cards for interpretations
        for (let item of panoramaInterpretationDict[imgId]) {
            let photo = document.createElement('div');
            let url = path + item['view'];
            photo.classList.add('photo');
            photo.style.backgroundImage = 'url(' + url + ')';
            photo.texture = new THREE.TextureLoader().load(url);
            photo.setAttribute('title-text', `${item['title']} by ${item['autor']}`);
            photo.addEventListener('click', function () {
                viewerPanoDict[imgId]['panorama'].updateTexture(this.texture);
            });
            panoramaWindow.appendChild(photo);
        }
    }

    let finalPanoramas = [];
    let viewerPanoList = Object.values(viewerPanoDict);
    for (let obj of viewerPanoList) {
        const panorama = obj.panorama; // Get the value by the key panorama
        finalPanoramas.push(panorama); // Collect all panoramas into an array
    }

    viewer.add(...finalPanoramas);
    viewersList.push(viewer);

}