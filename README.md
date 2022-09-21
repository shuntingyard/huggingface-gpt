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

#### Generation Requests on Intel NUC7i7BNH
| model                     | load i7-7567U | generation i7 | load GeForce GTX 1070 | generation GTX 1070 |
|:-------------------------:| -------------:| -------------:| ---------------------:| -------------------:|
| gpt2                      | 2.05          | 7.22          | 9.05                  | 1.13                |
| EleutherAI/gpt-neo-125M   | 1.7           | 6.86          | 9.75                  | 0.97                |
| EleutherAI/gpt-neo-1.3B   | 19.6 1)       | 71.05         | 11.7                  | 5.03                |
| EleutherAI/gpt-neo-2.7B   | 258.5         | 128.6         | -                     | -                   |
| EleutherAI/gpt-j-6B       | -             | -             | -                     | -                   |

1) STDEV was at 28

#### Generation Requests on Intel NUC7i7BNH - Alt !!!
| startup   | i7-7567U  | GeForce GTX 1070  | request       | gpustart |
| ---------:| ---------:| -----------------:| ------------- | - |
| 2.3 1.8   | 6.89 7.55 | 1.12 1.13         | text.json     | 9.1 9.0
| 1.7 1.7   | 6.91 6.81 | 0.86 1.04 1.03    | text.json     | 9.6 9.9
| 5.? 5.5   | 71.6 70.5 | 6.74 6.29 4.04 4. | text.json     | 11.9 11.5 11.6
| 256.3 -1. | 128.56+.1 | -                 | text.json     |
| -         | -         | -                 | -             |

## More Links
https://towardsdatascience.com/how-you-can-use-gpt-j-9c4299dd8526
https://tracklify.com/blog/gpt-j-is-self-hosted-open-source-analog-of-gpt-3-how-to-run-in-docker/
