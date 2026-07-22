from pathlib import Path
import sys


PROJECT_DIRECTORY = Path(__file__).resolve().parent

if str(PROJECT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIRECTORY))