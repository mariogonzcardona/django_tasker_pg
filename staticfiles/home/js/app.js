// Llamada a la función loadTasks cuando se carga la página
document.addEventListener('DOMContentLoaded', loadTasks());

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
            // console.log(data.detail); // "Logout successful"
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
    const title = document.getElementById('add-taskTitle').value;
    const description = document.getElementById('add-taskDescription').value;
    const endDate = document.getElementById('add-taskEndDate').value;

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

// Función para actualizar la paginación
function updatePagination(data) {
    const paginationElement = document.getElementById('pagination');
    paginationElement.innerHTML = ''; // Limpiar la paginación actual

    // Añadir 'Previous' si no estamos en la primera página
    let previousDisabled = !data.previous ? ' disabled' : '';
    paginationElement.innerHTML += `
      <li class="page-item${previousDisabled}">
        <a class="page-link" href="#" onclick="loadPage('${data.previous}')">Previous</a>
      </li>`;

    // Añadir números de página basados en la respuesta de la API (esto es solo un ejemplo y puede requerir ajustes)
    if (data.count && data.results.length) {
        const totalPages = Math.ceil(data.count / data.results.length);
        for (let i = 1; i <= totalPages; i++) {
            paginationElement.innerHTML += `
            <li class="page-item"><a class="page-link" href="#" onclick="loadPage('${window.location.origin}/api/v1/tasks/?page=${i}')">${i}</a></li>`;
        }
    }

    // Añadir 'Next' si no estamos en la última página
    let nextDisabled = !data.next ? ' disabled' : '';
    paginationElement.innerHTML += `
      <li class="page-item${nextDisabled}">
        <a class="page-link" href="#" onclick="loadPage('${data.next}')">Next</a>
      </li>`;
}

// Función para cargar una página específica
function loadPage(url) {
    if (!url) return; // Si la URL no es válida, no hacer nada

    fetch(url)
        .then(response => response.json())
        .then(data => {
            populateTable(data);
            updatePagination(data); // Actualiza la paginación con la nueva página de datos
        })
        .catch(error => console.error('Error:', error));
}

// Asegúrate de llamar a updatePagination(data) dentro de loadTasks()
function loadTasks() {
    fetch('/api/v1/tasks/')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
            updatePagination(data); // Llama a esta función para inicializar la paginación cuando cargas las tareas
        })
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

// Abre el modal con los datos actuales de la tarea
function openEditModal(taskId) {
    // Llama a la API para obtener los datos de la tarea por ID
    fetch(`/api/v1/tasks/${taskId}/`)
        .then(response => response.json())
        .then(task => {
            
            // Rellena el formulario con los datos de la tarea usando los nuevos IDs
            $('#edit-taskTitle').val(task.title);
            $('#edit-taskDescription').val(task.description);
            $('#edit-taskCompleted').val(task.completed.toString());
            $('#edit-taskDateToFinish').val(task.date_to_finish);
            $('#taskId').val(task.id); // Este ID parece ser único, está bien.

            // Muestra el modal
            $('#editTaskModal').modal('show');
        })
        .catch(error => console.error('Error:', error));
}

// Guarda los cambios cuando se hace clic en el botón de guardar
$('#saveTaskChanges').click(function () {
    const accessToken = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí

    // Prepara los datos del formulario para enviar
    const taskId = $('#taskId').val();
    let formData = {
        title: $('#edit-taskTitle').val(),
        description: $('#edit-taskDescription').val(),
        completed: $('#edit-taskCompleted').val() === 'true', // o comparar con '1' si los valores son '1' y '0'
        date_to_finish: $('#edit-taskDateToFinish').val()
    };
    console.log(formData);
    // Llama a la API para actualizar la tarea
    fetch(`/api/v1/tasks/${taskId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken // Así es como añadirías un token de autenticación, por ejemplo
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) {
            throw response;
        }
        return response.json(); // si el status es 200 OK, seguimos adelante
    })
    .then(data => {
        // Cierra el modal y actualiza la tabla o lista de tareas en la interfaz de usuario
        $('#editTaskModal').modal('hide');
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());

        // Muestra el mensaje de éxito con SweetAlert
        Swal.fire({
            title: 'Éxito!',
            text: 'Tarea actualizada correctamente.',
            icon: 'success',
            timer: 1500,
            showConfirmButton: false
        });

        // Recarga la tabla de tareas
        reloadTasks();
    })
    .catch(errorResponse => {
        // Maneja la respuesta de error
        errorResponse.json().then(errorData => {
            console.error('Error:', errorData);
            // Muestra el mensaje de error con SweetAlert
            Swal.fire({
                title: 'Error!',
                text: errorData.detail || 'Ocurrió un error al actualizar la tarea.',
                icon: 'error',
                timer: 1500,
                showConfirmButton: false
            });
        });
        // Cierra el modal y actualiza la tabla o lista de tareas en la interfaz de usuario
        $('#editTaskModal').modal('hide');
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
    });
});

function reloadTasks() {
    const accessToken = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí

    fetch('/api/v1/tasks/', {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        },
    })
    .then(response => response.json())
    .then(data => populateTable(data))
    .catch(error => {
        // Manejar el error aquí
        console.error('Error al recargar las tareas:', error);
    });
}

// Funciones de editar.
function editTask(taskId) {
    // Aquí va la lógica para editar la tarea
    openEditModal(taskId);
}

function deleteTask(taskId) {
    // Confirmar antes de eliminar
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, ¡eliminar!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Si se confirma, procede a eliminar
            const accessToken = localStorage.getItem('access'); // Asumiendo que el token está almacenado aquí
            
            fetch(`/api/v1/tasks/${taskId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + accessToken // Así es como añadirías un token de autenticación, por ejemplo
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json(); // si el status es 200 OK, seguimos adelante
            })
            .then(data => {
                // Muestra el mensaje de éxito con SweetAlert
                Swal.fire({
                    title: 'Eliminado!',
                    text: 'La tarea ha sido eliminada.',
                    icon: 'success',
                    timer: 1500,
                    showConfirmButton: false
                });

                // Recarga la tabla de tareas
                reloadTasks();
                
            })
            .catch(errorResponse => {
                // Maneja la respuesta de error
                errorResponse.json().then(errorData => {
                    console.error('Error:', errorData);
                    // Muestra el mensaje de error con SweetAlert
                    Swal.fire({
                        title: 'Error!',
                        text: errorData.detail || 'Ocurrió un error al eliminar la tarea.',
                        icon: 'error',
                        timer: 3000,
                        showConfirmButton: true
                    });
                });
            });
        }
    });
}