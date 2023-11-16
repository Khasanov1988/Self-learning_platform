let videoPlayer = document.getElementById('videoPlayer');
let frameNumberInput = document.getElementById('frameNumber');
let AAA = document.getElementById('AAA');
let BBB = document.getElementById('BBB');
let NF = document.getElementById('NF');
let NFR = document.getElementById('NFR');
let rotateButton = document.getElementById('rotateButton');

let isRotating = false;

let modeButton = document.getElementById('modeButton');
let isParallelMode = true; // Default mode is "Параллельные николи"

function toggleMode() {
    isParallelMode = !isParallelMode;

    if (isParallelMode) {
        modeButton.textContent = 'Параллельные николи';
        videoPlayer.src = filePPL;
    } else {
        modeButton.textContent = 'Скрещенные николи';
        videoPlayer.src = fileCPL;
    }

    frameNumberInput.value = currentFrame;
    updateFrame();
}

function toggleRotation() {
    isRotating = !isRotating;
    if (isRotating) {
        rotateButton.textContent = 'Выключить вращение';
    } else {
        rotateButton.textContent = 'Включить вращение';
    }
}

function updateFrame() {
    let frameNumber = parseInt(frameNumberInput.value);
    let totalFrames = Math.floor(videoPlayer.duration * 30); // 30 - частота кадров (пример для NTSC)

    if (isNaN(frameNumber) || frameNumber < 0 || frameNumber > 359) {
        alert('Введите корректное значение от 0 до 359.');
        return;
    }

    let seekTime = (frameNumber / totalFrames) * videoPlayer.duration;
    videoPlayer.currentTime = seekTime;
}

videoPlayer.addEventListener('timeupdate', function () {
    let currentFrame = Math.floor(videoPlayer.currentTime * 30); // 30 - частота кадров (пример для NTSC)
    frameNumberInput.value = currentFrame;
});

let isDragging = false;
let nullPoint = 0;
let nullFrame = 0;
let currentFrame = 0;
let rotatingSpeed = 1;

videoPlayer.addEventListener('mousedown', function (event) {
    if (event.button === 0) { // Проверка, что это левая кнопка мыши
        isDragging = true;
        nullPoint = {x: event.clientX, y: event.clientY};
    }
});

document.addEventListener('mouseup', function (event) {
    if (event.button === 0) {
        isDragging = false;
        nullFrame = currentFrame;
    }
});

document.addEventListener('mousemove', function (event) {
    if (isDragging) {
        let percentage = ((event.clientX - nullPoint.x) / videoPlayer.offsetWidth) * rotatingSpeed;
        AAA.value = percentage;
        let frameValue = Math.round(percentage * 359);
        BBB.value = frameValue;
        NF.value = nullFrame;
        currentFrame = (nullFrame + frameValue + 1800) % 360;
        NFR.value = currentFrame;
        frameNumberInput.value = currentFrame;
        if (isRotating) {
            // Реализация вращения видео
            let rotationValue = frameNumberInput.value;
            videoPlayer.style.transform = `rotate(${rotationValue}deg)`;
        }
        updateFrame();
    }
});