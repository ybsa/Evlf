import os
import time
import glob
from datetime import datetime, timedelta

def monitor_training():
    """Monitor the training progress by checking logs and checkpoints."""
    
    results_dir = "./results"
    
    print("=" * 60)
    print("🔍 Evlf Training Monitor")
    print("=" * 60)
    
    # Check if training has started
    if not os.path.exists(results_dir):
        print("⚠️  Training has not started yet (no results directory)")
        return
    
    # Find checkpoint directories
    checkpoints = glob.glob(os.path.join(results_dir, "checkpoint-*"))
    checkpoints.sort(key=lambda x: int(x.split('-')[-1]))
    
    if checkpoints:
        latest_checkpoint = checkpoints[-1]
        checkpoint_num = int(latest_checkpoint.split('-')[-1])
        total_steps = 51  # From your config (17 samples * 3 epochs / batch_size=1)
        
        progress_percent = (checkpoint_num / total_steps) * 100
        
        print(f"\n📊 Training Progress:")
        print(f"   Current Step: {checkpoint_num}/{total_steps}")
        print(f"   Progress: {progress_percent:.1f}%")
        print(f"   Checkpoints saved: {len(checkpoints)}")
        print(f"   Latest checkpoint: {os.path.basename(latest_checkpoint)}")
        
        # Show progress bar
        bar_length = 40
        filled = int(bar_length * checkpoint_num / total_steps)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}] {progress_percent:.1f}%")
        
        # Check modification time to estimate if still running
        checkpoint_mtime = os.path.getmtime(latest_checkpoint)
        time_since_update = time.time() - checkpoint_mtime
        
        if time_since_update < 300:  # Less than 5 minutes
            print(f"\n✅ Status: Training in progress")
            print(f"   Last update: {int(time_since_update)} seconds ago")
        else:
            print(f"\n⚠️  Status: No recent updates")
            print(f"   Last update: {int(time_since_update/60)} minutes ago")
    else:
        print("\n📝 Training started but no checkpoints saved yet...")
        print("   (Checkpoints are saved every 25 steps)")
    
    # Check for trainer_state.json for more detailed info
    trainer_state_file = os.path.join(results_dir, "trainer_state.json")
    if os.path.exists(trainer_state_file):
        import json
        try:
            with open(trainer_state_file, 'r') as f:
                state = json.load(f)
            
            if 'log_history' in state and state['log_history']:
                latest_log = state['log_history'][-1]
                print(f"\n📉 Latest Metrics:")
                if 'loss' in latest_log:
                    print(f"   Loss: {latest_log['loss']:.4f}")
                if 'learning_rate' in latest_log:
                    print(f"   Learning Rate: {latest_log['learning_rate']:.2e}")
                if 'epoch' in latest_log:
                    print(f"   Epoch: {latest_log['epoch']:.2f}")
        except Exception as e:
            print(f"   (Could not read detailed metrics: {e})")
    
    # Check if final model exists
    final_model_dir = "./Evlf-Llama-3.1-8B-Final"
    if os.path.exists(final_model_dir):
        print(f"\n🎉 Training Complete!")
        print(f"   Final model saved to: {final_model_dir}")
    
    print("\n" + "=" * 60)
    print("Tip: Run this script again to see updated progress")
    print("=" * 60)

if __name__ == "__main__":
    try:
        monitor_training()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
