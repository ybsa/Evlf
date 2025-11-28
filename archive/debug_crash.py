from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
import torch

DATASET_FILE = "datasets/original/sft_dataset.jsonl"

print("Loading dataset...")
dataset = load_dataset("json", data_files=DATASET_FILE, split="train")
print(f"Dataset loaded. Features: {dataset.features}")
print(f"First example: {dataset[0]}")

def format_instruction(sample):
    return [f"<|im_start|>user\n{inst}<|im_end|>\n<|im_start|>assistant\n{resp}<|im_end|>" for inst, resp in zip(sample['instruction'], sample['response'])]

print("Initializing SFTConfig...")
training_args = SFTConfig(
    output_dir="./debug_results",
    dataset_text_field="text",
    max_length=128,
    packing=False,
)

class DummyConfig:
    use_cache = False
    pretraining_tp = 1
    hidden_size = 128
    vocab_size = 1000
    def to_dict(self): return {}

class DummyModel(torch.nn.Module):
    config = DummyConfig()
    def __init__(self):
        super().__init__()
        self.model = torch.nn.Linear(1, 1) # dummy
    def get_input_embeddings(self): return None
    def forward(self, *args, **kwargs): return None
    def save_pretrained(self, *args, **kwargs): pass

print("Initializing SFTTrainer...")
try:
    trainer = SFTTrainer(
        model=DummyModel(),
        train_dataset=dataset,
        args=training_args,
        formatting_func=format_instruction,
        processing_class=None 
    )
    print("SFTTrainer initialized successfully.")
except Exception as e:
    print(f"SFTTrainer init failed: {e}")
    import traceback
    traceback.print_exc()
