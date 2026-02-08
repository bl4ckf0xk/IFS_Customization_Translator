# IFS Language Automation Tool

## Overview

Deterministic automation tool for IFS Applications language handling. Processes TranslatableResources XML files and generates/updates IFS Foundation language files (.lng) and translation files (.trs) for customized fields only.

## Features

- ✅ **XML Parsing**: Extracts custom fields (C_* prefix) from TranslatableResources XML
- ✅ **Automatic .lng Generation**: Creates properly formatted language files with CS/CE blocks
- ✅ **Automatic .trs Generation**: Creates translation files for Swedish (sv-SE) and Norwegian (nb-NO)
- ✅ **AI Translation**: Translates field labels using enterprise-appropriate terminology
- ✅ **Validation**: Validates all generated files for correctness
- ✅ **Logging**: Comprehensive logging of all actions and decisions
- ✅ **Deterministic**: Same input always produces same output

## Requirements

- Python 3.7+
- For **running the tool**: standard library only (no pip install required).
- For **running tests**: `pip install -r requirements.txt` (pytest).
- For **AI translation** (Groq or Google): `pip install -r requirements-optional.txt`.

## Installation

```bash
# Optional: install test dependencies
pip install -r requirements.txt

# Optional: install AI translation backends (Groq, Google)
pip install -r requirements-optional.txt
```

To run the tool, no installation is required; all core modules use the standard library.

## Testing

From the **repository root**:

```bash
pytest tests/ -v
```

Tests run the tool on all `test/translationDb_*.xml` fixtures, validate generated .lng and .trs files, compare ActivityEstimate output to reference fixtures, and verify dictionary translations for Swedish and Norwegian.

For **production use**, run the tool from the project directory with the path to `src/main.py` and your XML file (see Usage below).

## Usage

### Basic Usage

Run from the **`src`** directory so that the tool can import its modules:

```bash
cd src
python main.py --xml path/to/translationDb_YourModule-Cust.xml
```

Example from repository root:

```bash
cd src && python main.py --xml ../test/translationDb_ActivityEstimate-Cust.xml
```

### Advanced Options

```bash
# Specify output directory
python src/main.py --xml path/to/file.xml --output-dir path/to/output

# Specify languages
python src/main.py --xml file.xml --languages sv-SE,nb-NO

# Validate only (not yet implemented)
python src/main.py --xml file.xml --validate-only
```

## Project Structure

```
Language Files Export 2026-02-05 (1)/
├── src/
│   ├── main.py              # Entry point and orchestration
│   ├── parser.py            # XML parsing
│   ├── lng_generator.py     # .lng file generation
│   ├── trs_generator.py     # .trs file generation
│   ├── translator.py        # AI translation service
│   ├── validator.py         # File validation
│   └── logger.py            # Logging utilities
├── translationDb_*.xml      # Input XML files
├── Esspro_LU_*.lng          # Generated language files
├── Esspro_LU_*-sv.trs       # Generated Swedish translations
├── Esspro_LU_*-no.trs       # Generated Norwegian translations
└── Log.txt                  # Execution log
```

## Scope Rules

1. **Process ONLY** fields whose identifiers start with "C_"
2. **Ignore** standard fields completely
3. **Preserve** full hierarchy: Logical Unit → View → Column
4. **Never modify** module, layer, LU name, or metadata unless derived from XML

## File Format

### .lng File Format

```
-------------------------------------------------------
File Type: IFS Foundation Language File
Type version: 10.00
-------------------------------------------------------
Module: ESSPRO
Layer: Cust
Main Type: LU
Sub Type: Logical Unit
Content: 
-------------------------------------------------------
CS:LogicalUnitName^LU^Logical Unit^N^N
	A:Prompt^Logical Unit Label^
	CS:VIEW_NAME^LU^View^N^N
		CS:C_FIELD_NAME^LU^Column^N^N
			A:Prompt^Field Label^
		CE:
	CE:
CE:
```

### .trs File Format

```
-------------------------------------------------------
File Type: IFS Foundation Translation File
Type version: 10.00
-------------------------------------------------------
Module: ESSPRO
Language: sv
Culture: sv-SE
Layer: Cust
Main Type: LU
Sub Type: Logical Unit
Content: 
-------------------------------------------------------
CS:LogicalUnitName^LU
	CS:VIEW_NAME^LU
		CS:C_FIELD_NAME^LU
			P:Field Label^
			A:Prompt^Fältnamn^
		CE:
	CE:
CE:
```

## Translation

The tool includes default translations for common IFS ERP terms in:
- **Swedish (sv-SE)**: Enterprise-appropriate Swedish terminology
- **Norwegian (nb-NO)**: Enterprise-appropriate Norwegian Bokmål terminology

Translations maintain:
- Professional ERP terminology
- Consistency across similar terms
- Preservation of universal abbreviations (EAN, URL, UOM, etc.)

## Validation

All generated files are validated for:
- ✅ Correct CS/CE pairing
- ✅ Proper indentation (tabs)
- ✅ Valid header format
- ✅ Correct structure for .lng and .trs files
- ✅ No orphan nodes

## Logging

All actions are logged to `Log.txt` including:
- Timestamp for each action
- Files processed
- Fields extracted and skipped
- Translation actions
- Validation results
- Errors and warnings

## Example Output

For the provided XML file `translationDb_HostedSuppCatProduct-Cust.xml`:

**Input**: 51 total columns (18 custom, 33 standard)

**Output**:
- `Esspro_LU_LogicalUnit-Cust.lng` - Language file with 18 custom fields
- `Esspro_LU_LogicalUnit-Cust-sv.trs` - Swedish translations
- `Esspro_LU_LogicalUnit-Cust-nb.trs` - Norwegian translations
- `Log.txt` - Detailed execution log

## Non-Goals

- ❌ No UI or interactive prompts
- ❌ No manual field selection
- ❌ No modification of non-C_* fields
- ❌ No reformatting of existing file content
- ❌ No inference beyond XML content

## License

MIT License. See [LICENSE](LICENSE). This tool is designed for IFS Applications customization projects.
