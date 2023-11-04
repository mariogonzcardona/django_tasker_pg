// Llamada a la función loadTasks cuando se carga la página
document.addEventListener('DOMContentLoaded', loadTasks);

// Proceso para verificar el token de acceso
document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem('access');

    if (!accessToken) {
        // No hay token, redireccionar al login
        window.location.href = "/login";
        return;
    }

    // Aquí debes agregar la verificación del token con tu API
    // Ejemplo (deberás ajustar la URL y el método según tu backend):
    fetch('/api/v1/user/verify-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        },
        body: JSON.stringify({ token: accessToken })
    })
        .then(response => {
            if (!response.ok) {
                // Token inválido o expirado, redireccionar al login
                window.location.href = "/login";
            }
            // Si no hay error, el token es válido y la página de home se carga normalmente
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.href = "/login";
        });
});

// Proceso para hacer logout
document.getElementById('logoutButton').addEventListener('click', function (event) {
    event.preventDefault(); // Para evitar que el enlace navegue a otra página

    const accessToken = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí

    if (!accessToken) {
        console.error('No access token found');
        return;
    }

    fetch('/api/v1/user/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al procesar la solicitud de logout');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.detail); // "Logout successful"
            localStorage.removeItem('access'); // Eliminar el token de localStorage
            localStorage.removeItem('refresh'); // Eliminar el refresh token de localStorage
            window.location.href = "/login"; // Redirigir al usuario al login
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Proceso para crear una tarea
function addTask() {
    const accessToken = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí

    // Obtiene los valores del formulario
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const endDate = document.getElementById('taskEndDate').value;

    // Crea el objeto de datos de la tarea
    const taskData = {
        title: title,
        description: description,
        date_to_finish: endDate
    };

    // Configuración de la solicitud fetch
    fetch('/api/v1/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Aquí deberás incluir también el header de autorización si tu API lo requiere
            'Authorization': 'Bearer ' + accessToken // Así es como añadirías un token de autenticación, por ejemplo
        },
        body: JSON.stringify(taskData)
    })
        .then(response => {
            console.log(response);
            if (response.status === 201) {
                Swal.fire({
                    title: `La tarea fue creada con éxito.`,
                    icon: 'success',
                    showConfirmButton: false,
                    timer: 1500
                }).then((result) => {
                    // Si SweetAlert2 se cierra y la promesa resuelve, entonces cerramos el modal.
                    if (result.isConfirmed || result.isDismissed) {
                        $('#addTaskModal').modal('hide');
                        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                    }
                });
            } else {
                // Al no ser un 201, asumimos que hay un mensaje de error que queremos mostrar.
                // Parseamos el cuerpo de la respuesta a JSON para obtener el mensaje de error.
                response.json().then(data => {
                    Swal.fire(
                        'Error',
                        'No se pudo crear la tarea: ' + data.detail,
                        'error'
                    );
                }).catch(jsonError => {
                    // En caso de que no se pueda parsear el JSON, mostramos un mensaje genérico.
                    Swal.fire(
                        'Error',
                        'No se pudo crear la tarea y no se pudo obtener un mensaje de error del servidor.',
                        'error'
                    );
                });
            }
        })
        .catch(error => {
            // Este catch captura cualquier error que no esté relacionado con el rango de respuestas HTTP (como problemas de red)
            Swal.fire(
                'Error',
                'Hubo un problema con la petición: ' + error.message,
                'error'
            );
        });
}

// Función para cargar tareas
function loadTasks() {
    fetch('/api/v1/tasks/')
        .then(response => response.json())
        .then(data => populateTable(data))
        .catch(error => console.error('Error:', error));
}

// Función para llenar la tabla con los datos de las tareas
function populateTable(data) {
    const tableBody = document.getElementById('tasks_table_body');
    tableBody.innerHTML = ''; // Limpia la tabla antes de añadir los nuevos datos
    data.results.forEach(task => {
        const row = tableBody.insertRow();
        row.innerHTML = `
        <td>${task.id}</td>
        <td>${task.title}</td>
        <td>${task.description}</td>
        <td>${task.user}</td>
        <td>${task.completed ? 'Sí' : 'No'}</td>
        <td>${task.date_to_finish}</td>
        <td>
            <button type="button" class="btn btn-info btn-sm" onclick="editTask(${task.id})"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>
            <button type="button" class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})"><i class="fa fa-trash-o" aria-hidden="true"></i></button>
        </td>
      `;
    });

    // Actualiza el contador de registros
    document.getElementById('tasks_count').textContent = `Total de Tareas: ${data.count}`;
}

// Funciones de editar y eliminar (estos deben estar definidos para manejar eventos)
function editTask(taskId) {
    // Aquí va la lógica para editar la tarea
    console.log('Editing task', taskId);
}

function deleteTask(taskId) {
    // Aquí va la lógica para eliminar la tarea
    console.log('Deleting task', taskId);
}