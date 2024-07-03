document.getElementById('show-employees-button').addEventListener('click', function() {
    var employeeList = document.getElementById('employee-list');
    if (employeeList.style.display === 'none') {
        fetch('/employees/list')
            .then(response => response.json())
            .then(data => {
                employeeList.innerHTML = '';
                data.employees.forEach(employee => {
                    var employeeDiv = document.createElement('div');
                    employeeDiv.classList.add('employee-profile');
                    employeeDiv.innerHTML = `
                        <h3>${employee.name} (ID: ${employee.id})</h3>
                        <img class="employee_profile" src="${employee.photo_path}" alt="${employee.name}" >
                        <h4>Work Hours:</h4>
                        <ul>
                            ${employee.work_hours.map(wh => `<li>${wh.date}: ${wh.hours_worked}</li>`).join('')}
                        </ul>
                        <button class="delete-button" data-id="${employee.id}">Delete</button>
                    `;
                    employeeList.appendChild(employeeDiv);
                });
                employeeList.style.display = 'block';

                // Add event listeners to delete buttons
                document.querySelectorAll('.delete-button').forEach(button => {
                    button.addEventListener('click', function() {
                        var employeeId = this.getAttribute('data-id');
                        fetch('/employees/delete', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: new URLSearchParams({ 'employee_id': employeeId }),
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                // Remove the employee div
                                this.parentElement.remove();
                            } else {
                                alert(data.message);
                            }
                        });
                    });
                });
            });
    } else {
        employeeList.style.display = 'none';
    }
});