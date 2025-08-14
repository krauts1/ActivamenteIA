from fastapi import APIRouter, File, UploadFile, BackgroundTasks, Depends
from app.core.deps import get_ingest_service
import uuid
jobs = {} 

router = APIRouter()

def do_ingest(job_id: str, filename: str, content: bytes, svc):
    try:
        ok, registered = svc.ingest_file(filename, content)
        jobs[job_id] = {"status": "done", "ok": ok, "registered_in_sql": registered}
    except Exception as e:
        jobs[job_id] = {"status": "error", "detail": str(e)}

@router.post("/ingest_async", status_code=202)
async def ingest_async(background: BackgroundTasks, file: UploadFile = File(...), svc = Depends(get_ingest_service)):
    jid = str(uuid.uuid4())
    jobs[jid] = {"status": "queued"}
    background.add_task(do_ingest, jid, file.filename, await file.read(), svc)
    return {"job_id": jid, "status": "queued"}

@router.get("/ingest_status/{job_id}")
def ingest_status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})
