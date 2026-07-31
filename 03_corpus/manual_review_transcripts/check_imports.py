#!/usr/bin/env python3
"""Quick test to verify Python imports work."""
import sys
print(f"Python {sys.version}")
try:
    import requests
    print(f"requests {requests.__version__} - OK")
except ImportError:
    print("requests not installed")
try:
    import base64
    print("base64 - OK")
except ImportError:
    print("base64 not installed")
