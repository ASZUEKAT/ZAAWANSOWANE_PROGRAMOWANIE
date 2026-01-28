from app.settings import settings
import os
import cv2
from ultralytics import YOLO

_MODEL = None

def _get_model() -> YOLO:
    global _MODEL
    if _MODEL is None:
        _MODEL = YOLO(settings.MODEL_NAME)
    return _MODEL

def count_people(image_path: str, annotate: bool, job_id: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Nie mogę wczytać obrazu: {image_path}")

    model = _get_model()
    results = model.predict(
        source=img,
        classes=[settings.PERSON_CLASS_ID],
        conf=settings.CONF_THRESH,
        verbose=False,
    )

    r0 = results[0]
    boxes = []
    if r0.boxes is not None and r0.boxes.xyxy is not None:
        boxes = r0.boxes.xyxy.cpu().numpy().astype(int).tolist()

    count = len(boxes)
    annotated_path = None

    if annotate:
        os.makedirs(settings.ANNOTATED_DIR, exist_ok=True)
        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        annotated_path = os.path.join(settings.ANNOTATED_DIR, f"{job_id}.jpg")
        cv2.imwrite(annotated_path, img)

    return {"count": count, "annotated_path": annotated_path}
