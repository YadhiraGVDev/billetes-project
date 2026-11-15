document.addEventListener("DOMContentLoaded", function() {
    
    // ==========================================
    // 1. Lógica del Tema Oscuro/Claro
    // ==========================================
    const btnTema = document.getElementById('btn-tema');
    const txtTema = document.getElementById('txt-tema');
    const iconoTema = document.getElementById('icon-tema');
    const body = document.body;

    // Función para aplicar el tema
    function aplicarTema(tema) {
        if (tema === 'oscuro') {
            body.classList.add('dark-mode');
            if(txtTema) txtTema.innerText = 'Oscuro';
            if(iconoTema) {
                iconoTema.classList.remove('bi-moon-stars');
                iconoTema.classList.add('bi-sun');
            }
        } else {
            body.classList.remove('dark-mode');
            if(txtTema) txtTema.innerText = 'Claro';
            if(iconoTema) {
                iconoTema.classList.remove('bi-sun');
                iconoTema.classList.add('bi-moon-stars');
            }
        }
    }

    // Revisar si ya había un tema guardado al cargar la página
    const temaGuardado = localStorage.getItem('tema') || 'claro';
    aplicarTema(temaGuardado);

    // Evento al hacer clic en la fila del tema
    if (btnTema) {
        btnTema.addEventListener('click', function() {
            const temaActual = localStorage.getItem('tema') || 'claro';
            const nuevoTema = (temaActual === 'claro') ? 'oscuro' : 'claro';
            
            localStorage.setItem('tema', nuevoTema);
            aplicarTema(nuevoTema);
        });
    }

    // ==========================================
    // 2. Lógica de las Notificaciones
    // ==========================================
    const switchNoti = document.getElementById('switch-noti');
    const txtNoti = document.getElementById('txt-noti');

    // Revisar estado guardado
    if (localStorage.getItem('notificaciones') === 'desactivadas') {
        if(switchNoti) switchNoti.checked = false;
        if(txtNoti) txtNoti.innerText = 'Desactivadas';
    }

    // Evento al cambiar el interruptor
    if (switchNoti) {
        switchNoti.addEventListener('change', function() {
            if (this.checked) {
                txtNoti.innerText = 'Activadas';
                localStorage.setItem('notificaciones', 'activadas');
            } else {
                txtNoti.innerText = 'Desactivadas';
                localStorage.setItem('notificaciones', 'desactivadas');
            }
        });
    }

    // ==========================================
    // 3. Efecto para la zona de subida de imágenes
    // ==========================================
    const fileInput = document.getElementById('bill_image');
    const uploadZone = document.querySelector('.upload-zone');
    const textoAyuda = document.getElementById('texto-ayuda');

    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                textoAyuda.innerHTML = `<strong>Archivo seleccionado:</strong><br>${file.name}`;
                uploadZone.style.borderColor = "#198754";
                uploadZone.style.backgroundColor = "#e8f5e9";
            }
        });
    }
});