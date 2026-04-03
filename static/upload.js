const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('file-name-display');
const submitBtn = document.getElementById('submit-btn');
const form = document.getElementById('upload-form');

// Click anywhere on drop zone opens the file picker
dropZone.addEventListener('click', () => fileInput.click());

// Update display when file chosen via dialog
fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    showFileName(fileInput.files[0].name);
  }
});

// Drag-and-drop
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    try {
      const dt = new DataTransfer();
      dt.items.add(files[0]);
      fileInput.files = dt.files;
    } catch (_) {
      // DataTransfer assignment not supported — file name display only
    }
    showFileName(files[0].name);
  }
});

function showFileName(name) {
  fileNameDisplay.textContent = name;
  fileNameDisplay.classList.add('has-file');
}

// Loading state on submit
form.addEventListener('submit', () => {
  submitBtn.classList.add('loading');
  submitBtn.querySelector('.btn-label').textContent = 'Analyzing...';
  submitBtn.disabled = true;
});
