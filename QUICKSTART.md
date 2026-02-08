# IFS Language Automation Tool - Quick Start Guide

## What This Tool Does

Automatically generates IFS language files (.lng) and translation files (.trs) from TranslatableResources XML files for **custom fields only** (C_* prefix).

## Prerequisites

- Python 3.7 or higher
- No additional packages required (uses standard library only)

## Quick Start

### 1. Basic Usage

```bash
# Navigate to project directory
cd "C:\Users\KavinduAlahakoon\Downloads\Language Files Export 2026-02-05 (1)"

# Run the tool
python src/main.py --xml translationDb_HostedSuppCatProduct-Cust.xml
```

### 2. What Happens

The tool will:
1. ✅ Parse the XML file
2. ✅ Extract custom fields (C_* prefix only)
3. ✅ Skip standard fields automatically
4. ✅ Generate .lng file with proper CS/CE blocks
5. ✅ Translate labels to Swedish and Norwegian
6. ✅ Generate .trs files for each language
7. ✅ Validate all generated files
8. ✅ Log everything to Log.txt

### 3. Output Files

After running, you'll find:

- `Esspro_LU_LogicalUnit-Cust.lng` - Language file
- `Esspro_LU_LogicalUnit-Cust-sv.trs` - Swedish translations
- `Esspro_LU_LogicalUnit-Cust-nb.trs` - Norwegian translations
- `Log.txt` - Detailed execution log (appended)

## Advanced Options

### Specify Output Directory

```bash
python src/main.py --xml file.xml --output-dir C:\path\to\output
```

### Specify Languages

```bash
# Only Swedish
python src/main.py --xml file.xml --languages sv-SE

# Multiple languages
python src/main.py --xml file.xml --languages sv-SE,nb-NO,da-DK
```

## Understanding the Output

### .lng File Structure

```
CS:LogicalUnitName^LU^Logical Unit^N^N
	A:Prompt^Logical Unit Label^
	CS:VIEW_NAME^LU^View^N^N
		CS:C_CUSTOM_FIELD^LU^Column^N^N
			A:Prompt^Field Label^
		CE:
	CE:
CE:
```

### .trs File Structure

```
CS:LogicalUnitName^LU
	CS:VIEW_NAME^LU
		CS:C_CUSTOM_FIELD^LU
			P:Field Label^
			A:Prompt^Översatt etikett^
		CE:
	CE:
CE:
```

## Key Features

### ✅ Automatic Filtering
- Only processes fields starting with `C_`
- Skips all standard fields automatically
- No manual selection needed

### ✅ Validation
- Checks CS/CE pairing
- Validates indentation
- Ensures proper file structure
- Fails fast on errors

### ✅ Logging
- Every action logged with timestamp
- Fields processed and skipped
- Translation results
- Validation outcomes

### ✅ Deterministic
- Same input = same output
- Repeatable results
- No randomness

## Troubleshooting

### Error: "XML file not found"
- Check the file path is correct
- Use quotes around paths with spaces
- Ensure XML file exists

### Error: "Validation failed"
- Check Log.txt for details
- Ensure XML is valid IFS format
- Contact support if issue persists

### No custom fields found
- Verify XML contains C_* fields
- Check Log.txt for parsing details
- Ensure XML is not empty

## File Naming Convention

Generated files follow IFS naming standards:

- **Module**: First letter capitalized, rest lowercase (e.g., `Esspro`)
- **Format**: `{Module}_LU_LogicalUnit-{Layer}.lng`
- **Languages**: `{Module}_LU_LogicalUnit-{Layer}-{lang}.trs`

Examples:
- `Esspro_LU_LogicalUnit-Cust.lng`
- `Esspro_LU_LogicalUnit-Cust-sv.trs`
- `Esspro_LU_LogicalUnit-Cust-nb.trs`

## Supported Languages

Currently supported:
- `sv-SE` - Swedish
- `nb-NO` - Norwegian Bokmål

To add more languages, modify `translator.py`.

## Log File

The `Log.txt` file contains:
- Timestamp for each run
- Fields processed and skipped
- Translation results
- Validation outcomes
- Error messages (if any)

Example log entry:
```
[2026-02-05 16:53:15] [INFO] Processing custom field: C_BRANCH_NO -> 'Branch No'
[2026-02-05 16:53:15] [SUCCESS] Extracted 18 custom fields
[2026-02-05 16:53:15] [INFO] Skipped 15 standard fields (non-C_* prefix)
```

## Best Practices

1. **Always review Log.txt** after each run
2. **Validate files** in IFS before importing
3. **Keep backups** of existing language files
4. **Run tool in test environment** first
5. **Check translations** for accuracy

## Example Workflow

```bash
# 1. Export XML from IFS
# (done manually in IFS)

# 2. Run automation tool
python src/main.py --xml translationDb_MyModule-Cust.xml

# 3. Review output
cat Log.txt

# 4. Validate generated files
# (files are auto-validated by tool)

# 5. Import into IFS
# (done manually in IFS)
```

## Success Indicators

You'll see this when successful:

```
============================================================
SUCCESS: All files generated and validated
============================================================

Generated files in: .
Log Summary: 44 info, 0 warnings, 0 errors, 10 success
```

## Getting Help

1. Check [README.md](file:///C:/Users/KavinduAlahakoon/Downloads/Language%20Files%20Export%202026-02-05%20(1)/README.md) for detailed documentation
2. Review [walkthrough.md](file:///C:/Users/KavinduAlahakoon/.gemini/antigravity/brain/257c021f-a7d0-4cfd-8ce7-6f010c326ff3/walkthrough.md) for implementation details
3. Examine Log.txt for execution details
4. Check source code comments in `src/` directory

## Common Use Cases

### Process Single XML File
```bash
python src/main.py --xml translationDb_Module-Cust.xml
```

### Process with Custom Output Location
```bash
python src/main.py --xml file.xml --output-dir C:\IFS\Languages
```

### Generate Only Swedish Translations
```bash
python src/main.py --xml file.xml --languages sv-SE
```

## What NOT to Do

❌ Don't edit generated files manually (re-run tool instead)
❌ Don't process non-IFS XML files
❌ Don't modify C_* field names in XML
❌ Don't skip validation step
❌ Don't ignore warnings in Log.txt

## Production Checklist

Before using in production:

- [ ] Test with sample XML file
- [ ] Review generated .lng file
- [ ] Review generated .trs files
- [ ] Verify translations are correct
- [ ] Check Log.txt for warnings
- [ ] Validate in IFS test environment
- [ ] Get approval from stakeholders
- [ ] Import into production IFS

---

**Tool Version**: 1.0  
**Last Updated**: 2026-02-05  
**Python Required**: 3.7+  
**Dependencies**: None (standard library only)
