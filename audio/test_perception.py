
"""
test_perception.py (audio, streaming)

Test script to stream live audio segments through the audio perception pipeline and print results in real time.
"""

import time
from audio_capture import AudioInputCapture
from perception import AudioPerception

def perception_callback(audio_chunk, timestamp):

    import psutil
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
    except ImportError:
        GPUtil = None
        gpus = []

    ap = AudioPerception()
    obs = ap.process_chunk(audio_chunk, chunk_timestamp=timestamp)
    print("\n[RESULT] Audio perception output:")
    for k, v in obs.items():
        if isinstance(v, dict) and 'lag' in v:
            print(f"  {k}: value={v['value']}, lag={v['lag']:.4f}s")
        else:
            print(f"  {k}: {v}")

    # System performance monitoring
    print("[SYSTEM] Hardware performance:")
    # RAM
    vm = psutil.virtual_memory()
    print(f"  RAM: {vm.used / (1024**3):.2f} GB used / {vm.total / (1024**3):.2f} GB total ({vm.percent}%)")
    # CPU
    cpu_percent = psutil.cpu_percent(interval=None)
    print(f"  CPU: {cpu_percent:.1f}% usage")
    # Load average (Linux/Unix)
    try:
        load1, load5, load15 = psutil.getloadavg()
        print(f"  Load average (1/5/15 min): {load1:.2f} / {load5:.2f} / {load15:.2f}")
    except (AttributeError, OSError):
        pass
    # GPU/VRAM
    if gpus:
        for gpu in gpus:
            print(f"  GPU {gpu.id}: {gpu.name}, load={gpu.load*100:.1f}%, VRAM used={gpu.memoryUsed}MB / {gpu.memoryTotal}MB ({gpu.memoryUtil*100:.1f}%)")
    elif GPUtil is not None:
        print("  No GPUs detected.")
    else:
        print("  GPUtil not installed (no GPU/VRAM info). To enable: pip install gputil")

if __name__ == "__main__":
    output_dir = "training_data/audio"
    capture = AudioInputCapture(output_dir, samplerate=44100, channels=2, segment_duration=0.02)
    print("[INFO] Starting audio streaming test. Speak or make noise to see perception output. Press Ctrl+C to stop.")
    capture.stream_audio(perception_callback, parallel=False)
