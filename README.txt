# PRJ_493 Smart Malnutrition Detection — Streamlit Starter

## Included
- `app.py`: Streamlit app with Home, AI Screening, Report Card, Nutrition Awareness, Download Report, Model Information, About Project.
- `requirements.txt`: Python dependencies.
- `run_app.bat`: Windows helper to install dependencies and launch Streamlit.

## Important: add the model file
Place your verified model in this folder and name it exactly:
`best_malnutrition_yolov8n.pt`

Your current verified file was named `best_malnutrition_yolov8n_recovered.pt`. Copy it into this project folder and rename the COPY to `best_malnutrition_yolov8n.pt`. Keep the original ZIP as backup.

## Run on Windows
1. Install the Microsoft Visual C++ Redistributable x64 if needed: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Run:
   `& "C:\Users\Manasa C\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt`
5. Confirm the model file is in the folder.
6. Run:
   `& "C:\Users\Manasa C\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app.py`
7. Open the local URL printed in the terminal (usually http://localhost:8501).

Or double-click `run_app.bat`.

## Metrics
Precision, Recall, F1, and mAP are intentionally not fabricated. Use a real validation evaluation before reporting these values.

## Medical disclaimer
This is an academic computer-vision prototype. Predictions are not medical diagnoses. Do not use them to determine a person's nutritional status or treatment.
