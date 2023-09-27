import os
from flask import Flask, request, jsonify, render_template
from PIL import Image
import tensorflow as tf

app = Flask(_name_)

# Load your trained model and labels here
model = tf.keras.models.load_model("data/trained_model/model.h5")
with open("data/trained_model/labels.json", "r") as labels_file:
    labels = json.load(labels_file)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/identify", methods=["POST"])
def identify_plant():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"})

        image = request.files["image"]

        # Ensure the file is an image
        if not image.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            return jsonify({"error": "Invalid image format"})

        # Process the image using your trained model to get the plant name
        img = Image.open(image)
        img = img.resize((224, 224))  # Resize the image to match the input size expected by your model
        img = np.asarray(img)  # Convert the image to a NumPy array
        img = img / 255.0  # Normalize the image (if necessary)

        # Make predictions using your model (replace this with your actual prediction code)
        predictions = model.predict(np.expand_dims(img, axis=0))

        # Get the predicted class label
        predicted_class_index = np.argmax(predictions)
        predicted_class = labels[predicted_class_index]

        return jsonify({"plantName": predicted_class})

    except Exception as e:
        return jsonify({"error": str(e)})

if _name_ == "_main_":
    app.run(debug=True)