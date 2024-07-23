const video = document.getElementById('videoElement');
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const confirmationPopup = document.getElementById('confirmationPopup');
const confirmButton = document.getElementById('confirmButton');
const rejectButton = document.getElementById('rejectButton');
const h3 = document.getElementById('startWork');

let lastImageData;
let motionDetected = false;

// Setup video stream
navigator.mediaDevices.getUserMedia({
        video: true
    })
    .then((stream) => {
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
            setTimeout(() => {
                requestAnimationFrame(checkForMotion);
            }, 500); // Delay to ensure video is ready
        };
    })
    .catch((err) => {
        console.error("Error accessing camera: " + err);
    });

function checkForMotion() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

        if (lastImageData) {
            const diff = detectMotion(lastImageData.data, imageData.data);

            //Motion Threshold: Adjust the 800-1500 threshold in the detectMotion function 
            //based on your environment and sensitivity requirements.
            if (diff > 800) { // Motion threshold
                if (!motionDetected) {
                    motionDetected = true;
                    setTimeout(() => {
                        sendFrameForRecognition(imageData);
                        motionDetected = false;
                    }, 1000); // Delay between checks
                }
            }
        }
        lastImageData = imageData;
    }

    requestAnimationFrame(checkForMotion);
}

function detectMotion(data1, data2) {
    let diff = 0;
    for (let i = 0; i < data1.length; i += 4) {
        const r = data1[i] - data2[i];
        const g = data1[i + 1] - data2[i + 1];
        const b = data1[i + 2] - data2[i + 2];
        diff += Math.abs(r) + Math.abs(g) + Math.abs(b);
    }
    //reduce motion sensitivity by 10 000. for human readability
    return Math.floor(diff / 10000);
}

async function sendFrameForRecognition(imageData) {
    const dataUrl = canvas.toDataURL('image/png');
    const response = await fetch('/face_recognition', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            image: dataUrl
        })
    });
    const result = await response.json();
    handleRecognitionResult(result);
}

function handleRecognitionResult(result) {
    if (result.recognized) {
        const {
            employee_id,
            start_count,
            employee_name,
            employee_photo,
            face_location
        } = result;
        console.log("START: " + start_count)
        console.log("face_location: " + face_location);
        // drawFaceFrame(face_location);

        video.pause();
        confirmationPopup.style.display = 'block';
        h3.innerHTML=" "
        if (!start_count) 
            h3.innerHTML = "Start Work?"
        else
            h3.innerHTML = "End Work?";
        
        document.getElementById('employeeName').textContent = employee_name;
        document.getElementById('employeePhoto').src = `/static/uploads/${employee_photo}`;

        confirmButton.onclick = async () => {
            confirmationPopup.style.display = 'none';
            await fetch('/confirm_employee', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    employee_id: employee_id
                })
            });
            video.play(); // Continue the video stream
            updateActiveEmployees(); // Update the active employees list
        };


        rejectButton.onclick = () => {
            // Handle reject
            confirmationPopup.style.display = 'none';
            // Continue streaming
            video.play(); // Continue the video stream
        };
    }
}

// Function to update the active employees list
async function updateActiveEmployees() {
    const response = await fetch('/get_active_employees');
    const activeEmployees = await response.json();

    activeEmployeesList.innerHTML = ''; // Clear the list
    activeEmployees.forEach(employee => {
        const listItem = document.createElement('li');
        const elapsedTime = (Date.now() - new Date(employee.start_time)) / 1000; // Elapsed time in seconds
        const hours = Math.floor(elapsedTime / 3600);
        const minutes = Math.floor((elapsedTime % 3600) / 60);

        listItem.textContent = `${employee.name} - ${hours}h ${minutes}m`;
        activeEmployeesList.appendChild(listItem);
    });
}

// Function to periodically update active employees list
setInterval(updateActiveEmployees, 60000); // Update every 60 seconds

// Initial call to populate active employees list
updateActiveEmployees();


function drawFaceFrame(face_location) {
    const [top, right, bottom, left] = face_location;
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    ctx.strokeStyle = 'green';
    ctx.lineWidth = 2;
    ctx.strokeRect(left, top, right - left, bottom - top);
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial setup code here if needed
});