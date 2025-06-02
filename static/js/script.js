// ==============================================
// 1. Configuración inicial y selección de elementos
// ==============================================
const inputMarca = document.getElementById("marca");
const inputLocalidad = document.getElementById("localidad");
const inputNombre = document.getElementById("aspirante");

const createBtn = document.querySelector(".create-button");
const cancelBtn = document.querySelector(".cancel-button");
const actionButtons = document.querySelector(".action-buttons");
const addBtn = document.querySelector(".add-button");
const tableBody = document.querySelector(".table-container tbody");

let filaEditando = null; // Almacena la fila en edición

// Mapeo de íconos (rutas estáticas consistentes)
const iconMap = [
  {
    selector: '.form-row:nth-of-type(2) img.icon',
    original: "/static/assets/Icon_vehiculo.svg",
    active: "/static/assets/Icon_vehiculo1.svg"
  },
  {
    selector: '.form-row:nth-of-type(3) img.icon',
    original: "/static/assets/Icon_puntoubicacion.svg",
    active: "/static/assets/Icon_puntoubicacion1.svg"
  },
  {
    selector: '.form-row:nth-of-type(4) img.icon',
    original: "/static/assets/Icon_persona.svg",
    active: "/static/assets/Icon_persona1.svg"
  }
];

// ==============================================
// 2. Funciones auxiliares
// ==============================================
const resetForm = () => {
  inputMarca.value = "";
  inputLocalidad.value = "";
  inputNombre.value = "";
  actionButtons.style.display = "none";
  addBtn.style.display = "inline-block";
  
  iconMap.forEach(icon => {
    const img = document.querySelector(icon.selector);
    if (img) img.src = icon.original;
  });
};

const toggleIcons = (state) => { // 'active' o 'original'
  iconMap.forEach(icon => {
    const img = document.querySelector(icon.selector);
    if (img) img.src = icon[state];
  });
};

// ==============================================
// 3. Event Listeners
// ==============================================
// Mostrar botones de acción
addBtn.addEventListener("click", () => {
  filaEditando = null;
  addBtn.style.display = "none";
  actionButtons.style.display = "flex";
  toggleIcons('active');
});

// Cancelar acción
cancelBtn.addEventListener("click", resetForm);

// Crear/Actualizar registro
createBtn.addEventListener("click", () => {
  const marca = inputMarca.value.trim();
  const localidad = inputLocalidad.value.trim();
  const nombre = inputNombre.value.trim();

  if (!marca || !localidad || !nombre) {
    alert("Por favor complete todos los campos");
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
        <img src="/static/assets/Icon_editar.svg" alt="Editar">
      </button>
      <button class="delete-button">
        <img src="/static/assets/Icon_eliminar.svg" alt="Eliminar">
      </button>
    `;
  } else {
    // Crear nueva fila
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
      <td>${marca}</td>
      <td>${localidad}</td>
      <td>
        ${nombre}
        <button class="edit-button">
          <img src="/static/assets/Icon_editar.svg" alt="Editar">
        </button>
        <button class="delete-button">
          <img src="/static/assets/Icon_eliminar.svg" alt="Eliminar">
        </button>
      </td>
    `;
    tableBody.appendChild(nuevaFila);
  }

  resetForm();
});

// Manejo de eventos en la tabla
tableBody.addEventListener("click", (event) => {
  const editBtn = event.target.closest(".edit-button");
  const deleteBtn = event.target.closest(".delete-button");

  if (editBtn) {
    // Modo edición
    const fila = event.target.closest("tr");
    const celdas = fila.querySelectorAll("td");
    
    inputMarca.value = celdas[0].textContent;
    inputLocalidad.value = celdas[1].textContent;
    inputNombre.value = celdas[2].childNodes[0].textContent.trim();
    
    filaEditando = fila;
    actionButtons.style.display = "flex";
    addBtn.style.display = "none";
    toggleIcons('active');

    // Cambiar ícono de edición temporalmente
    const img = editBtn.querySelector("img");
    if (img) img.src = "/static/assets/Icon_editar1.svg";

  } else if (deleteBtn) {
    // Eliminar registro
    if (confirm("¿Está seguro de eliminar este registro?")) {
      event.target.closest("tr").remove();
    } else {
      // Efecto visual al cancelar eliminación
      const img = deleteBtn.querySelector("img");
      img.src = "/static/assets/Icon_eliminar1.svg";
      setTimeout(() => {
        img.src = "/static/assets/Icon_eliminar.svg";
      }, 1000);
    }
  }
});