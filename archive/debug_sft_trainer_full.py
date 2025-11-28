from trl import SFTTrainer
import inspect

sig = inspect.signature(SFTTrainer.__init__)
for param in sig.parameters.values():
    print(param)
