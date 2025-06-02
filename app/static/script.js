const inputMarca = document.getElementById("marca");
const inputLocalidad = document.getElementById("localidad");
const inputNombre = document.getElementById("aspirante");

const createBtn = document.querySelector(".create-button");
const cancelBtn = document.querySelector(".cancel-button");
const actionButtons = document.querySelector(".action-buttons");
const addBtn = document.querySelector(".add-button");
const tableBody = document.querySelector(".table-container tbody");

let filaEditando = null; // Guardará la fila en edición

const iconMap = [
  {
    selector: '.form-row:nth-of-type(2) img.icon',
    original: '/app/static/assets/Icon_vehiculo.svg',
    active: '/app/static/assets/Icon_vehiculo1.svg'
  },
  {
    selector: '.form-row:nth-of-type(3) img.icon',
    original: '/app/static/assets/Icon_puntoubicacion.svg',
    active: '/app/static/assets/Icon_puntoubicacion1.svg'
  },
  {
    selector: '.form-row:nth-of-type(4) img.icon',
    original: '/app/static/assets/Icon_persona.svg',
    active: '/app/static/assets/Icon_persona1.svg'
  }
];

// Mostrar botones "crear/cancelar" y cambiar íconos
addBtn.addEventListener("click", () => {
  filaEditando = null;
  addBtn.style.display = "none";
  actionButtons.style.display = "flex";

  iconMap.forEach(icon => {
    const img = document.querySelector(icon.selector);
    if (img) img.src = icon.active;
  });
});

// Cancelar acción
cancelBtn.addEventListener("click", () => {
  filaEditando = null;
  inputMarca.value = "";
  inputLocalidad.value = "";
  inputNombre.value = "";
  actionButtons.style.display = "none";
  addBtn.style.display = "inline-block";

  iconMap.forEach(icon => {
    const img = document.querySelector(icon.selector);
    if (img) img.src = icon.original;
  });
});

// Crear o actualizar fila
createBtn.addEventListener("click", () => {
  const marca = inputMarca.value.trim();
  const localidad = inputLocalidad.value.trim();
  const nombre = inputNombre.value.trim();

  if (!marca || !localidad || !nombre) {
    alert("Por favor llena todos los campos.");
    return;
  }

  if (filaEditando) {
    // Actualizar fila existente
    const celdas = filaEditando.querySelectorAll("td");
    celdas[0].textContent = marca;
    celdas[1].textContent = localidad;
    celdas[2].innerHTML = `
      ${nombre}
      <button class="edit-button">
        <img src="/app/static/assets/Icon_editar.svg" alt="Editar">
      </button>
      <button class="delete-button">
        <img src="/app/static/assets/Icon_eliminar.svg" alt="Eliminar">
      </button>
    `;
    filaEditando = null;
  } else {
    // Crear nueva fila
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
      <td>${marca}</td>
      <td>${localidad}</td>
      <td>
        ${nombre}
        <button class="edit-button">
          <img src="/app/static/assets/Icon_editar.svg" alt="Editar">
        </button>
        <button class="delete-button">
          <img src="/app/static/assets/Icon_eliminar.svg" alt="Eliminar">
        </button>
      </td>
    `;
    tableBody.appendChild(nuevaFila);
  }

  // Reset form
  inputMarca.value = "";
  inputLocalidad.value = "";
  inputNombre.value = "";
  actionButtons.style.display = "none";
  addBtn.style.display = "inline-block";

  iconMap.forEach(icon => {
    const img = document.querySelector(icon.selector);
    if (img) img.src = icon.original;
  });
});

// Eventos de la tabla (editar o eliminar)
tableBody.addEventListener("click", (event) => {
  const editBtn = event.target.closest(".edit-button");
  const deleteBtn = event.target.closest(".delete-button");

  if (editBtn) {
    const fila = event.target.closest("tr");
    const celdas = fila.querySelectorAll("td");
    inputMarca.value = celdas[0].textContent.trim();
    inputLocalidad.value = celdas[1].textContent.trim();
    inputNombre.value = celdas[2].childNodes[0].textContent.trim();

    filaEditando = fila;

    // Activar modo edición
    actionButtons.style.display = "flex";
    addBtn.style.display = "none";

    iconMap.forEach(icon => {
      const img = document.querySelector(icon.selector);
      if (img) img.src = icon.active;
    });

    // Cambiar icono de editar
    const img = editBtn.querySelector("img");
    if (img) img.src = "/app/static/assets/Icon_editar1.svg";

  } else if (deleteBtn) {
    const fila = event.target.closest("tr");
    const confirmar = confirm("¿Estás seguro de que deseas eliminar este registro?");
    if (confirmar) fila.remove();
    else {
      // Cambiar icono de eliminar si se activa pero no se elimina
      const img = deleteBtn.querySelector("img");
      if (img) img.src = "/app/static/assets/Icon_eliminar.svg";

      setTimeout(() => {
        if (img) img.src = "/app/static/assets/Icon_eliminar1.svg";
      }, 1000);
    }
  }
});
