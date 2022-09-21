import time

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, pipeline
import uvicorn

# init RESTful
app = FastAPI()

# global declarations
model_to_load = [
    "gpt2",
    "EleutherAI/gpt-neo-125M",
    "EleutherAI/gpt-neo-1.3B",
    "EleutherAI/gpt-neo-2.7B",  # too memory intensive for my GTX 1070
    "EleutherAI/gpt-j-6B",
][1]
gpt_j_generator = None
model = None


# init model
@app.on_event("startup")
def load_model():
    global gpt_j_generator, model
    start = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        model_to_load, low_cpu_mem_usage=True
    ).to("cuda")
    wall = time.time() - start
    print(f"Model loadtime wall clock: {wall / 60:1.0f}min {wall % 60:3.1f}s")

    gpt_j_generator = pipeline(
        # CUDA device n to use (-1 is cpu): device=n
        "text-generation", model=model, tokenizer=model_to_load, device=0
    )


def evaluate(args):
    start = time.time()
    sentences = gpt_j_generator(
        args.text,
        do_sample=args.do_sample,
        top_p=args.top_p,
        top_k=args.top_k,
        temperature=args.temperature,
        max_length=args.max_length,
        num_return_sequences=args.num_return_sequences,
    )
    return {
        "model": model_to_load,
        "s_elapsed": f"{time.time() - start:.2f}",
        "sentences": sentences,
    }


class Input(BaseModel):
    text: str
    do_sample: bool = True
    top_p: int = 100
    top_k: int = 50
    temperature: float = 0.7
    max_length: int = 128
    num_return_sequences: int = 1


@app.post("/generate")
async def generate(args: Input):
    return evaluate(args)


if __name__ == "__main__":
    uvicorn.run("srvrest:app", host="0.0.0.0", port=49151)
