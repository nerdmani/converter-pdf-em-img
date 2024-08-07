document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'images.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Erro:', error));
});
