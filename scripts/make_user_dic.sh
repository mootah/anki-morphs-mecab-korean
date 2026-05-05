#!/usr/bin/env bash
set -euo pipefail

# Find project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADDON_DIR="$PROJECT_ROOT/addon/anki_morphs_mecab_korean"
CSV_FILE="$PROJECT_ROOT/scripts/user_nnp.csv"
DIC_FILE="$ADDON_DIR/user_nnp.dic"

# Write the CSV file
# Format: <surface>,<left_id>,<right_id>,<cost>,<POS>,<semantic_class>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
cat <<EOF > "$CSV_FILE"
PROPNT,1786,3546,0,NNP,*,T,PROPNT,*,*,*,*
PROPNF,1786,3545,0,NNP,*,F,PROPNF,*,*,*,*
EOF

echo "Created user dictionary CSV at $CSV_FILE"

# Find openkorpos_dic directory
DICDIR=$("$PROJECT_ROOT/.venv/bin/python" -c 'import openkorpos_dic, os; print(os.path.join(os.path.dirname(openkorpos_dic.__file__), "dicdir"))' 2>/dev/null || true)

if [ -z "$DICDIR" ]; then
    echo "Error: openkorpos_dic not found. Please ensure your virtual environment is set up."
    exit 1
fi

echo "Using system dictionary from: $DICDIR"

# Check if mecab-dict-index is available
if ! command -v mecab-dict-index &> /dev/null; then
    echo "============================================================"
    echo "ERROR: mecab-dict-index is not installed."
    echo "To compile the dictionary, you need the MeCab toolkit."
    echo "============================================================"
    exit 1
fi

echo "Compiling dictionary..."
mecab-dict-index -d "$DICDIR" -u "$DIC_FILE" -f utf-8 -t utf-8 "$CSV_FILE"

echo "Success! Compiled user dictionary to: $DIC_FILE"