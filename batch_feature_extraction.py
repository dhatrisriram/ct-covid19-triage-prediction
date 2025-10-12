import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import subprocess

def extract_features_for_patient(patient_id, study_id, series_id):
    """Extract radiomics features for a single patient"""
    
    dicom_path = f"/app/data/dicom_data/{patient_id}/{study_id}/{series_id}"
    mask_path = f"/app/data/segmentation_data/{patient_id}/{study_id}/{series_id}"
    output_path = f"/app/results/patient_features/{patient_id}_{study_id}_{series_id}"
    
    os.makedirs(output_path, exist_ok=True)
    
    # Check if segmentation masks exist
    if not os.path.exists(mask_path) or len(os.listdir(mask_path)) == 0:
        return False, "No segmentation masks found"
    
    try:
        # Run the original feature extraction script
        cmd = [
            "python", "proc_radiomic_feature.py",
            "--dicom_root", f"/app/data/dicom_data",
            "--lesion_mask_root", f"/app/data/segmentation_data", 
            "--save_root", output_path
        ]
        
        # Set environment to only process this specific patient
        env = os.environ.copy()
        env['PATIENT_FILTER'] = f"{patient_id}/{study_id}/{series_id}"
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd="/app")
        
        if result.returncode == 0:
            # Check if feature file was created
            feature_file = os.path.join(output_path, "final_merge_feature.csv")
            if os.path.exists(feature_file):
                return True, f"Features extracted to {feature_file}"
            else:
                return False, "Feature extraction completed but no output file found"
        else:
            return False, f"Feature extraction failed: {result.stderr}"
            
    except Exception as e:
        return False, f"Error running feature extraction: {str(e)}"

def batch_feature_extraction():
    """Extract features for all patients"""
    
    # Load patient list
    with open("/app/data/patient_list.json", "r") as f:
        patients = json.load(f)
    
    print(f"🧬 Extracting radiomics features for {len(patients)} patients...")
    
    results = []
    all_features = []
    
    for patient_info in tqdm(patients, desc="Extracting features"):
        patient_id = patient_info['patient_id']
        study_id = patient_info['study_id'] 
        series_id = patient_info['series_id']
        
        print(f"\n🔬 Processing {patient_id}...")
        
        success, message = extract_features_for_patient(patient_id, study_id, series_id)
        
        result = {
            'patient_id': patient_id,
            'study_id': study_id,
            'series_id': series_id,
            'success': success,
            'message': message
        }
        
        results.append(result)
        
        if success:
            print(f"  ✅ {message}")
            
            # Load the features and add patient info
            try:
                feature_file = f"/app/results/patient_features/{patient_id}_{study_id}_{series_id}/final_merge_feature.csv"
                if os.path.exists(feature_file):
                    patient_features = pd.read_csv(feature_file)
                    patient_features['patient_id'] = patient_id
                    patient_features['study_id'] = study_id
                    patient_features['series_id'] = series_id
                    all_features.append(patient_features)
            except Exception as e:
                print(f"  ⚠️ Could not load features: {e}")
        else:
            print(f"  ❌ {message}")
    
    # Combine all features into one file
    if all_features:
        combined_features = pd.concat(all_features, ignore_index=True)
        combined_features.to_csv("/app/results/all_patients_features.csv", index=False)
        print(f"\n💾 Combined features saved: {len(combined_features)} rows, {len(combined_features.columns)} columns")
    
    # Save extraction results
    with open("/app/results/feature_extraction_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\n🎉 Feature extraction complete: {successful}/{len(patients)} patients successful")
    
    return results, all_features

if __name__ == "__main__":
    os.makedirs("/app/results/patient_features", exist_ok=True)
    batch_feature_extraction()
