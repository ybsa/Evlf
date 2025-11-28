import os
import time
import json
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_all_checkpoints_info(step_num):
    """Get info from all checkpoints"""
    results_dir = f"results_step{step_num}"
    if not os.path.exists(results_dir):
        return None
    
    # Find all checkpoints
    checkpoints = [d for d in os.listdir(results_dir) if d.startswith('checkpoint-')]
    if not checkpoints:
        return None
    
    # Sort checkpoints by number
    checkpoint_list = []
    for checkpoint_name in sorted(checkpoints, key=lambda x: int(x.split('-')[1])):
        checkpoint_path = os.path.join(results_dir, checkpoint_name)
        checkpoint_num = int(checkpoint_name.split('-')[1])
        
        # Try to read trainer_state.json
        state_file = os.path.join(checkpoint_path, "trainer_state.json")
        info = {
            'name': checkpoint_name,
            'number': checkpoint_num,
            'has_state': False,
            'last_log': None
        }
        
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                    info['has_state'] = True
                    if 'log_history' in data and data['log_history']:
                        # Get last entry with loss
                        for entry in reversed(data['log_history']):
                            if 'loss' in entry or 'eval_loss' in entry:
                                info['last_log'] = entry
                                break
            except:
                pass
        
        checkpoint_list.append(info)
    
    return checkpoint_list

def watch_training():
    print("🔴 LIVE TRAINING MONITOR")
    print("=" * 70)
    print("Press Ctrl+C to stop monitoring\n")
    
    while True:
        try:
            clear_screen()
            
            # Header
            print("🔴 LIVE TRAINING MONITOR")
            print("=" * 70)
            print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 70)
            
            # Read tracker to find current dataset
            with open('training_tracker.json', 'r') as f:
                tracker = json.load(f)
            
            # Find in-progress dataset
            current_dataset = None
            current_step = None
            for path, info in tracker['datasets'].items():
                if info['status'] == 'in_progress':
                    current_dataset = path.split('\\')[-1]
                    # Try to figure out step number from completed datasets
                    completed_count = sum(1 for d in tracker['datasets'].values() if d['status'] == 'completed')
                    current_step = completed_count + 1
                    break
            
            if current_dataset and current_step:
                print(f"\n📂 Dataset: {current_dataset}")
                print(f"📊 Step: {current_step}")
                
                # Get all checkpoints info
                checkpoints_info = get_all_checkpoints_info(current_step)
                
                if checkpoints_info:
                    print(f"\n💾 Total Checkpoints: {len(checkpoints_info)}")
                    print("\n" + "=" * 70)
                    print("📦 ALL CHECKPOINTS")
                    print("=" * 70)
                    print(f"{'Checkpoint':<15} {'Step':<8} {'Loss':<10} {'Epoch':<10} {'Status':<10}")
                    print("-" * 70)
                    
                    for cp in checkpoints_info:
                        if cp['last_log']:
                            step = cp['last_log'].get('step', '-')
                            loss = cp['last_log'].get('loss', cp['last_log'].get('eval_loss', '-'))
                            epoch = cp['last_log'].get('epoch', '-')
                            
                            if loss != '-':
                                loss = f"{loss:.4f}"
                            if epoch != '-':
                                epoch = f"{epoch:.2f}"
                            
                            status = "✅ Done"
                            print(f"{cp['name']:<15} {str(step):<8} {str(loss):<10} {str(epoch):<10} {status:<10}")
                        else:
                            status = "⏳ Wait"
                            print(f"{cp['name']:<15} {'-':<8} {'-':<10} {'-':<10} {status:<10}")
                else:
                    print("\n⏳ Waiting for first checkpoint...")
            else:
                print("\n✅ No training in progress or completed!")
            
            print("\n" + "=" * 70)
            print("🔄 Refreshing in 5 seconds... (Ctrl+C to stop)")
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    watch_training()
