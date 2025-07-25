from input.input_capture import InputCapture

def test_input_capture_pause():
    capture = InputCapture()
    capture.start_listeners()
    capture.pause()
    # After pause, listeners should be stopped
    assert not hasattr(capture, 'keyboard_listener') or not capture.keyboard_listener.running
    assert not hasattr(capture, 'mouse_listener') or not capture.mouse_listener.running
    print("InputCapture pause test passed.")

if __name__ == "__main__":
    test_input_capture_pause()
