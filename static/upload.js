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
    let assigned = false;
    try {
      const dt = new DataTransfer();
      dt.items.add(files[0]);
      fileInput.files = dt.files;
      assigned = fileInput.files.length > 0 && fileInput.files[0].name === files[0].name;
    } catch (_) {}
    if (assigned) {
      showFileName(files[0].name);
    } else {
      fileNameDisplay.textContent = 'Drag-and-drop not supported — please use the file picker.';
      fileNameDisplay.classList.remove('has-file');
    }
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
