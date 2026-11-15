document.addEventListener("DOMContentLoaded", () => {
    const previewImage = document.getElementById('preview-image');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const retakeBtn = document.getElementById('retake-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const analyzeBtn = document.getElementById('analyze-btn');

    // 1. Recuperar la imagen guardada por la cámara (desde localStorage)
    const imageData = localStorage.getItem('fotoBillete');

    if (imageData) {
        previewImage.src = imageData;
        
        // Calcular un tamaño aproximado en MB (ya que es base64)
        const sizeInBytes = imageData.length * (3 / 4) - (imageData.length > 0 && imageData.endsWith('==') ? 2 : 0);
        const sizeInMB = (sizeInBytes / (1024 * 1024)).toFixed(1);
        
        fileName.textContent = 'billete_capturado.jpg';
        fileSize.textContent = `${sizeInMB} MB`;
    } else {
        // Si no hay imagen, regresamos a la cámara
        window.location.href = "/detectar/";
    }

    // 2. Botón "Cambiar imagen" (Volver a la cámara)
    retakeBtn.addEventListener('click', () => {
        window.location.href = "/detectar/";
    });

    // 3. Botón "Eliminar" (Borrar imagen y volver)
    deleteBtn.addEventListener('click', () => {
        localStorage.removeItem('fotoBillete');
        window.location.href = "/detectar/";
    });

    // 4. Botón "Analizar billete" (Enviar a Django)
    analyzeBtn.addEventListener('click', () => {
        // Cambiamos el texto del botón mientras carga
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analizando...';
        analyzeBtn.disabled = true;

        fetch('/detectar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            // Borrar la foto de la memoria local porque ya se analizó
            localStorage.removeItem('fotoBillete'); 
            
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                alert("Error al analizar.");
                analyzeBtn.innerHTML = '<i class="fa-solid fa-expand"></i> Analizar billete';
                analyzeBtn.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Hubo un error al procesar la imagen.");
            analyzeBtn.innerHTML = '<i class="fa-solid fa-expand"></i> Analizar billete';
            analyzeBtn.disabled = false;
        });
    });

    // Función para obtener el token de seguridad de Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});