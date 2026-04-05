const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileElem');
const gallery = document.getElementById('gallery');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('results');
const resultList = document.getElementById('result-list');
const cameraBtn = document.getElementById('camera-btn');
const captureBtn = document.getElementById('capture-btn');
const cameraContainer = document.getElementById('camera-container');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resetBtn = document.getElementById('reset-btn');

let stream = null;

// Initialize drag & drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
});

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

// Camera functionality
cameraBtn.addEventListener('click', async () => {
    if (cameraContainer.classList.contains('hidden')) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            cameraContainer.classList.remove('hidden');
            cameraBtn.innerText = '카메라 종료';
        } catch (err) {
            alert('카메라에 접근할 수 없습니다: ' + err.message);
        }
    } else {
        stopCamera();
    }
});

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    cameraContainer.classList.add('hidden');
    cameraBtn.innerText = '실시간 카메라 사용';
}

captureBtn.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob((blob) => {
        const file = new File([blob], 'capture.png', { type: 'image/png' });
        uploadFile(file);
        stopCamera();
    }, 'image/png');
});

// Upload functionality
async function uploadFile(file) {
    // Show preview
    previewFile(file);
    
    // UI states
    resultsSection.classList.add('hidden');
    loading.classList.remove('hidden');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || '이미지를 분석하는 데 실패했습니다.');
        }

        const data = await response.json();
        showResults(data);
    } catch (err) {
        alert(err.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        gallery.innerHTML = `<img src="${reader.result}" alt="Preview">`;
    };
}

function showResults(data) {
    resultList.innerHTML = '';
    resultsSection.classList.remove('hidden');
    
    data.forEach((match, index) => {
        const percentage = (match.similarity * 100).toFixed(1);
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>Top ${index + 1}: ${match.name}</h3>
            <div class="similarity-text">유사도: ${percentage}%</div>
            <div class="similarity-bar">
                <div class="similarity-progress" style="width: 0%"></div>
            </div>
        `;
        resultList.appendChild(card);
        
        // Trigger bar animation
        setTimeout(() => {
            card.querySelector('.similarity-progress').style.width = `${percentage}%`;
        }, 100);
    });
}

resetBtn.addEventListener('click', () => {
    resultsSection.classList.add('hidden');
    gallery.innerHTML = '';
    fileInput.value = '';
});
