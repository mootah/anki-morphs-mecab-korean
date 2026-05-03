from pathlib import Path
import sys

VENDOR = Path(__file__).parent / "vendor"

if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

