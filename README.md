# huggingface-gpt
Poor guy's access to on-premise GPT language models (GPT-2, GPT-Neo, GPT-J) via REST API on consumer-grade hardware

## Details
### Prerequisites
A working PyTorch installation. Test with:

`python -c 'import torch; print(torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))'`.

### Installation
- create a virtual environment (`python -m venv venv`)
- in `venv/pyvenv.cfg` set `include-system-site-packages = true` to honor your PyTorch installation
- activate with `. venv/bin/activate`
- `pip install -r requirements.txt`.

Then run `python srvrest.py` and (from the same machine) `HTTP POST` something like
<pre>
{
    "text": "To be honest, neural networks",
    "do_sample": true,
    "top_k": 50,
    "temperature": 0.6,
    "max_len": 128,
    "num_return_sequences": 3
}
</pre>
to `http://localhost:49151`.

(For convenience, on a machine with `sh`, `curl` and `jq` installed `./curljq.sh examples/text.json` might be used.)

### Credits
Based on ideas from https://www.thepythoncode.com/article/text-generation-with-transformers-in-python.

### Details (TBD)
A few figures to compare

#### Generation Requests Intel NUC7i7BNH
| cpu       | gpu               | model                     | request       |
| i7-7567U  | GeForce GTX 1070  |                           |               |
| ---------:| -----------------:|:-------------------------:| ------------- |
| 7.4s      | 0.86s             | EleutherAI/gpt-neo-125M   | text.json     |

## More Links
https://towardsdatascience.com/how-you-can-use-gpt-j-9c4299dd8526
https://tracklify.com/blog/gpt-j-is-self-hosted-open-source-analog-of-gpt-3-how-to-run-in-docker/
