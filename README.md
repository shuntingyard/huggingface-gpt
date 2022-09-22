# huggingface-gpt
Poor guy's access to GPT language models (GPT-2, EleutherAI's GPT-Neo and GPT-J) on-premise via REST API using consumer-grade hardware

For selection of a model and cpu/gpu alternatives please read the [configuration file](.env).

## Details
### Prerequisites
A working PyTorch installation. Test with:

```bash
python -c 'import torch; print(torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))'
```

### Installation
- create a virtual environment (`python -m venv venv`)
- in `venv/pyvenv.cfg` set `include-system-site-packages = true` in order to honor your PyTorch installation
- activate with `. venv/bin/activate`
- `pip install -r requirements.txt`

Then run
```bash
python srvrest.py
```
and (from the same machine) POST something like
```json
{
    "text": { "plain": "To be honest, neural networks" },
    "do_sample": true,
    "top_p": 100,
    "top_k": 50,
    "temperature": 0.6,
    "max_length": 128,
    "num_return_sequences": 3
}
```
or (for multiple lines with escape sequences etc)
```json
{
    "text": { "in_64": "SGVsbG8gd29ybGQhCg==" },
    "do_sample": true,
    "top_k": 10,
    "temperature": 0.05,
    "max_length": 256
}
```
to `http://localhost:49151`.

(For convenience, on a machine with `sh`, `curl` and `jq` installed

```bash
./curl_from_plain examples/text.json
```
or
```bash
./curl_from_encoded examples/b64-bash.sh
```
might be used.)

### Credits
Based on ideas from https://www.thepythoncode.com/article/text-generation-with-transformers-in-python.

### Some Figures for Comparison

Typical hardware configuration used for machine learning tasks by author:
#### Text Generation Requests on (16GB RAM) Intel NUC7i7BNH with GeForce GTX 1070 eGPU attached
| model                       | load on i7-7567U | generation on i7 | load on GTX 1070 | generation on GTX 1070 |
|:---------------------------:| ----------------:| ----------------:| ----------------:| ----------------------:|
| gpt2                        | 2s               | 7.2s             | 9s               | 1.1s                   |
| EleutherAI/gpt-neo-125M     | 2s               | 6.9s             | 10s              | 1.0s                   |
| EleutherAI/gpt-neo-1.3B     | 6s               | 71.0s            | 11s              | 5.0s                   |
| EleutherAI/gpt-neo-2.7B[^1] | 4min 15s         | 2min 8s          | -                | -                      |
| EleutherAI/gpt-j-6B         | -                | -                | -                | -                      |

[^1]: STDEV of time samples for loading the model is elevated by a factor ~6 comparing to other models.

Oldest possible hardware configuration available to author for a complementary example:
#### Text Generation Requests on (1975MB RAM) ASRock ION 3D with Atom D525 cpu
| model                   | load on Atom D525 | generation on Atom |
|:-----------------------:| -----------------:| ------------------:|
| gpt2                    | 16s               | 92.0s              |
| EleutherAI/gpt-neo-125M | 8s                | 87.2s              |

## More Links
https://towardsdatascience.com/how-you-can-use-gpt-j-9c4299dd8526
https://tracklify.com/blog/gpt-j-is-self-hosted-open-source-analog-of-gpt-3-how-to-run-in-docker/
