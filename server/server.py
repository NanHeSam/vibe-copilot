from flask import Flask, send_file, render_template_string
import os
import glob
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Path to the folder containing the images
# /Users/samhe/projects/agi_house_imagen/vibe-copilot/samples/20230812185205
IMAGES_PATH = '/Users/samhe/projects/agi_house_imagen/vibe-copilot/samples/*/*.png'  # Change this to your folder path

@app.route('/image')
def latest_image():
    # List all files ending in .png
    images = glob.glob(IMAGES_PATH)

    # images = [f for f in os.listdir(IMAGES_PATH) if f.endswith('.png')]
    # print(images)
    # Get the latest image based on creation time
    if images:
        latest_image = max(images, key=lambda f: os.path.getctime(f))
        return send_file(os.path.join(IMAGES_PATH, latest_image), mimetype='image/png')

    return "No PNG images found", 404

@app.route('/')
def html():
    return """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest Image Display</title>
    <style>
        /* Styling to set the background black and center the image */
        body {
            background-color: black;
            margin: 0;
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;     /* Center vertically */
            height: 100vh;           /* Make the body take up the full viewport height */
        }
        
        img {
            display: block; /* Remove any default spacing below the image */
        }
    </style>
    <script>
        function refreshImage() {
            // Assumes some way (e.g., server-side scripting) to get the latest image URL
            const imageUrl = "/image";  // replace with your logic or method to get the latest image
            document.getElementById("latestImage").src = imageUrl + "?timestamp=" + new Date().getTime();  // Append timestamp to prevent caching
            setTimeout(refreshImage, 100);  // Refreshes the image every 0.1 seconds
        }
    </script>
</head>

<body onload="refreshImage()">
    <img id="latestImage" src="" alt="Latest Image" width="500"> <!-- Set width as required -->
</body>

</html>

    """

if __name__ == "__main__":
    app.run(debug=True)
