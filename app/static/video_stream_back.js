const video = document.getElementById('videoElement');
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const activeEmployeesList = document.getElementById('activeEmployeesList');
document.getElementById('confirmationPopup').style.display = 'none';

// Function to handle showing the confirmation popup
function showConfirmationPopup(employee) {
    document.getElementById('employeeName').textContent = employee.employee_name;
    document.getElementById('employeePhoto').src = `/static/uploads/${employee.employee_photo}`;
    document.getElementById('confirmationPopup').style.display = 'block';

    document.getElementById('confirmButton').onclick = async () => {
        document.getElementById('confirmationPopup').style.display = 'none';
        await fetch('/confirm_employee', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: employee.employee_id })
        });
        video.play(); // Continue the video stream
        updateActiveEmployees(); // Update the active employees list
    };

    document.getElementById('rejectButton').onclick = () => {
        document.getElementById('confirmationPopup').style.display = 'none';
        video.play(); // Continue the video stream
    };
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

// Function to handle face recognition
async function fetchFaceRecognition() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');

    const response = await fetch('/face_recognition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    });
    const result = await response.json();
    if (result.recognized) {
        video.pause();
        showConfirmationPopup(result);
    }
}

// Initialize video stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        setInterval(fetchFaceRecognition, 3000); // Check for face recognition every 5 seconds
    })
    .catch(error => console.error('Error accessing media devices.', error));

// Function to periodically update active employees list
setInterval(updateActiveEmployees, 10000); // Update every 60 seconds

// Initial call to populate active employees list
updateActiveEmployees();
