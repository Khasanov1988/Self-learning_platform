function mapMaker(infoPointLatitude, infoPointLongitude) {
    // Make map window from map_iframe with marker with special coordinates
    let map = document.getElementById('map_iframe');
    map.src = `https://www.google.com/maps/embed/v1/place?key=AIzaSyBLm1b3FFisaX7FvbChYS_MkI9MhqifCJI&q=${infoPointLatitude},${infoPointLongitude}&maptype=satellite`;
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

    let infoSpot = new PANOLENS.Infospot(250, PANOLENS.DataImage.Info);
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
                    'coord_Z': linkSpot['coord_Z']
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


if (panoramaDict) {
    // Situation for MaterialDetailView
    const panoramaWindows = document.querySelectorAll('.pano-image');
    panoramaWindows.forEach((panoramaWindow) => {

        const currentFigureId = panoramaWindow.id.split('_')[1];
        let mainPanoramaId;
        let viewerPanoDict = {};

        for (let item of material_photos_list) {
            if (item.pk == currentFigureId) {
                mainPanoramaId = item.fields.pano_view;
            }
        }
        const mainPanoramaPath = panoramaDict[mainPanoramaId].view
        console.log(mainPanoramaPath)
        for (let item of panoramaList) {
            let panoramaId = item['pk'];
            let panoramaPath = item['view'];
            viewerPanoDict[panoramaId] = panoramaMaker(panoramaPath, panoramaId, infoSpotCoordList, infoSpotDict, linkSpotCoordList)
        }

        let viewerPanoList2 = Object.values(viewerPanoDict);
        for (let panoFrom of viewerPanoList2) {
            if (panoFrom.linkSpotsIdList) {
                for (let panorama_to of panoFrom.linkSpotsIdList) {
                    panoFrom.panorama.link(viewerPanoDict[panorama_to.id].panorama, new THREE.Vector3(panorama_to.coord_X, panorama_to.coord_Y, panorama_to.coord_Z), 270);
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
        console.log(finalPanoramas)
        for (let item of finalPanoramas) {
            if (item.src === mainPanoramaPath) {
                temp = item;
            } else {
                finalPanoramasSwapped.push(item);
            }
        }
        finalPanoramasSwapped.unshift(temp)
        console.log(finalPanoramasSwapped)
        viewer.add(...finalPanoramasSwapped);
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

}