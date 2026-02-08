# Quick Start: Using Groq AI for FREE Translation

## Step 1: Get FREE Groq API Key (30 seconds)

1. Go to: **https://console.groq.com**
2. Click "Sign Up" (free, no credit card)
3. Go to "API Keys" section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)

## Step 2: Install Groq (10 seconds)

```bash
pip install groq
```

## Step 3: Set API Key

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY="gsk_your_api_key_here"
```

**Windows CMD:**
```cmd
set GROQ_API_KEY=gsk_your_api_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="gsk_your_api_key_here"
```

## Step 4: Run with Groq

```bash
python src/main.py --xml translationDb_HostedSuppCatProduct-Cust.xml --backend groq
```

## That's It!

You'll see:
```
[OK] Using Groq AI for translations (Model: llama-3.3-70b-versatile)
[INFO] Starting translation to sv-SE: 18 fields
[SUCCESS] Translation to sv-SE complete
```

---

## Example: Translate to Multiple Languages

```bash
python src/main.py \
  --xml translationDb_HostedSuppCatProduct-Cust.xml \
  --backend groq \
  --languages sv-SE,nb-NO,da-DK,fi-FI,de-DE
```

This will generate:
- Swedish (sv-SE)
- Norwegian (nb-NO)
- Danish (da-DK)
- Finnish (fi-FI)
- German (de-DE)

All for **FREE**! 🎉

---

## Why Groq?

- ✅ **100% FREE** - No credit card, no limits for reasonable use
- ✅ **Fast** - Uses llama-3.3-70b-versatile (one of the best open models)
- ✅ **Smart** - Understands ERP context better than Google Translate
- ✅ **Reliable** - Better than dictionary, more consistent than Google

---

## Troubleshooting

### "groq library not installed"
```bash
pip install groq
```

### "API key not found"
Make sure you set the environment variable:
```bash
# Check if it's set
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows CMD
$env:GROQ_API_KEY   # Windows PowerShell
```

### Still not working?
Pass the API key directly:
```bash
python src/main.py --xml file.xml --backend groq --api-key "gsk_your_key_here"
```

---

## Full Documentation

See [AI_TRANSLATION_GUIDE.md](file:///C:/Users/KavinduAlahakoon/Downloads/Language%20Files%20Export%202026-02-05%20(1)/AI_TRANSLATION_GUIDE.md) for complete details.
