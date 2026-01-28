import os
import time
from app.celery_app import celery_app
from app.detector import count_people
from app.settings import settings

@celery_app.task(bind=True, name="people_counter.count_people_task")
def count_people_task(self, image_path: str, annotate: bool, job_id: str) -> dict:
    """
    Zapisuje wynik do /app/data/results/<TASK_ID>.txt
    Po zmianie w main.py: TASK_ID == job_id zwracane przez API.
    """
    task_id = self.request.id  # ID taska Celery (u Ciebie będzie takie samo jak job_id)

    os.makedirs(settings.RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(settings.RESULTS_DIR, f"{task_id}.txt")

    t0 = time.time()
    try:
        res = count_people(image_path=image_path, annotate=annotate, job_id=job_id)
        elapsed_ms = int((time.time() - t0) * 1000)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("state=SUCCESS\n")
            f.write(f"task_id={task_id}\n")
            f.write(f"job_id={job_id}\n")
            f.write(f"count={res.get('count')}\n")
            f.write(f"annotated_path={res.get('annotated_path')}\n")
            f.write(f"image_path={image_path}\n")
            f.write(f"elapsed_ms={elapsed_ms}\n")

        return res

    except Exception as e:
        elapsed_ms = int((time.time() - t0) * 1000)
        # zapisujemy błąd do pliku, a potem rzucamy wyjątek dalej (żeby Celery miał FAILURE)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("state=FAILURE\n")
            f.write(f"task_id={task_id}\n")
            f.write(f"job_id={job_id}\n")
            f.write(f"image_path={image_path}\n")
            f.write(f"elapsed_ms={elapsed_ms}\n")
            f.write(f"error={repr(e)}\n")
        raise
