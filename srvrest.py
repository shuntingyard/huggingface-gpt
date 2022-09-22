import base64
import os
import time
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, validator
from transformers import AutoModelForCausalLM, pipeline
import uvicorn

# init RESTful, load .env
app = FastAPI()
load_dotenv()

# constants
SRVREST_CUDA_DEV = int(os.environ["SRVREST_CUDA_DEV"])
SRVREST_MODEL = int(os.environ["SRVREST_MODEL"])

# global declarations
model_to_load = [
    "gpt2",
    "EleutherAI/gpt-neo-125M",
    "EleutherAI/gpt-neo-1.3B",
    "EleutherAI/gpt-neo-2.7B",  # too memory intensive for my GTX 1070
    "EleutherAI/gpt-j-6B",
][SRVREST_MODEL]

gpt_generator = None
model = None


# init model
@app.on_event("startup")
def load_model():
    global gpt_generator, model
    start = time.time()

    model = AutoModelForCausalLM.from_pretrained(
        model_to_load, low_cpu_mem_usage=True
    ).to("cpu" if SRVREST_CUDA_DEV == -1 else "cuda")

    gpt_generator = pipeline(
        # CUDA device n to use (-1 is cpu): device=n
        "text-generation",
        model=model,
        tokenizer=model_to_load,
        device=SRVREST_CUDA_DEV,
    )

    wall = time.time() - start
    print(f"Model loadtime wall clock: {wall / 60:1.0f}min {wall % 60:3.1f}s")


def evaluate(args):
    text = (
        args.text.in_64 if isinstance(args.text, Decoded) else args.text.plain
    )

    start = time.time()
    sentences = gpt_generator(
        text,
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


class Plain(BaseModel):
    plain: str


class Decoded(BaseModel):
    in_64: str

    @validator("in_64")
    def _(cls, encoded):
        try:
            return base64.b64decode(encoded).decode()
        except Exception as e:
            raise ValueError(f"Bad b64 encoding - {e}")


class Input(BaseModel):
    """
    Partial copy from Docs » Module code » transformers.generation_utils

        def generate(...) in

        https://huggingface.co/transformers/v4.2.0/_modules/transformers/generation_utils.html

        do_sample (:obj:`bool`, `optional`, defaults to :obj:`False`):
            Whether or not to use sampling ; use greedy decoding otherwise.

        top_p (:obj:`float`, `optional`, defaults to 1.0):
            If set to float < 1, only the most probable tokens with probabili-
            ties that add up to :obj:`top_p` or higher are kept for generation.

        top_k (:obj:`int`, `optional`, defaults to 50):
            The number of highest probability vocabulary tokens to keep
            for top-k-filtering.

        temperature (:obj:`float`, `optional`, defaults tp 1.0):
            The value used to module the next token probabilities.

        max_length (:obj:`int`, `optional`, defaults to 20):
            The maximum length of the sequence to be generated.

        num_return_sequences(:obj:`int`, `optional`, defaults to 1):
            The number of independently computed returned sequences for
            each element in the batch.
    """

    text: Union[Plain, Decoded]
    do_sample: bool = False
    top_p: int = 100  # Seems to be of type int these days.
    top_k: int = 50
    temperature: float = 1.0
    max_length: int = 20
    num_return_sequences: int = 1


@app.post("/generate")
async def generate(args: Input):
    return evaluate(args)


if __name__ == "__main__":
    uvicorn.run("srvrest:app", host="0.0.0.0", port=49151)
