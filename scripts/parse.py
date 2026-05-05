from __future__ import annotations

import importlib
import sys
from pathlib import Path
import rich_click as click
from rich import print


REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_ROOT = REPO_ROOT / "addon"

if str(ADDON_ROOT) not in sys.path:
    sys.path.insert(0, str(ADDON_ROOT))

MODULE_NAME = "anki_morphs_mecab_korean.reading"
reading = importlib.import_module(MODULE_NAME)
parser = reading.MecabKoreanController()

@click.command()
@click.option("--text", default="", help="Text to analyze", required=True)
def main(text: str):
    print(parser.get_morphs(text))
    
if __name__ == "__main__":
    main()
