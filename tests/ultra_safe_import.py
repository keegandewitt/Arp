"""Ultra-safe import test"""
import time

print("Testing if i2cdisplaybus can be imported...")
print("Starting in 2 seconds...")
time.sleep(2)

result = "unknown"
try:
    __import__('i2cdisplaybus')
    result = "SUCCESS - imported without crash"
except ImportError:
    result = "Module not found (ImportError)"
except Exception as e:
    result = f"Exception: {type(e).__name__}: {e}"

print(f"Result: {result}")

print("\nIf you see this, the test completed without crashing")
while True:
    time.sleep(1)
