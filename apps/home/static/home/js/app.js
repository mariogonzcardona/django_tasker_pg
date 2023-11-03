// Ejemplo de código JavaScript en el cliente
document.addEventListener('DOMContentLoaded', function() {
    const url = 'api/v1/tasks';  // La URL de tu endpoint DRF
    const token = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí

    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        // Ahora tienes los datos y puedes proceder a insertarlos en el HTML
        // Esto podría hacerse directamente aquí o podrías pasar los datos a otra función
        displayData(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function displayData(data) {
    // Referencia directa a tbody usando su ID
    const tableBody = document.getElementById('tasks_table_body');
    const results = data.results;
    // Asegurarse de que el contenido del tbody esté vacío antes de añadir nuevos datos
    tableBody.innerHTML = '';

    // Iterar sobre el conjunto de datos y añadir filas a la tabla
    results.forEach(task => {
        // Crear una fila de tabla HTML
        const row = `
            <tr>
                <td>${task.id}</td>
                <td>${task.title}</td>
                <td>${task.description}</td>
                <td>${task.completed}</td>
                <td>${task.date_to_finish}</td>
                <td>${task.user}</td>
                <td>
                    <button onclick="editTask(${task.id})" class="btn btn-primary btn-sm">Editar</button>
                    <button onclick="deleteTask(${task.id})" class="btn btn-danger btn-sm">Eliminar</button>
                </td>
            </tr>
        `;

        // // Añadir la fila creada al cuerpo de la tabla
        tableBody.innerHTML += row;
    });
}

// Suponiendo que tienes funciones para editar y eliminar que aún debes definir
function editTask(id) {
    console.log('Editar tarea', id);
    // Aquí pondrías la lógica para editar la tarea
}

function deleteTask(id) {
    console.log('Eliminar tarea', id);
    // Aquí pondrías la lógica para eliminar la tarea
}