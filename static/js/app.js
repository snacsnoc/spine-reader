var socket = io.connect('https://' + document.domain + ':' + location.port + '/status',{  pingTimeout: 120000  });

socket.on('status_update', function(data) {
    console.log(data.message);

    let statusElement = document.getElementById("statusMessage");

    // Set the message
    statusElement.innerText = data.message;

    // Fade in and display the message
    statusElement.style.display = 'block';
    statusElement.style.opacity = 1;

    // Wait for a bit then fade out
    setTimeout(() => {
        statusElement.style.opacity = 0;

        // Hide the element after the fade out transition is complete
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 1500);

    }, 1500); // The message will display for 1.5 seconds before starting to fade out
});

socket.on('titles_update', function(data) {
    console.log(data.titles);

    // Get the ul within the .title-container div
    let ul = document.querySelector('.title-container > ul');

    // Clear existing titles (if any)
    ul.innerHTML = '';

    // Append each title as a new list item to the ul
    data.titles.forEach(title => {
        let li = document.createElement('li');
        li.textContent = title;
        ul.appendChild(li);
    });
});
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    let fileInput = document.querySelector('input[type="file"]');
    let file = fileInput.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(event) {
            let base64Image = event.target.result;
            socket.emit('upload_image', {
                'image': base64Image
            });
        };
        reader.readAsDataURL(file);
    }
});