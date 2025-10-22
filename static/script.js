const form = document.getElementById('uploadForm');
const previewImage = document.getElementById('previewImage');
const fileInput = form.querySelector('input[type="file"]');
const loading = document.getElementById('loading');

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            previewImage.src = reader.result;
        };
        reader.readAsDataURL(file);
    }
});

form.addEventListener('submit', () => {
    loading.style.display = 'block';
});
