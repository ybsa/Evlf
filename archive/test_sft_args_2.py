from trl import SFTConfig, SFTTrainer

# Test 1: max_length in SFTConfig
try:
    config = SFTConfig(output_dir=".", max_length=1024)
    print("max_length accepted in SFTConfig")
except TypeError as e:
    print(f"max_length error in SFTConfig: {e}")

# Test 2: max_seq_length in SFTTrainer
# We need a dummy model and dataset for this, or just check init
# But init requires model/dataset usually.
# Let's just check if we can pass it without erroring immediately on arguments.
# We can pass a dummy model (None) if we are lucky, or just catch the specific argument error.

try:
    # This might fail due to missing model, but we want to see if it fails on max_seq_length
    trainer = SFTTrainer(model=None, args=SFTConfig(output_dir="."), max_seq_length=1024)
    print("max_seq_length accepted in SFTTrainer")
except TypeError as e:
    print(f"max_seq_length error in SFTTrainer: {e}")
except Exception as e:
    # If it fails for other reasons (like missing model), it means max_seq_length might be accepted
    if "max_seq_length" not in str(e):
        print(f"max_seq_length might be accepted in SFTTrainer (failed with other error: {e})")
    else:
        print(f"max_seq_length error in SFTTrainer: {e}")
