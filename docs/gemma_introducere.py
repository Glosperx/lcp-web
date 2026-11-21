import sys, mlx.core as mx
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler
prompt = open(sys.argv[1]).read()
model, tok = load("mlx-community/gemma-4-12B-it-qat-OptiQ-4bit", revision="63912b888c04ba2c555f198685d10b05f54cf564",
                  model_config={"model_type": "gemma4"})
text = tok.apply_chat_template([{"role": "user", "content": prompt}], add_generation_prompt=True, tokenize=False)
# chat_template.jinja closes an empty thought channel when thinking is off; the template that
# mlx-lm applies does not, so it is added here as the official template writes it.
if not text.endswith("<|channel>thought\n<channel|>"):
    text += "<|channel>thought\n<channel|>"
ids = tok.encode(text, add_special_tokens=False)
# Reopening a thought channel is also banned.
ban = [tok.convert_tokens_to_ids(t) for t in ("<|channel>", "<|think|>")]
print("prompt tokens:", len(ids), "| banned ids:", ban, "| tail:", repr(tok.decode(ids[-8:])))
def no_thought(tokens, logits):
    logits[:, ban] = -float("inf")
    return logits
mx.random.seed(0)
out = generate(model, tok, prompt=ids, max_tokens=1500, sampler=make_sampler(temp=0.7, top_p=0.95),
               logits_processors=[no_thought], verbose=False)
open(sys.argv[2], "w").write(out.strip() + "\n")
print("=== ANSWER ===")
print(out)
