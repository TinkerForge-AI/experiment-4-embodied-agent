import os
import sys
import importlib.util

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.join(TEST_ROOT, 'unit')
E2E_DIR = os.path.join(TEST_ROOT, 'e2e')

def run_test_file(test_path):
    print(f"\n[RUNNING] {os.path.relpath(test_path, TEST_ROOT)}")
    spec = importlib.util.spec_from_file_location("test_module", test_path)
    test_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(test_module)
        print(f"[PASS] {os.path.relpath(test_path, TEST_ROOT)}")
    except Exception as e:
        print(f"[FAIL] {os.path.relpath(test_path, TEST_ROOT)}")
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

def run_all_tests():
    print("\n==============================")
    print("  Comprehensive Test Runner   ")
    print("==============================\n")
    print("[INFO] Running unit tests...")
    for fname in sorted(os.listdir(UNIT_DIR)):
        if fname.startswith('test_') and fname.endswith('.py'):
            run_test_file(os.path.join(UNIT_DIR, fname))
    print("\n[INFO] Running end-to-end tests...")
    for fname in sorted(os.listdir(E2E_DIR)):
        if fname.startswith('test_') and fname.endswith('.py'):
            run_test_file(os.path.join(E2E_DIR, fname))
    print("\n==============================")
    print("  All tests completed.        ")
    print("==============================\n")

if __name__ == "__main__":
    run_all_tests()
