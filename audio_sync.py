"""
Audio synchronization module using cross-correlation analysis.
"""
import os
from typing import Dict
import librosa
import numpy as np
from scipy.signal import correlate


class AudioSyncProcessor:
    """Handles audio file synchronization using cross-correlation."""
    
    def __init__(self):
        self.supported_formats = {'.wav', '.mp3', '.mp4', '.flac', '.m4a', '.aac'}
    
    def validate_file(self, file_path: str) -> bool:
        """Validate if file exists and has supported format."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {ext}. Supported: {', '.join(self.supported_formats)}")
        
        return True
    
    def sync_files(self, reference_file: str, target_file: str) -> Dict:
        """
        Synchronize two audio files using cross-correlation.
        
        Args:
            reference_file: Path to reference audio file
            target_file: Path to audio file to be synchronized

        Returns:
            Dict containing sync results
        """
        # Validate input files
        self.validate_file(reference_file)
        self.validate_file(target_file)
        
        try:
            # Load audio files
            y1, sr1 = librosa.load(reference_file)
            y2, sr2 = librosa.load(target_file)

            # Resample if sample rates differ
            if sr1 != sr2:
                y2 = librosa.resample(y2, orig_sr=sr2, target_sr=sr1)

            # Cross-correlate to find offset
            correlation = correlate(y1, y2, mode='full')
            offset = np.argmax(correlation) - len(y2) + 1
            offset_seconds = offset / sr1

            return {
                'success': True,
                'offset_seconds': float(offset_seconds),
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    

    def get_file_info(self, file_path: str) -> Dict:
        """Get basic information about an audio file."""
        self.validate_file(file_path)
        
        try:
            duration = librosa.get_duration(path=file_path)
            return {
                'file_path': file_path,
                'duration_seconds': float(duration),
                'exists': True,
                'format': os.path.splitext(file_path)[1].lower()
            }
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'exists': False
            }


# Convenience function for direct usage
def sync_audio_files(reference_file: str, target_file: str) -> Dict:
    """
    Convenience function to sync two audio files.
    
    Args:
        reference_file: Path to reference audio file
        target_file: Path to audio file to be synchronized

    Returns:
        Dict containing sync results
    """
    processor = AudioSyncProcessor()
    return processor.sync_files(reference_file, target_file)
