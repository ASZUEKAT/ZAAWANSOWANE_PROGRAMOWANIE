import asyncio
import glob
import os
import time
import httpx

API = os.getenv("API", "http://localhost:8000")
FOLDER = os.getenv("FOLDER", "data/input")
RESULTS_DIR = os.getenv("RESULTS_DIR", "data/results")
JOB_IDS_PATH = os.getenv("JOB_IDS_PATH", "job_ids.txt")

N = int(os.getenv("N", "1000"))
ANNOTATE = int(os.getenv("ANNOTATE", "0"))  # 0 dla 1000, 1 tylko do małego demo

ENQUEUE_CONCURRENCY = int(os.getenv("ENQUEUE_CONCURRENCY", "100"))
WATCH_INTERVAL_SEC = float(os.getenv("WATCH_INTERVAL_SEC", "0.5"))

# MODE:
#   run     = enqueue + watch
#   enqueue = tylko enqueue (zapisze job_ids.txt)
#   watch   = tylko watch (czyta job_ids.txt i czeka na .txt w data/results)
MODE = os.getenv("MODE", "run").lower()

PRINT_EACH = os.getenv("PRINT_EACH", "1") == "1"   # drukuj każdy wynik
PROGRESS_EVERY = int(os.getenv("PROGRESS_EVERY", "50"))  # co ile wypisać progress


def parse_kv_file(path: str) -> dict:
    out = {}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def load_job_map(path: str) -> dict[str, str]:
    """job_id -> filename"""
    job_map = {}
    if not os.path.exists(path):
        return job_map
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                filename, job_id = parts
                job_map[job_id] = filename
    return job_map


async def enqueue_jobs(client: httpx.AsyncClient, filenames: list[str]) -> dict[str, str]:
    # wyczyść job_ids.txt na start (żeby wznowienia robić MODE=watch)
    with open(JOB_IDS_PATH, "w", encoding="utf-8") as f:
        f.write("")

    lock = asyncio.Lock()
    job_map: dict[str, str] = {}
    sem = asyncio.Semaphore(ENQUEUE_CONCURRENCY)

    async def enqueue_one(filename: str):
        async with sem:
            params = {"path": filename, "annotate": ANNOTATE}
            r = await client.get(f"{API}/jobs/from-disk", params=params)
            r.raise_for_status()
            job_id = r.json()["job_id"]
            return job_id, filename

    async def persist(filename: str, job_id: str):
        async with lock:
            with open(JOB_IDS_PATH, "a", encoding="utf-8") as f:
                f.write(f"{filename}\t{job_id}\n")

    tasks: set[asyncio.Task] = set()
    queued = 0

    try:
        for fn in filenames:
            tasks.add(asyncio.create_task(enqueue_one(fn)))

            # żeby nie tworzyć 1000 tasków naraz w pętli
            if len(tasks) >= ENQUEUE_CONCURRENCY * 2:
                done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for t in done:
                    job_id, filename = t.result()
                    job_map[job_id] = filename
                    await persist(filename, job_id)
                    queued += 1
                    if queued % 50 == 0:
                        print(f"Queued so far: {queued}/{len(filenames)}")

        # dokończ resztę
        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                job_id, filename = t.result()
                job_map[job_id] = filename
                await persist(filename, job_id)
                queued += 1
                if queued % 50 == 0:
                    print(f"Queued so far: {queued}/{len(filenames)}")

    except KeyboardInterrupt:
        print("\n[CTRL+C] Przerwano enqueue. Przechodzę do watch dla już zakolejkowanych.")
        # anuluj pozostałe requesty
        for t in tasks:
            t.cancel()

    print(f"Queued: {len(job_map)}  (zapisane w {JOB_IDS_PATH})")
    return job_map


def watch_results(job_map: dict[str, str]):
    pending = set(job_map.keys())
    success = 0
    failure = 0
    done = 0

    print(f"Watching {len(pending)} jobów. Wyniki: {RESULTS_DIR}/<job_id>.txt")
    try:
        while pending:
            finished_now = []

            for job_id in list(pending):
                result_path = os.path.join(RESULTS_DIR, f"{job_id}.txt")
                if not os.path.exists(result_path):
                    continue

                # plik może się jeszcze dopisywać — jak parse się wywali, spróbujemy w kolejnej iteracji
                try:
                    data = parse_kv_file(result_path)
                except Exception:
                    continue

                state = data.get("state")
                if state not in ("SUCCESS", "FAILURE"):
                    continue

                filename = job_map.get(job_id, "?")

                if state == "SUCCESS":
                    cnt = data.get("count")
                    ann = data.get("annotated_path")
                    if PRINT_EACH:
                        print(f"[SUCCESS] {filename} -> count={cnt} (job_id={job_id})")
                        if ann and ann != "None":
                            # tylko informacyjnie (w kontenerze to /app/data/..., na hoście masz data/annotated/)
                            print(f"         annotated_path={ann}")
                    success += 1
                else:
                    err = data.get("error")
                    if PRINT_EACH:
                        print(f"[FAILURE] {filename} -> error={err} (job_id={job_id})")
                    failure += 1

                finished_now.append(job_id)
                done += 1

                if done % PROGRESS_EVERY == 0:
                    print(f"Progress: done={done}/{len(job_map)} pending={len(pending)-len(finished_now)}")

            for jid in finished_now:
                pending.discard(jid)

            time.sleep(WATCH_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n[CTRL+C] Przerwano watch. Możesz wznowić: MODE=watch")

    print("\n=== SUMMARY ===")
    print(f"Total tracked: {len(job_map)}")
    print(f"Success: {success}")
    print(f"Failure: {failure}")
    print(f"Pending: {len(pending)}")


async def main():
    files = glob.glob(os.path.join(FOLDER, "*"))
    if not files:
        raise SystemExit("Brak plików w data/input")

    files = (files * (N // len(files) + 1))[:N]
    filenames = [os.path.basename(f) for f in files]

    if MODE == "watch":
        job_map = load_job_map(JOB_IDS_PATH)
        if not job_map:
            raise SystemExit(f"Brak jobów w {JOB_IDS_PATH}. Najpierw zrób MODE=enqueue.")
        watch_results(job_map)
        return

    async with httpx.AsyncClient(timeout=60.0) as client:
        job_map = await enqueue_jobs(client, filenames)

    if MODE == "enqueue":
        return

    if job_map:
        watch_results(job_map)


if __name__ == "__main__":
    asyncio.run(main())
