import os
import subprocess
import re
from django.shortcuts import render
import pandas as pd

# ─── CONFIG: paths ───────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CSV_PATH    = os.path.join(BASE_DIR, 'phoneme_vibration_table.csv')
PROJECT_DIR = os.path.dirname(BASE_DIR)
ESPEAK_BIN  = '/usr/bin/espeak'

# ─── LOAD CSV once ────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, encoding='utf-8-sig', dtype=str)
df['Phoneme']           = df['Phoneme'].str.strip()
df['Vibration_Pattern'] = df['Vibration_Pattern'].str.strip()
phoneme_dict = dict(zip(df['Phoneme'], df['Vibration_Pattern']))

# ─── X-SAMPA SPLITTING & IPA MAPPING ──────────────────────────────────────────────
# splits “goUIN” → ["g","oU","IN"]
TOKEN_RE = re.compile(r"[a-z][A-Z]+|[A-Z]+|[a-z]")
# map multi-char X-SAMPA tokens back to your IPA keys
XSAMPA_TO_IPA = {
    "aI":  "aɪ",
    "aU":  "aʊ",
    "oU":  "oʊ",
    "IN":  "ŋ",
    "OI":  "ɔɪ",
}
# build a regex that matches your multi-char tokens first, then single letters
_x_keys = sorted(XSAMPA_TO_IPA.keys(), key=len, reverse=True)
_pattern = "|".join(re.escape(k) for k in _x_keys)
TOKEN_RE = re.compile(f"(?:{_pattern})|[A-Z]|[a-z]")

# ─── HELPER: convert text to vibration patterns ─────────────────────────────────
def text_to_vibrations(text):
    output = []
    for word in text.split():
        # invoke espeak with X-SAMPA (-x) and merge stderr
        proc = subprocess.run(
            [ESPEAK_BIN, '-q', '-x', word],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        raw = proc.stdout.decode('utf-8', errors='ignore').strip()
        print(f"[espeak raw] {word!r} → {raw!r}")

        # strip any surrounding quotes, then remove @, spaces, tabs, AND internal apostrophes
        raw = raw.strip('"').strip("'")
        raw = (
            raw
            .replace("@", "")
            .replace(" ", "")
            .replace("\t", "")
            .replace("'", "")  # ← this is the new line
        )
        # split into X-SAMPA tokens
        x_tokens = TOKEN_RE.findall(raw)

        if not x_tokens:
            x_tokens = list(word.lower())

        phonemes = []
        patterns = []
        for x_ph in x_tokens:
            # 1) map X-SAMPA → IPA (or lowercase single-char)
            ipa_ph = XSAMPA_TO_IPA.get(x_ph, x_ph.lower())
            # 2) lookup vibration (fall back if missing)
            pat = phoneme_dict.get(ipa_ph)
            if not pat:
                print(f" ⚠️ no mapping for IPA {ipa_ph!r}; falling back")
                pat = 'C-0-0'
            phonemes.append(ipa_ph)
            patterns.append(pat)

        output.append({
            'word':     word,
            'phonemes': phonemes,
            'pattern':  "|".join(patterns),
        })

    return output

# ─── VIEW ────────────────────────────────────────────────────────────────────────
def index(request):
    print("===> INDEX VIEW CALLED, method:", request.method)
    if request.method == 'POST':
        print("===> RAW POST DATA:", request.POST)

    context = {}
    if request.method == 'POST':
        txt = request.POST.get('spoken_text', None)
        print(f"===> RAW txt from POST.get('spoken_text') → {repr(txt)}")

        if txt:
            print("===> txt is truthy, will convert")
            try:
                context['original'] = txt
                context['result']   = text_to_vibrations(txt)
                print("===> COMPUTED RESULT:", context['result'])
            except subprocess.CalledProcessError as e:
                context['error'] = "Espeak error: " + e.stderr.decode()
            except Exception as e:
                context['error'] = str(e)
        else:
            print("===> txt is empty or None; skipping conversion")

    return render(request, 'translator/index.html', context)
