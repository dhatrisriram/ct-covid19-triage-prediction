import os
import json
import time
from datetime import datetime

def run_batch_analysis():
    start_time = time.time()
    print(f"🚀 Starting batch COVID-19 analysis at {datetime.now()}")
    print("=" * 60)
    
    # Step 1: Use the FIXED discovery script that found 61 patients
    print("\n📋 STEP 1: Discovering patients...")
    os.system("python /app/batch_scripts/discover_patients_fixed.py")
    
    # Check if patients were found
    if not os.path.exists("/app/data/patient_list.json"):
        print("❌ No patient list found! Stopping.")
        return
    
    with open("/app/data/patient_list.json", "r") as f:
        patients = json.load(f)
    
    print(f"✅ Found {len(patients)} patients for processing")
    
    # Step 2: Create segmentations  
    print("\n🫁 STEP 2: Creating lung segmentations...")
    os.system("python /app/batch_scripts/batch_segmentation.py")
    
    # Step 3: Extract features using original repository
    print("\n🧬 STEP 3: Extracting radiomics features...")
    os.system("python proc_radiomic_feature.py --dicom_root /app/data/dicom_data --lesion_mask_root /app/data/segmentation_data --save_root /app/results")
    
    # Step 4: Run predictions
    print("\n🎯 STEP 4: Running COVID-19 predictions...")
    if os.path.exists("/app/results/final_merge_feature.csv"):
        os.system("python COVID-19_prediction.py --radiomics_data /app/results/final_merge_feature.csv")
    else:
        print("❌ No features file found, skipping predictions")
    
    # Generate summary
    end_time = time.time()
    runtime_minutes = (end_time - start_time) / 60
    
    print(f"\n🎉 Analysis complete! Runtime: {runtime_minutes:.1f} minutes")
    print(f"📊 Processed {len(patients)} patients")
    print("📁 Results saved in: /app/results/")

if __name__ == "__main__":
    run_batch_analysis()
