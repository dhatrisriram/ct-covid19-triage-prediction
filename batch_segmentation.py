import SimpleITK as sitk
import numpy as np
import cv2
import os
import json
from pathlib import Path
from tqdm import tqdm

def create_lung_masks_for_patient(dicom_dir, output_dir):
    """Create lung segmentation masks for a single patient"""
    try:
        # Read DICOM series
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(str(dicom_dir))
        
        if not dicom_names:
            return False, "No DICOM files found"
        
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        image_array = sitk.GetArrayFromImage(image)
        
        os.makedirs(output_dir, exist_ok=True)
        
        masks_created = 0
        
        for i, slice_data in enumerate(image_array):
            # Lung segmentation using intensity thresholding
            # CT lung tissue typically ranges from -1000 to -400 HU
            lung_mask = (slice_data > -1000) & (slice_data < -400)
            
            # Clean up mask with morphological operations
            kernel = np.ones((3,3), np.uint8)
            lung_mask = cv2.morphologyEx(lung_mask.astype(np.uint8), 
                                       cv2.MORPH_OPEN, kernel, iterations=2)
            lung_mask = cv2.morphologyEx(lung_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            
            # Only save masks that have some content
            if np.sum(lung_mask) > 1000:  # Minimum number of lung pixels
                mask_filename = f"{output_dir}/{i:03d}.png"
                cv2.imwrite(mask_filename, lung_mask * 255)
                masks_created += 1
        
        return True, f"Created {masks_created} masks"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def batch_create_segmentations():
    """Create segmentations for all patients"""
    
    # Load patient list
    with open("/app/data/patient_list.json", "r") as f:
        patients = json.load(f)
    
    print(f"🔬 Creating lung segmentations for {len(patients)} patients...")
    
    results = []
    
    for patient_info in tqdm(patients, desc="Processing patients"):
        patient_id = patient_info['patient_id']
        study_id = patient_info['study_id']
        series_id = patient_info['series_id']
        
        dicom_dir = Path(f"/app/data/dicom_data/{patient_id}/{study_id}/{series_id}")
        seg_dir = Path(f"/app/data/segmentation_data/{patient_id}/{study_id}/{series_id}")
        
        print(f"\n🫁 Processing {patient_id}...")
        
        success, message = create_lung_masks_for_patient(dicom_dir, seg_dir)
        
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
        else:
            print(f"  ❌ {message}")
    
    # Save results
    with open("/app/results/segmentation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\n🎉 Segmentation complete: {successful}/{len(patients)} patients successful")
    
    return results

if __name__ == "__main__":
    os.makedirs("/app/results", exist_ok=True)
    batch_create_segmentations()
