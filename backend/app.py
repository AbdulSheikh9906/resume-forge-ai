from flask import Flask, request, send_file, render_template
import subprocess
import os
import time

app = Flask(__name__, template_folder="../frontend")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JD_PATH = os.path.join(BASE_DIR, "JD.txt")
BAT_PATH = os.path.join(BASE_DIR, "ResumeTailor.bat")
OUTPUT_PDF = os.path.join(BASE_DIR, "output", "tailored_resume.pdf")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_resume():
    jd_text = request.form["job_description"]
    with open(JD_PATH, "w", encoding="utf-8") as f:
        f.write(jd_text)
    subprocess.call(
    ["cmd", "/c", "Resume_Tailor.bat"],
    cwd=BASE_DIR
)
    while not os.path.exists(OUTPUT_PDF):
        time.sleep(1)
    return send_file(OUTPUT_PDF, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
