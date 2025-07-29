import numpy as np

# Utility to decode audio_chunk bytes to numpy array
def decode_audio_chunk_bytes(audio_chunk_bytes, shape=None, dtype=np.int16):
    """
    Decodes audio_chunk bytes to a numpy array.
    If shape is provided, assumes raw array; otherwise, returns None.
    Args:
        audio_chunk_bytes: bytes or memoryview containing audio data.
        shape: tuple, if known (e.g., (n_samples, 2)) for raw arrays.
        dtype: numpy dtype, default np.int16.
    Returns:
        chunk: numpy array or None if decoding fails.
    """
    if isinstance(audio_chunk_bytes, memoryview):
        print(f"[DEBUG] Converting memoryview to bytes (length: {len(audio_chunk_bytes)})")
        audio_chunk_bytes = audio_chunk_bytes.tobytes()
    if shape is not None:
        try:
            print(f"[DEBUG] Attempting to reshape buffer to shape {shape} and dtype {dtype} (buffer length: {len(audio_chunk_bytes)})")
            chunk = np.frombuffer(audio_chunk_bytes, dtype=dtype).reshape(shape)
            print(f"[DEBUG] Successfully reshaped raw audio_chunk: {chunk.shape}, dtype: {chunk.dtype}")
            return chunk
        except Exception as e:
            print(f"[ERROR] Could not reshape raw audio_chunk: {e}")
            return None
    else:
        print(f"[ERROR] No shape provided for audio_chunk decoding.")
        return None

# AudioPerception class to wrap feature extraction
class AudioPerception:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def process_chunk(self, chunk, chunk_timestamp=None):
        """
        Process a raw audio chunk and extract features, recording lag for each feature.
        Args:
            chunk: numpy array (n_samples, 2)
            chunk_timestamp: float or datetime, time when chunk was captured (for lag calculation)
        Returns:
            observation: dict with high-level features and per-feature lag (in seconds)
        """
        import time
        if chunk_timestamp is None:
            chunk_timestamp = time.time()
        observation = {}
        def timed_feature(fn, *args, **kwargs):
            t0 = time.time()
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                result = f"Error: {e}"
            t1 = time.time()
            lag = t1 - chunk_timestamp if isinstance(chunk_timestamp, (int, float)) else (t1 - chunk_timestamp.timestamp())
            return {'value': result, 'lag': lag}

        observation['bandpass_300_3400Hz'] = timed_feature(bandpass_filter, chunk, 300, 3400, self.sample_rate)
        observation['envelope'] = timed_feature(envelope_detection, chunk)
        observation['onset'] = timed_feature(onset_detection, chunk, self.sample_rate)
        observation['pitch'] = timed_feature(pitch_detection, chunk, self.sample_rate)
        observation['spatial_localization'] = timed_feature(spatial_localization, chunk, self.sample_rate)
        observation['spectral_centroid'] = timed_feature(spectral_centroid, chunk, self.sample_rate)
        observation['chunk_timestamp'] = chunk_timestamp
        return observation
"""
perception.py

Audio perception pre-processing for embodied agent.
Defines baseline functions for auditory pre-filters inspired by human hearing.
These functions are currently stubs and can be implemented incrementally.
"""


import numpy as np
from scipy.signal import butter, lfilter

def bandpass_filter(audio_signal, low_freq, high_freq, sample_rate):
    """
    Simulate cochlear frequency filtering (critical bands) using a Butterworth bandpass filter.
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples, shape (n_samples, 2) for stereo.
        low_freq (float): Low cutoff frequency in Hz.
        high_freq (float): High cutoff frequency in Hz.
        sample_rate (int): Sampling rate in Hz.
    Returns:
        np.ndarray: Bandpass-filtered audio signal (same shape as input).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("audio_signal must be 2D with shape (n_samples, 2) for stereo.")
    # The Nyquist frequency is half the sample rate. It's the highest frequency that can be represented.
    nyquist = 0.5 * sample_rate
    # Normalize the cutoff frequencies to be a ratio of the Nyquist frequency (required by scipy)
    # For example, if low_freq=300Hz, sample_rate=44100Hz, then low=300/22050 ≈ 0.0136
    low = low_freq / nyquist
    high = high_freq / nyquist
    # Design a 4th-order Butterworth bandpass filter
    # 'b' and 'a' are the filter coefficients for the numerator and denominator of the filter's transfer function
    b, a = butter(N=4, Wn=[low, high], btype='band')
    # Apply the filter to each channel independently (left and right)
    left = lfilter(b, a, audio_signal[:, 0])
    right = lfilter(b, a, audio_signal[:, 1])
    # Stack the filtered channels back together into a stereo signal
    return np.stack([left, right], axis=1)

def envelope_detection(audio_signal):
    """
    Detect amplitude envelope (loudness over time).
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples, shape (n_samples, 2) for stereo.
    Returns:
        np.ndarray: Envelope of the audio signal (same shape as input).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("audio_signal must be 2D with shape (n_samples, 2) for stereo.")
    left = np.abs(audio_signal[:, 0])
    right = np.abs(audio_signal[:, 1])
    return np.stack([left, right], axis=1)

def onset_detection(audio_signal, sample_rate):
    """
    Detect sudden changes (onsets) in the audio signal.
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples, shape (n_samples, 2) for stereo.
        sample_rate (int): Sampling rate in Hz.
    Returns:
        np.ndarray: Onset strength (same shape as input).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("audio_signal must be 2D with shape (n_samples, 2) for stereo.")
    def simple_onset(sig):
        return np.diff(np.abs(sig), prepend=0)
    left = simple_onset(audio_signal[:, 0])
    right = simple_onset(audio_signal[:, 1])
    return np.stack([left, right], axis=1)

def pitch_detection(audio_signal, sample_rate):
    """
    Estimate the fundamental frequency (pitch).
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples, shape (n_samples, 2) for stereo.
        sample_rate (int): Sampling rate in Hz.
    Returns:
        list or np.ndarray: Estimated pitch for each channel (None if not implemented).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("audio_signal must be 2D with shape (n_samples, 2) for stereo.")
    pitches = []
    min_freq = 50
    max_freq = 2000
    min_lag = int(sample_rate / max_freq)
    max_lag = int(sample_rate / min_freq)
    for ch in range(2):
        sig = audio_signal[:, ch]
        # Normalize if int16
        if sig.dtype == np.int16:
            sig = sig.astype(np.float32) / 32768.0
        else:
            sig = sig.astype(np.float32)
        print(f"[DEBUG] Channel {ch}: min={sig.min()}, max={sig.max()}, mean={sig.mean()}, std={sig.std()}")
        sig = sig - np.mean(sig)  # Remove DC
        if np.all(sig == 0):
            print(f"[DEBUG] Channel {ch}: signal is all zeros after DC removal.")
            pitches.append(None)
            continue
        if len(sig) < max_lag:
            print(f"[DEBUG] Channel {ch}: signal too short for pitch detection (len={len(sig)}, need >{max_lag}).")
            pitches.append(None)
            continue
        # Autocorrelation
        corr = np.correlate(sig, sig, mode='full')
        corr = corr[len(corr)//2:]
        # Only search for peaks in valid lag range
        search_corr = corr[min_lag:max_lag]
        if len(search_corr) == 0:
            print(f"[DEBUG] Channel {ch}: no valid lag range for pitch.")
            pitches.append(None)
            continue
        peak = np.argmax(search_corr) + min_lag
        peak_value = corr[peak]
        zero_lag = corr[0]
        print(f"[DEBUG] Channel {ch}: peak lag={peak}, value={peak_value}, zero_lag={zero_lag}")
        # Require peak to be at least 10% of zero-lag value
        if peak == 0 or zero_lag == 0 or peak_value < 0.1 * zero_lag:
            print(f"[DEBUG] Channel {ch}: peak not significant (peak_value={peak_value}, zero_lag={zero_lag})")
            pitches.append(None)
            continue
        pitch = sample_rate / peak
        print(f"[DEBUG] Channel {ch}: estimated pitch={pitch} Hz")
        if min_freq < pitch < max_freq:
            pitches.append(pitch)
        else:
            pitches.append(None)
    return pitches

def spatial_localization(audio_signal, sample_rate):
    """
    Estimate direction of arrival (left/right cues).
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples (n_samples, 2) for stereo.
        sample_rate (int): Sampling rate in Hz.
    Returns:
        float: Placeholder for direction estimate (None if not implemented).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("spatial_localization requires stereo input (n_samples, 2)")
    return None  # To be implemented

def spectral_centroid(audio_signal, sample_rate):
    """
    Compute spectral centroid (brightness of sound).
    Args:
        audio_signal (np.ndarray): 2D numpy array of audio samples, shape (n_samples, 2) for stereo.
        sample_rate (int): Sampling rate in Hz.
    Returns:
        list: Spectral centroid for each channel (None if not implemented).
    Raises:
        ValueError: If audio_signal is not stereo (2 channels).
    """
    if audio_signal.ndim != 2 or audio_signal.shape[1] != 2:
        raise ValueError("audio_signal must be 2D with shape (n_samples, 2) for stereo.")
    return [None, None]  # To be implemented per channel

# Add more auditory pre-processing stubs as needed