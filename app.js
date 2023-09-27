document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageInput");
    const uploadButton = document.getElementById("uploadButton");
    const resultDiv = document.getElementById("result");
    const plantNameElement = document.getElementById("plantName");

    uploadButton.addEventListener("click", function () {
        const file = imageInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("image", file);

            // Send the image to the backend for processing
            fetch("/identify", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.error) {
                        plantNameElement.textContent = "Error: " + data.error;
                    } else {
                        plantNameElement.textContent = "Plant Name: " + data.plantName;
                    }
                })
                .catch((error) => {
                    plantNameElement.textContent = "Error: Something went wrong.";
                    console.error(error);
                });
        } else {
            plantNameElement.textContent = "Please select an image.";
        }
    });
});