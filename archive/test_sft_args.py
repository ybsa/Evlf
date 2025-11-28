from trl import SFTConfig

try:
    config = SFTConfig(output_dir=".", dataset_text_field="text")
    print("dataset_text_field accepted")
except TypeError as e:
    print(f"dataset_text_field error: {e}")

try:
    config = SFTConfig(output_dir=".", max_seq_length=1024)
    print("max_seq_length accepted")
except TypeError as e:
    print(f"max_seq_length error: {e}")
