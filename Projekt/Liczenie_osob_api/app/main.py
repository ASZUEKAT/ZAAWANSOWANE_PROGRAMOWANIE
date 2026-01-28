from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from urllib.parse import urlparse
import os, uuid
import httpx

from app.settings import settings
from app.tasks import count_people_task
from app.celery_app import celery_app

app = FastAPI(title="People Counter API")


def _safe_join(base_dir: str, user_path: str) -> str:
    base = os.path.abspath(base_dir)
    target = os.path.abspath(os.path.join(base, user_path))
    if not target.startswith(base + os.sep):
        raise HTTPException(status_code=400, detail="Niepoprawna ścieżka (poza katalogiem bazowym).")
    return target


@app.get("/jobs/from-disk")
def enqueue_from_disk(path: str, annotate: int = 0):
    image_path = _safe_join(settings.INPUT_DIR, path)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Plik nie istnieje w data/input.")

    # To ID będzie: task_id, nazwa pliku wyniku .txt, a także (po naszej logice) job_id
    job_id = str(uuid.uuid4())

    task = count_people_task.apply_async(
        kwargs={"image_path": image_path, "annotate": bool(annotate), "job_id": job_id},
        task_id=job_id,
    )
    return {"job_id": task.id, "status_url": f"/jobs/{task.id}"}


@app.get("/jobs/from-url")
def enqueue_from_url(url: str, annotate: int = 0):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="URL musi zaczynać się od http/https.")

    job_id = str(uuid.uuid4())
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
    local_path = os.path.join(settings.UPLOADS_DIR, f"{job_id}.jpg")

    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            r = client.get(url)
            r.raise_for_status()
            if "image" not in (r.headers.get("content-type") or ""):
                raise HTTPException(status_code=400, detail="URL nie wygląda na obraz (Content-Type).")
            with open(local_path, "wb") as f:
                f.write(r.content)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nie udało się pobrać obrazu: {e}")

    task = count_people_task.apply_async(
        kwargs={"image_path": local_path, "annotate": bool(annotate), "job_id": job_id},
        task_id=job_id,
    )
    return {"job_id": task.id, "status_url": f"/jobs/{task.id}"}


@app.post("/jobs/upload")
async def enqueue_upload(file: UploadFile = File(...), annotate: int = 0):
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Wyślij plik typu image/*")

    job_id = str(uuid.uuid4())
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

    # Bezpieczniejsza nazwa pliku (gdyby filename miał dziwne znaki)
    orig_name = os.path.basename(file.filename or "upload")
    local_path = os.path.join(settings.UPLOADS_DIR, f"{job_id}_{orig_name}")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Pusty plik.")
    with open(local_path, "wb") as f:
        f.write(content)

    task = count_people_task.apply_async(
        kwargs={"image_path": local_path, "annotate": bool(annotate), "job_id": job_id},
        task_id=job_id,
    )
    return {"job_id": task.id, "status_url": f"/jobs/{task.id}"}


@app.get("/jobs/{task_id}")
def job_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    payload = {"job_id": task_id, "state": res.state}

    if res.state == "SUCCESS":
        payload["result"] = res.result
    elif res.state == "FAILURE":
        payload["error"] = str(res.result)

    return JSONResponse(payload)
