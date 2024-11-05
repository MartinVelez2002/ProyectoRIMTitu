// Espera 5 segundos y luego oculta los mensajes
setTimeout(function() {
    const messages = document.querySelectorAll('.message');
    const error_messages = document.querySelectorAll('.error-message'); // Asegúrate de que la clase sea .error_message

    // Combina los dos NodeLists en un solo array
    const allMessages = [...messages, ...error_messages];

    // Recorre todos los mensajes y oculta cada uno
    allMessages.forEach(message => {
        message.style.display = 'none';      
        
    });
}, 3000);

