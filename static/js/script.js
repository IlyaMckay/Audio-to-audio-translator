// This function shows the processing message when the user submits the form
function showProcessing() {
    document.getElementById('processing').style.display = 'block';
    document.getElementById('form-container').style.display = 'none';
    document.getElementById('downloadLink').style.display = 'none'; // Hide the download link initially
    document.getElementById('saveMessage').style.display = 'none'; // Hide the save message initially
}

// This function shows the download link after the file is processed
function showDownloadLink(fileUrl, fileName) {
    document.getElementById('processing').style.display = 'none';
    const downloadLinkContainer = document.getElementById('downloadLink');
    const downloadButton = document.getElementById('downloadButton');
    
    downloadButton.href = fileUrl;  // Set the download URL to the button
    downloadButton.download = fileName; // Set the default download filename
    downloadLinkContainer.style.display = 'block';  // Show the download link
    document.getElementById('saveMessage').style.display = 'block'; // Show the save message
}

// This function is called after form submission to handle the response from the server
function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the form from submitting the usual way
    showProcessing(); // Show the processing message

    const formData = new FormData(event.target);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        // Extract the filename from the Content-Disposition header
        const contentDisposition = response.headers.get('Content-Disposition');
        const fileNameMatch = contentDisposition && contentDisposition.match(/filename="?([^"]+)"?/);
        const fileName = fileNameMatch ? fileNameMatch[1] : 'processed_audio.mp3';
    
        // Create a blob and URL for the file
        return response.blob().then(blob => {
            const fileUrl = URL.createObjectURL(blob);
            showDownloadLink(fileUrl, fileName);
        });
    })
    .catch(error => {
        alert('An error occurred during file processing');
        console.error(error);
    });
}
    