from celery import signals
from celery.result import AsyncResult
from fastapi import APIRouter

from farm_api.web.api.textgen.utils import generate_output
from services.celery import make_celery

from .models import ChatItem, ModelLoader

router = APIRouter()

# Set up celery + models
celery = make_celery()
model_loader = None
model_path = "meta-llama/Llama-2-7b-chat-hf"


@router.post("/generate")
def chat(item: ChatItem) -> dict[str, str]:
    """
    Generates text from a given prompt.

    Uses the llama v2 model.
    """
    task = generate_text_task.delay(item.prompt)
    return {"task_id": task.id}


@router.get("/task/{task_id}")
async def get_task(task_id: str) -> dict[str, str]:
    result = AsyncResult(task_id)
    if result.ready():
        res = result.get()
        return {
            "result": res[0],
            "time": res[1],
            "memory": res[2],
        }
    else:
        return {"status": "Task not completed yet"}


@signals.worker_process_init.connect
def setup_model() -> None:
    global model_loader
    model_loader = ModelLoader(model_path)


@celery.task
def generate_text_task(prompt: str) -> str:
    time, memory, outputs = generate_output(
        prompt,
        model_loader.model,
        model_loader.tokenizer,
    )
    return model_loader.tokenizer.decode(outputs[0]), time, memory
