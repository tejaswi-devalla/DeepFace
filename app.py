from flask import Flask, request, render_template, jsonify
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
COMPARE_FOLDER = "compare"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["COMPARE_FOLDER"] = COMPARE_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/register", methods=["POST"])
def register():
    if "file" not in request.files:
        return (
            render_template(
                "index.html",
                recognition_message="No file",
            ),
            400,
        )

    file = request.files["file"]
    if file.filename == "":
        return (
            render_template(
                "index.html",
                recognition_message="No selected file",
            ),
            400,
        )

    if not allowed_file(file.filename):
        return (
            render_template(
                "index.html",
                recognition_message="Invalid file format",
            ),
            400,
        )

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        origin = "uploads"
        target = "static"
        tot_files = os.listdir(origin)
        for file_name in tot_files:
            shutil.copy(origin + "/" + file_name, target + "/" + file_name)
        return (
            render_template(
                "index.html",
                recognition_message="Face registered successfully",
                register_img=filename,
            ),
            200,
        )


@app.route("/recognize", methods=["POST"])
def recognize():
    if "file" not in request.files:
        return (
            render_template(
                "index.html",
                recognition_message="No file",
            ),
            400,
        )

    file = request.files["file"]
    if file.filename == "":
        return (
            render_template(
                "index.html",
                recognition_message="No selected file",
            ),
            400,
        )

    if not allowed_file(file.filename):
        return (
            render_template(
                "index.html",
                recognition_message="Invalid file format",
            ),
            400,
        )

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["COMPARE_FOLDER"], filename))
        file_path = os.path.join(app.config["COMPARE_FOLDER"], filename)
        # print(file_path)
        origin = "compare"
        target = "static"
        tot_files = os.listdir(origin)
        for file_name in tot_files:
            shutil.copy(origin + "/" + file_name, target + "/" + filename)
        reg_img = filename
        try:

            def compare_image_to_folder(image_path, folder_path):
                images_match = False
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                        image2_path = os.path.join(folder_path, filename)
                        result = DeepFace.verify(
                            img1_path=image_path, img2_path=image2_path
                        )
                        # print(result)
                        if result["verified"]:
                            images_match = True
                            registered_img = filename
                            return images_match, registered_img
                        else:
                            registered_img = filename
                            return images_match, registered_img

                if not images_match:
                    return images_match, ""

            img1_path = file_path
            folder2_path = "uploads"
            x, registered_img = compare_image_to_folder(img1_path, folder2_path)
            if x:
                recognition_message = "Face Recognized"
            else:
                recognition_message = "Face not Matched"

            return render_template(
                "index.html",
                recognition_message=recognition_message,
                register_img=registered_img,
                recognize_img=reg_img,
            )

        except Exception as e:
            recognition_message = "Error recognizing face. Face not Registered."

            return (
                render_template(
                    "index.html",
                    recognition_message=recognition_message,
                ),
                200,
            )


if __name__ == "__main__":
    app.run(debug=True)
