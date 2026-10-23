from pathlib import Path
from datetime import datetime
from io import BytesIO
import json
import streamlit as st
from PIL import Image
from ultralytics import YOLO
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "best_malnutrition_yolov8n.pt"
KNOWLEDGE_PATH = APP_DIR / "PRJ493_RAG_Knowledge_Chunks.jsonl"
OUTPUT_DIR = APP_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="PRJ_493 | Smart Malnutrition Detection",
    page_icon="🥗",
    layout="wide",
)

DISCLAIMER = (
    "This application is an academic computer-vision prototype. Its output is not "
    "a medical diagnosis and must not be used to determine a person's nutritional "
    "status or treatment. Consult a qualified healthcare professional for concerns."
)

@st.cache_resource
def load_model(model_path: str):
    return YOLO(model_path)

def get_model():
    if not MODEL_PATH.exists():
        st.error(
            f"Model file not found: {MODEL_PATH.name}. Place the trained checkpoint "
            "in the same folder as app.py and name it exactly "
            "'best_malnutrition_yolov8n.pt'."
        )
        st.stop()
    try:
        return load_model(str(MODEL_PATH))
    except Exception as exc:
        st.error(f"The model could not be loaded: {exc}")
        st.info("Check that this is a valid Ultralytics YOLO checkpoint and that dependencies installed correctly.")
        st.stop()



def load_knowledge_base():
    """Load the prepared RAG knowledge chunks from JSONL."""
    if not KNOWLEDGE_PATH.is_file():
        raise FileNotFoundError(
            f"Knowledge file not found: {KNOWLEDGE_PATH}"
        )

    chunks = []

    with KNOWLEDGE_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            if "id" in chunk and "text" in chunk:
                chunks.append(chunk)

    return chunks


def retrieve_nutrition_knowledge(prediction):
    """
    Retrieve knowledge sections matching the displayed YOLO class.
    Always include the general safety section.
    """
    label = str(prediction).strip().casefold()

    if label == "healthy":
        target_ids = [
            "HEALTHY_001",
            "HEALTHY_002",
            "HEALTHY_003",
        ]
    elif label == "malnourished":
        target_ids = [
            "MALNUTRITION_001",
            "MALNUTRITION_002",
            "MALNUTRITION_003",
        ]
    else:
        target_ids = ["NO_DETECTION_001"]

    target_ids = ["GENERAL_001"] + target_ids

    chunks = load_knowledge_base()
    chunks_by_id = {chunk["id"]: chunk for chunk in chunks}

    retrieved = [
        chunks_by_id[chunk_id]
        for chunk_id in target_ids
        if chunk_id in chunks_by_id
    ]

    if not retrieved:
        return []

    return retrieved


def retrieve_references():
    """Retrieve the knowledge base's reference section."""
    chunks = load_knowledge_base()

    return next(
        (
            chunk for chunk in chunks
            if chunk.get("id") == "SOURCE_001"
        ),
        None,
    )


def predict_image(image: Image.Image, conf: float):
    model = get_model()
    results = model.predict(source=image, conf=conf, verbose=False)
    result = results[0]
    annotated = result.plot()  # BGR numpy array
    annotated_rgb = Image.fromarray(annotated[:, :, ::-1].copy())
    boxes = result.boxes
    detections = []
    if boxes is not None and len(boxes) > 0:
        names = result.names
        for box in boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            xyxy = [round(float(v), 1) for v in box.xyxy[0].tolist()]
            detections.append({
                "class": names.get(class_id, str(class_id)),
                "confidence": confidence,
                "xyxy": xyxy,
            })
        detections.sort(key=lambda item: item["confidence"], reverse=True)
    return annotated_rgb, detections

def make_pdf(report: dict) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 55
    pdf.setTitle("PRJ_493 Screening Report")
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(48, y, "PRJ_493 Smart Malnutrition Detection")
    y -= 28
    pdf.setFont("Helvetica", 11)
    pdf.drawString(48, y, f"Report date/time: {report['date']}")
    y -= 22
    pdf.drawString(48, y, f"Prediction: {report['prediction']}")
    y -= 20
    pdf.drawString(48, y, f"Confidence: {report['confidence']}")
    y -= 30
    if report.get("image_bytes"):
        try:
            img = Image.open(BytesIO(report["image_bytes"])).convert("RGB")
            img.thumbnail((480, 320))
            image_buffer = BytesIO()
            img.save(image_buffer, format="JPEG", quality=90)
            image_buffer.seek(0)
            draw_h = min(300, img.height)
            draw_w = min(480, img.width)
            pdf.drawImage(ImageReader(image_buffer), 48, y - draw_h, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
            y -= draw_h + 24
        except Exception:
            pass
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(48, y, "Disclaimer")
    y -= 17
    pdf.setFont("Helvetica", 9)
    text = pdf.beginText(48, y)
    text.setLeading(13)
    for line in [
        "This is an academic computer-vision prototype, not a medical diagnosis.",
        "Do not use this result to determine nutritional status or treatment.",
        "For health concerns, consult a qualified healthcare professional."
    ]:
        text.textLine(line)
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()

def sidebar():
    st.sidebar.title("🥗 PRJ_493")
    st.sidebar.caption("Smart Malnutrition Detection System")
    return st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "AI Screening",
            "Report Card",
            "Nutrition Awareness",
            "Download Report",
            "About Project",
        ],
    )

if "screening" not in st.session_state:
    st.session_state.screening = None

page = sidebar()

if page == "Home":
    st.title("Smart Malnutrition Detection System")
    st.subheader("PRJ_493 | Machine Learning + Computer Vision | SDG 2")
    st.write(
        "This academic prototype uses a YOLOv8 object-detection model to analyse "
        "an uploaded image and display its predicted class, confidence, and bounding boxes."
    )
    st.warning(DISCLAIMER)
    if st.button("Start Screening", type="primary"):
        st.session_state.go_screening = True
        st.rerun()
    if st.session_state.get("go_screening"):
        st.info("Choose **AI Screening** from the navigation menu to upload an image.")

elif page == "AI Screening":
    st.title("AI Screening")
    st.write("Upload an image file to run the trained YOLO model.")
    uploaded = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
    confidence_threshold = st.slider("Minimum detection confidence", 0.05, 0.95, 0.25, 0.05)
    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded image", use_container_width=True)
            if st.button("Run AI Screening", type="primary"):
                with st.spinner("Running model prediction..."):
                    annotated, detections = predict_image(image, confidence_threshold)
                image_bytes = BytesIO()
                annotated.save(image_bytes, format="PNG")
                original_bytes = BytesIO()
                image.save(original_bytes, format="PNG")
                now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
                if detections:
                    top = detections[0]
                    prediction = top["class"]
                    confidence_text = f"{top['confidence'] * 100:.2f}%"
                else:
                    prediction = "No objects detected"
                    confidence_text = "N/A"
                st.session_state.screening = {
                    "date": now,
                    "prediction": prediction,
                    "confidence": confidence_text,
                    "detections": detections,
                    "annotated_bytes": image_bytes.getvalue(),
                    "original_bytes": original_bytes.getvalue(),
                }
                st.success("Prediction completed.")
        except Exception as exc:
            st.error(f"Could not process this image: {exc}")

    report = st.session_state.screening
    if report:
        st.divider()
        st.subheader("Latest prediction")
        c1, c2 = st.columns(2)
        c1.metric("Prediction", report["prediction"])
        c2.metric("Confidence", report["confidence"])
        st.image(report["annotated_bytes"], caption="Prediction with bounding boxes", use_container_width=True)
        if report["detections"]:
            st.write("Detected objects")
            st.dataframe(
                [
                    {
                        "Class": d["class"],
                        "Confidence": f"{d['confidence'] * 100:.2f}%"
                    }
                    for d in report["detections"]
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No detections exceeded the selected confidence threshold.")
        st.caption(DISCLAIMER)

elif page == "Report Card":
    st.title("Report Card")
    report = st.session_state.screening
    if not report:
        st.info("No screening report is available yet. Go to AI Screening and upload an image first.")
    else:
        st.subheader("Screening summary")
        st.write(f"**Prediction:** {report['prediction']}")
        st.write(f"**Confidence:** {report['confidence']}")
        st.write(f"**Date:** {report['date']}")
        st.image(report["annotated_bytes"], caption="Annotated screening image", use_container_width=True)
        st.warning(DISCLAIMER)



elif page == "Nutrition Awareness":
    st.title("Nutrition Awareness")

    report = st.session_state.screening

    if not report:
        st.info("Please complete AI Screening first.")

    else:
        prediction = report.get("prediction", "").strip().casefold()

        if prediction == "healthy":
            st.subheader("🥗 Healthy Nutrition Awareness")

            st.write(
                "Maintain a balanced diet and continue healthy eating habits."
            )

            st.markdown("### Balanced meals")
            st.write(
                "Include rice, wheat, millets or other grains along with "
                "dal, vegetables, fruits, and suitable protein sources."
            )

            st.markdown("### Protein-rich foods")
            st.write(
                "Include dal, beans, chickpeas, lentils, soy foods, milk, "
                "curd, eggs, fish, or lean meat according to your preferences."
            )

            st.markdown("### Fruits and vegetables")
            st.write(
                "Eat a variety of seasonal fruits and vegetables to obtain "
                "different vitamins, minerals, and fibre."
            )

            st.markdown("### Hydration")
            st.write(
                "Drink safe water regularly. Fluid needs vary according "
                "to age, activity, climate, and health."
            )

            st.markdown("### Maintain healthy habits")
            st.write(
                "Eat regularly, choose a variety of foods, maintain food "
                "hygiene, and follow healthy habits suited to your needs."
            )

        elif prediction == "malnourished":
            st.subheader("🍎 Nutrition Awareness and Support")

            st.write(
                "A varied and nutritious diet can support overall health. "
                "If you are concerned about nutrition, seek guidance from "
                "a qualified healthcare professional or registered dietitian."
            )

            st.markdown("### Energy-providing foods")
            st.write(
                "Rice, wheat, millets, potatoes, and other staple foods "
                "can provide energy as part of a balanced diet."
            )

            st.markdown("### Protein-rich foods")
            st.write(
                "Dal, beans, chickpeas, lentils, soy foods, milk, curd, "
                "eggs, fish, and meat where suitable provide protein."
            )

            st.markdown("### Include a variety of foods")
            st.write(
                "Where available and suitable, include vegetables, fruits, "
                "protein sources, staple foods, and sources of healthy fats "
                "such as nuts and seeds."
            )

            st.markdown("### Regular meals and support")
            st.write(
                "Suitable meal frequency and portions depend on age, health, "
                "and individual needs. A healthcare professional can help "
                "identify appropriate nutritional support."
            )

            st.markdown("### When to seek help")
            st.write(
                "Consult a healthcare professional if you have concerns "
                "about unexplained weight loss, persistent poor appetite, "
                "weakness, feeding difficulties, or a child's growth."
            )

        else:
            st.subheader("General Nutrition Awareness")

            st.write(
                "Choose a variety of foods, including staple foods, protein "
                "sources, fruits, and vegetables. Drink safe water regularly "
                "and consult a healthcare professional if you have nutrition "
                "concerns."
            )

    st.caption(
        "General nutrition education only. Food choices and nutritional "
        "needs vary from person to person."
    )

    
elif page == "Download Report":
    st.title("Download Report")
    report = st.session_state.screening
    if not report:
        st.info("Complete an AI Screening first to generate a report.")
    else:
        st.write(f"**Prediction:** {report['prediction']}")
        st.write(f"**Confidence:** {report['confidence']}")
        st.write(f"**Date:** {report['date']}")
        pdf_bytes = make_pdf({
            "date": report["date"],
            "prediction": report["prediction"],
            "confidence": report["confidence"],
            "image_bytes": report["annotated_bytes"],
        })
        st.download_button(
            "Download screening report (PDF)",
            data=pdf_bytes,
            file_name="PRJ493_screening_report.pdf",
            mime="application/pdf",
            type="primary",
        )
        st.caption(DISCLAIMER)
   

elif page == "About Project":
    st.title("About Project")

    st.header("PRJ_493 — Smart Malnutrition Detection System")

    st.write(
        "The Smart Malnutrition Detection System is an academic project "
        "that explores the use of Machine Learning and Computer Vision "
        "to analyse uploaded images using a YOLOv8 object-detection model. "
        "The application provides a simple web interface for displaying "
        "model predictions and related nutrition awareness information."
    )

    st.divider()

    st.subheader("Problem Statement")

    st.write(
        "Nutrition-related concerns are important for individual and "
        "community well-being. This project explores an image-based "
        "computer-vision approach to classifying images into the model's "
        "trained categories: Healthy and Malnourished. The prototype "
        "demonstrates how an AI model can be integrated with a web "
        "application to present predictions and educational information."
    )

    st.subheader("Project Objectives")

    st.markdown("""
    - Develop a web application using Streamlit.
    - Integrate a trained YOLOv8 object-detection model.
    - Allow users to upload images for model inference.
    - Display predicted classes, confidence scores, and bounding boxes.
    - Generate a screening report containing the prediction and image.
    - Retrieve relevant nutrition awareness content based on the displayed prediction.
    - Provide general nutrition education through a dedicated page.
    """)

    st.subheader("Technologies Used")

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:
        st.markdown("**Machine Learning**")
        st.write("YOLOv8 object-detection model")
        st.markdown("**Programming Language**")
        st.write("Python")

    with tech_col2:
        st.markdown("**Web Framework**")
        st.write("Streamlit")
        st.markdown("**Image Processing and Reporting**")
        st.write("Pillow, Ultralytics, ReportLab")

    st.subheader("System Workflow")

    st.markdown("""
    1. **Image Upload:** The user uploads an image through the AI Screening page.
    2. **Model Inference:** The trained YOLOv8 model processes the image.
    3. **Prediction Display:** The application presents the detected class,
       confidence score, and annotated image when detections are available.
    4. **Nutrition Awareness:** Relevant educational information is displayed
       according to the latest supported prediction.
    5. **Report Generation:** The user can view the screening summary and
       download a PDF report.
    """)

    st.subheader("Key Features")

    st.markdown("""
    - Simple and user-friendly Streamlit interface.
    - Image-based AI screening demonstration.
    - Detection visualisation with bounding boxes.
    - Screening summary and downloadable PDF report.
    - Nutrition awareness information for the two supported classes.
    - Model information and project documentation.
    """)

    st.subheader("Applications")

    st.write(
        "The prototype can be used for academic demonstrations, learning "
        "about computer vision, exploring object-detection workflows, "
        "and demonstrating how AI predictions can be connected to an "
        "educational information retrieval system."
    )

    st.subheader("Sustainable Development Goal")

    st.markdown("**SDG 2 — Zero Hunger**")

    st.write(
        "The project is related to SDG 2, which focuses on ending hunger, "
        "improving food security and nutrition, and promoting sustainable "
        "agriculture. Its educational focus highlights the importance of "
        "nutrition awareness."
    )

    st.subheader("Future Enhancements")

    st.markdown("""
    - Evaluate the model using a properly prepared validation dataset.
    - Improve model performance through additional training and testing.
    - Expand the nutrition knowledge base with reviewed educational sources.
    - Enhance document retrieval to find more relevant nutrition information.
    - Improve accessibility and the overall user interface.
    - Explore deployment for controlled academic demonstrations.
    """)

    st.subheader("Limitations and Disclaimer")

    st.warning(
        "This application is an academic computer-vision prototype, "
        "not a medical diagnostic system. Image predictions may be "
        "incorrect and cannot establish a person's nutritional status. "
        "Do not use the output to determine treatment or make medical "
        "decisions. Consult a qualified healthcare professional for "
        "nutrition concerns."
    )

    st.caption(
        "PRJ_493 | Smart Malnutrition Detection System | "
        "Machine Learning + Computer Vision | SDG 2"
    )
