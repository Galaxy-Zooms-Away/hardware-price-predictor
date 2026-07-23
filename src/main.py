"""
main.py
-----------
The execution entry point. 
The rest of the functions/modules will run from here without exposing module structure.

"""
from src.app.pipeline import run_pipeline

def main():
    print("Starting Hardware Pricing Pipeline...")
    run_pipeline()
    print("Pipeline completed successfully! Processed data saved to data/processed/")

if __name__ == "__main__":
    main()