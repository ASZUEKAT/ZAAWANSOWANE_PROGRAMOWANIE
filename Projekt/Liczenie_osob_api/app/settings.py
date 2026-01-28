from pydantic import BaseModel
import os

class Settings(BaseModel):
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
    RESULT_BACKEND: str = os.getenv("RESULT_BACKEND", "redis://redis:6379/0")
    INPUT_DIR: str = os.getenv("INPUT_DIR", "/app/data/input")
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "/app/data/uploads")
    ANNOTATED_DIR: str = os.getenv("ANNOTATED_DIR", "/app/data/annotated")
    CONF_THRESH: float = float(os.getenv("CONF_THRESH", "0.3"))
    PERSON_CLASS_ID: int = int(os.getenv("PERSON_CLASS_ID", "0"))  # COCO: person=0
    MODEL_NAME: str = os.getenv("MODEL_NAME", "yolov8n.pt")
    RESULTS_DIR: str = os.getenv("RESULTS_DIR", "/app/data/results")

settings = Settings()
