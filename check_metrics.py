import json
import os
import glob

def get_metrics():
    print(f"{'Step':<15} {'Epochs':<10} {'Final Loss':<10}")
    print("-" * 35)
    
    # Check results_step* folders
    folders = glob.glob("results_step*")
    folders.sort(key=lambda x: int(x.replace("results_step", "")) if x.replace("results_step", "").isdigit() else 0)
    
    for folder in folders:
        # Find the latest checkpoint folder
        checkpoints = glob.glob(os.path.join(folder, "checkpoint-*"))
        if not checkpoints:
            continue
            
        # Sort by step number
        checkpoints.sort(key=lambda x: int(x.split("-")[-1]))
        latest_checkpoint = checkpoints[-1]
        
        state_file = os.path.join(latest_checkpoint, "trainer_state.json")
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                    
                if 'log_history' in data and data['log_history']:
                    # Find last entry with loss
                    last_log = None
                    for log in reversed(data['log_history']):
                        if 'loss' in log:
                            last_log = log
                            break
                    
                    if last_log:
                        epoch = last_log.get('epoch', 'N/A')
                        loss = last_log.get('loss', 'N/A')
                        print(f"{folder:<15} {epoch:<10} {loss:<10}")
            except Exception as e:
                print(f"{folder:<15} Error reading state")

if __name__ == "__main__":
    get_metrics()
