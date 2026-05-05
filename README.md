# AnkiMorphs Mecab Korean

A companion Anki add-on for [AnkiMorphs](https://github.com/mootah/anki-morphs) that provides a Korean morphemizer using MeCab (`mecab-ko` / `openkorpos-dic`).

## Prerequisites

To use this add-on, **you must use the customized fork of AnkiMorphs**:
**[mootah/anki-morphs](https://github.com/mootah/anki-morphs)**

This add-on relies on a specific morphemizer handler that is only available in the fork.

### Installing AnkiMorphs

1. Clone the repository:
   ```zsh
   git clone git@github.com:mootah/anki-morphs.git
   ```
2. Copy the `ankimorphs` directory from the cloned repository into your Anki add-ons folder (`addons21`).

   **Example:**
   ```zsh
   cp -r /path/to/cloned/anki-morphs/ankimorphs /path/to/your/Anki2/addons21/ankimorphs
   ```

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```zsh
# 1. Download and sync dependencies
uv sync

# 2. Run tests (optional)
uv run pytest

# 3. Install the add-on to your Anki addons directory
uv run scripts/install_addon.py
```

### Development Mode

If you are developing or modifying the code, you can install the add-on as a **symlink** using the `-e` (editable) flag. This allows your changes to be reflected immediately without having to reinstall:

```zsh
uv run scripts/install_addon.py -e
```

## Morphemization Rules

This add-on customizes the parsing results of `mecab-ko` to provide a more natural Korean learning experience within AnkiMorphs. The main rules are as follows:

### 1. Handling of Compound Words
By default, `mecab-ko` may split certain compound words into their constituent components. If a morpheme is identified as a `Compound` based on its feature information, this add-on adopts the base form of the original compound word as the lemma, rather than the finely segmented roots. This prevents compound words that should be treated as a single word from being unnaturally split.

### 2. Handling of Contracted Particles and Endings
When multiple endings or particles are attached (contracted) to words, this add-on expands and analyzes the combined morpheme information. It then extracts only the base "stem" part located at the very beginning to serve as the lemma. This ensures that even with complex conjugations or contracted forms, they are correctly grouped as the same base form in AnkiMorphs.

### 3. Handling of Proper Nouns (`names.txt`)
This add-on supports parsing using AnkiMorphs' `names.txt` (proper noun list).
Before passing the text to the morpheme analysis engine, words in the list are temporarily replaced with placeholders (`PROPNT` or `PROPNF` depending on the presence of a final consonant/jongseong). This allows the process to execute without hindering the natural analysis of immediately following particles (such as "은/는" or "이/가"), and accurately restores them as the original proper nouns (POS: "Noun", Sub-POS: "Proper Noun") after parsing.
