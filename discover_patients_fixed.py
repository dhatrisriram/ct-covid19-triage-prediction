import os
import glob
import shutil
from pathlib import Path

def discover_and_prepare_patients(source_data_dir, target_dicom_dir):
    source_path = Path(source_data_dir)
    target_path = Path(target_dicom_dir)
    
    print(f"🔍 Scanning for patients in: {source_path}")
    
    patients = []
    
    for patient_dir in source_path.iterdir():
        if patient_dir.is_dir():
            patient_id = patient_dir.name
            print(f"Found patient: {patient_id}")
            
            # Look for files in all subdirectories
            all_files = []
            for file_path in patient_dir.rglob("*"):
                if file_path.is_file():
                    all_files.append(file_path)
            
            # Filter for medical imaging files
            dicom_files = [f for f in all_files if f.suffix.lower() in ['.dcm', '.ima', '.dicom'] or f.suffix == '']
            
            if dicom_files:
                patients.append({
                    'patient_id': patient_id,
                    'study_id': 'study_1',
                    'series_id': 'series_1', 
                    'source_files': dicom_files,
                    'dicom_count': len(dicom_files)
                })
                print(f"  └── Found {len(dicom_files)} medical imaging files")
    
    print(f"\n📊 Summary: Found {len(patients)} patient series")
    
    # Create target structure and copy files
    for patient_info in patients:
        target_patient_dir = target_path / patient_info['patient_id'] / patient_info['study_id'] / patient_info['series_id']
        target_patient_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Preparing {patient_info['patient_id']}...")
        
        dicom_files = sorted(patient_info['source_files'])
        
        for i, dicom_file in enumerate(dicom_files, 1):
            new_name = target_patient_dir / f"{i:06d}.dcm"
            shutil.copy2(dicom_file, new_name)
        
        print(f"  ✅ Copied {len(dicom_files)} files")
    
    return patients

if __name__ == "__main__":
    patients = discover_and_prepare_patients(
        "/app/data/source_dicom",
        "/app/data/dicom_data"
    )
    
    import json
    with open("/app/data/patient_list.json", "w") as f:
        json.dump(patients, f, indent=2, default=str)
    
    print(f"\n🎉 Prepared {len(patients)} patients for processing")
