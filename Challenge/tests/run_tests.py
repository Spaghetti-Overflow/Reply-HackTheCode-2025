import os
import time
import subprocess
from datetime import datetime

def create_timestamped_dir(base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def run_tests(input_dir, base_output_dir):
    output_dir = create_timestamped_dir(base_output_dir)
    input_files = sorted(f for f in os.listdir(input_dir) if f.endswith(".txt"))
    
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_filename = f"output{input_file.split('-')[0]}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\nRunning test for {input_file}...")
        
        # Auto mode
        # subprocess.run(["python", "-m", "src.main", input_path, output_path])
        
        # Force default solver
        # subprocess.run(["python", "-m", "src.main", input_path, output_path, "--solver", "default"])
        
        # Force dedicated solver
        subprocess.run(["python", "-m", "src.main", input_path, output_path, "--solver", "dedicated"])
        
        print(f"\nTest completed for {input_file}. Results stored in {output_path}\n")

def main():
    input_dir = "data/input_files"
    output_base_dir = "data/output_files"
    
    run_tests(input_dir, output_base_dir)
    print("All tests completed.")

if __name__ == "__main__":
    main()
