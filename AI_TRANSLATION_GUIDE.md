# AI Translation Setup Guide

This guide shows you how to use **FREE AI translation** instead of the built-in dictionary.

## Option 1: Groq AI (Recommended - FREE & Fast)

### Why Groq?
- ✅ **100% FREE** - No credit card required
- ✅ **Very Fast** - Uses llama-3.3-70b-versatile model
- ✅ **High Quality** - Better context understanding than Google Translate
- ✅ **No Rate Limits** for reasonable use

### Setup Steps

1. **Get Free API Key**
   - Go to: https://console.groq.com
   - Sign up (free, no credit card)
   - Go to API Keys section
   - Create a new API key
   - Copy the key (starts with `gsk_...`)

2. **Install Groq Library**
   ```bash
   pip install groq
   ```

3. **Set API Key** (Choose one method)

   **Method A: Environment Variable (Recommended)**
   ```bash
   # Windows PowerShell
   $env:GROQ_API_KEY="gsk_your_api_key_here"
   
   # Windows CMD
   set GROQ_API_KEY=gsk_your_api_key_here
   
   # Linux/Mac
   export GROQ_API_KEY=gsk_your_api_key_here
   ```

   **Method B: Command Line Argument**
   ```bash
   python src/main.py --xml file.xml --backend groq --api-key "gsk_your_api_key_here"
   ```

4. **Run with Groq**
   ```bash
   python src/main.py --xml translationDb_HostedSuppCatProduct-Cust.xml --backend groq
   ```

### Example Output
```
✓ Using Groq AI for translations (Model: llama-3.3-70b-versatile)
[INFO] Starting translation to sv-SE: 18 fields
[SUCCESS] Translation to sv-SE complete
```

---

## Option 2: Google Translate (FREE Tier)

### Why Google Translate?
- ✅ **FREE** for limited use
- ✅ **No API Key Required** (uses unofficial API)
- ✅ **Many Languages** supported
- ⚠️ **Rate Limited** - May fail with many requests

### Setup Steps

1. **Install Google Translate Library**
   ```bash
   pip install googletrans==4.0.0-rc1
   ```

2. **Run with Google Translate**
   ```bash
   python src/main.py --xml translationDb_HostedSuppCatProduct-Cust.xml --backend google
   ```

### Example Output
```
✓ Using Google Translate for translations
[INFO] Starting translation to sv-SE: 18 fields
[SUCCESS] Translation to sv-SE complete
```

---

## Option 3: Built-in Dictionary (Default)

### Why Dictionary?
- ✅ **No Setup** required
- ✅ **Offline** - No internet needed
- ✅ **Instant** - No API calls
- ⚠️ **Limited** - Only pre-defined terms

### Usage
```bash
# Default - no backend argument needed
python src/main.py --xml translationDb_HostedSuppCatProduct-Cust.xml
```

---

## Comparison Table

| Feature | Groq AI | Google Translate | Dictionary |
|---------|---------|------------------|------------|
| **Cost** | FREE | FREE (limited) | FREE |
| **Setup** | API Key | pip install | None |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | Fast | Medium | Instant |
| **Languages** | All major | 100+ | 2 (sv, nb) |
| **Context Aware** | Yes | Partial | No |
| **Offline** | No | No | Yes |
| **Rate Limits** | Generous | Strict | None |

---

## Supported Languages

### With AI (Groq/Google)
You can translate to **any language**:

```bash
# Danish
python src/main.py --xml file.xml --backend groq --languages da-DK

# German
python src/main.py --xml file.xml --backend groq --languages de-DE

# Multiple languages
python src/main.py --xml file.xml --backend groq --languages sv-SE,nb-NO,da-DK,fi-FI
```

### Supported Language Codes
- `sv-SE` - Swedish
- `nb-NO` - Norwegian Bokmål
- `da-DK` - Danish
- `fi-FI` - Finnish
- `de-DE` - German
- `fr-FR` - French
- `es-ES` - Spanish
- `it-IT` - Italian
- `nl-NL` - Dutch
- `pt-PT` - Portuguese
- `pl-PL` - Polish

---

## Advanced Usage

### 1. Translate to Multiple Languages with Groq
```bash
python src/main.py \
  --xml translationDb_HostedSuppCatProduct-Cust.xml \
  --backend groq \
  --languages sv-SE,nb-NO,da-DK,fi-FI
```

### 2. Use Environment Variable for API Key
```bash
# Set once
export GROQ_API_KEY="gsk_your_key_here"

# Use multiple times without specifying key
python src/main.py --xml file1.xml --backend groq
python src/main.py --xml file2.xml --backend groq
```

### 3. Custom Output Directory
```bash
python src/main.py \
  --xml translationDb_HostedSuppCatProduct-Cust.xml \
  --backend groq \
  --output-dir C:\IFS\Translations
```

---

## Troubleshooting

### Groq: "API key not found"
```bash
# Check if environment variable is set
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows CMD
$env:GROQ_API_KEY   # Windows PowerShell

# If not set, set it:
export GROQ_API_KEY="gsk_your_key_here"
```

### Groq: "groq library not installed"
```bash
pip install groq
```

### Google: "googletrans library not installed"
```bash
pip install googletrans==4.0.0-rc1
```

### Google: "Translation failed"
- Google Translate has rate limits
- Try again after a few minutes
- Or switch to Groq: `--backend groq`

### Fallback Behavior
If AI translation fails, the tool automatically falls back to dictionary mode:
```
⚠ Groq translation failed: API key invalid
  Falling back to dictionary
✓ Using built-in dictionary for translations
```

---

## Best Practices

### 1. Use Groq for Production
- Most reliable
- Best quality
- Fastest
- FREE

### 2. Cache Translations
The tool automatically caches translations, so:
- Re-running on same file is instant
- No duplicate API calls
- Saves API quota

### 3. Batch Processing
Process multiple files efficiently:
```bash
# Process all XML files
for file in *.xml; do
  python src/main.py --xml "$file" --backend groq
done
```

### 4. Verify Translations
Always review AI-generated translations:
1. Check Log.txt for translation results
2. Review .trs files
3. Test in IFS before production

---

## Cost Comparison

| Backend | Cost | Limit |
|---------|------|-------|
| Groq | $0 | ~14,400 requests/day |
| Google Translate | $0 | ~100-500 requests/day (unofficial) |
| Dictionary | $0 | Unlimited |

**Recommendation**: Use **Groq** for best results at zero cost.

---

## Example: Complete Workflow

```bash
# 1. Get Groq API key from https://console.groq.com
# 2. Set environment variable
export GROQ_API_KEY="gsk_your_key_here"

# 3. Install Groq
pip install groq

# 4. Run translation
python src/main.py \
  --xml translationDb_HostedSuppCatProduct-Cust.xml \
  --backend groq \
  --languages sv-SE,nb-NO,da-DK

# 5. Check results
cat Log.txt
cat Esspro_LU_LogicalUnit-Cust-sv.trs

# 6. Import into IFS
# (manual step in IFS Applications)
```

---

## Need Help?

1. Check [README.md](file:///C:/Users/KavinduAlahakoon/Downloads/Language%20Files%20Export%202026-02-05%20(1)/README.md) for general usage
2. Check [QUICKSTART.md](file:///C:/Users/KavinduAlahakoon/Downloads/Language%20Files%20Export%202026-02-05%20(1)/QUICKSTART.md) for basic setup
3. Review Log.txt for detailed error messages
4. Test with `--backend dictionary` first to verify XML parsing works
