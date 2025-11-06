#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decrypto.py — Hilfsskript zum Knacken von Ersetzungs-Ciphern (monoalphabetisch),
inkl. Caesar. Standalone, nur Standardbibliothek.

Funktionen:
- Caesar-Bruteforce (26 Shifts) mit Scoring
- Allgemeiner Substitution-Cipher via Hill-Climbing + Simulated Annealing
- Sprachmodelle: DE/EN (Common-Words + häufige Bi-/Trigramme + Buchstabenhäufigkeit)
- Interaktiver Modus: manuelle Buchstabentauschs (swap A B), Ausgabe des aktuellen Scores
- Ein-/Ausgabe: Datei oder STDIN, Optionen über CLI
"""

import argparse, math, random, re, sys, textwrap
from collections import Counter

# ---------------------------
# Sprachprofile (leichtgewichtig)
# ---------------------------

COMMON_WORDS_DE = {
    # Häufige Funktionswörter & kurze Wörter
    "der","die","das","und","ist","im","in","den","von","zu","mit","sich","des","auf","für",
    "als","auch","ein","eine","er","sie","es","an","am","aus","dem","nicht","ich","du","wir",
    "ihr","mir","mich","dich","sein","sein.","sein,","sind","war","waren","werden","wird",
    "wenn","dann","doch","nur","noch","nur.","aber","oder","weil","wie","was","wer","wo",
    "man","schon","bei","nach","über","bis","ohne","durch","zwischen","gegen","um"
}

COMMON_WORDS_EN = {
    "the","of","and","to","in","is","you","that","it","he","was","for","on","are","as","with",
    "his","they","i","at","be","this","have","from","or","one","had","by","word","but","not",
    "what","all","were","we","when","your","can","said","there","use","an","each","which"
}

# grobe Häufigkeitsreihenfolge (A->Z) – Quelle: allgemein bekannt; für Heuristik ausreichend
FREQ_ORDER_DE = "ENIRSATDHULCGMOBWFKZPVJYQXÄÖÜß".replace("Ä","A").replace("Ö","O").replace("Ü","U").replace("ß","S")
FREQ_ORDER_EN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Häufige Bigramme/Trigramme (kleines Set, gibt Bonuspunkte)
COMMON_BIGRAMS_DE = {
    "ER","EN","CH","DE","EI","IE","ND","GE","TE","IN","UN","ST","SC","AU","NN","NE","SE","BE","RE","AN","AR","IT","AL"
}
COMMON_TRIGRAMS_DE = {
    "DER","SCH","ICH","CHE","UNG","EIN","EER","ION","ENT","GEN","STE","TEN","ERS"
}

COMMON_BIGRAMS_EN = {
    "TH","HE","IN","ER","AN","RE","ON","AT","EN","ND","TI","ES","OR","TE","OF","ED","IS","IT","AL","AR"
}
COMMON_TRIGRAMS_EN = {
    "THE","ING","AND","HER","HAT","HIS","ENT","ION","FOR","THA","NTH","INT","ERE","TER"
}

VOWELS = set("AEIOUY")

# ---------------------------
# Hilfsfunktionen
# ---------------------------

def only_letters(s):
    return re.sub(r'[^A-Za-z]', '', s)

def normalize_text(s):
    # Uppercase und Umlaute vereinfachen (für die Entschlüsselung reicht das)
    s = s.upper()
    s = s.replace("Ä","AE").replace("Ö","OE").replace("Ü","UE").replace("ß","SS")
    return s

def apply_substitution(ciphertext, keymap):
    out = []
    for ch in ciphertext:
        up = ch.upper()
        if 'A' <= up <= 'Z':
            dec = keymap.get(up, up)
            # original casing beibehalten
            out.append(dec if ch.isupper() else dec.lower())
        else:
            out.append(ch)
    return ''.join(out)

def caesar_shift(s, k):
    out = []
    for ch in s:
        up = ch.upper()
        if 'A' <= up <= 'Z':
            idx = ord(up) - 65
            dec = chr((idx - k) % 26 + 65)
            out.append(dec if ch.isupper() else dec.lower())
        else:
            out.append(ch)
    return ''.join(out)

def freq_key_from_text(ciphertext, lang="de"):
    # Basierend auf Häufigkeit: häufigste Chiffre-Buchstaben -> häufigste Sprachbuchstaben
    freq_order = FREQ_ORDER_DE if lang=="de" else FREQ_ORDER_EN
    letters = [c for c in normalize_text(ciphertext) if 'A' <= c <= 'Z']
    cnt = Counter(letters)
    cipher_order = ''.join([p for p,_ in cnt.most_common()]) + ''.join([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in cnt])
    mapping = {}
    for i, cch in enumerate(cipher_order[:26]):
        mapping[cch] = freq_order[i if i < len(freq_order) else -1]
    # invertieren: wir brauchen Chiffre->Klartext
    # mapping ist bereits cipher->plain (cch -> freq_letter)
    return mapping

def random_key():
    plain = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(plain)
    # keymap: Cipher -> Plain (Permutation der 26 Buchstaben)
    return {c: p for c,p in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", plain)}

def key_to_string(keymap):
    # Darstellung: Zeile 1: Cipher; Zeile 2: Plain
    top = "CIPHER: " + " ".join(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    bot = "PLAIN : " + " ".join([keymap[c] for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    return top + "\n" + bot

def swap_in_key(keymap, a, b):
    # swap zugewiesene Plainbuchstaben der beiden Cipherbuchstaben a,b
    inv = invert_key(keymap)
    pa = keymap[a]; pb = keymap[b]
    keymap[a], keymap[b] = pb, pa
    # Konsistenz ok, da 1-zu-1
    return keymap

def invert_key(keymap):
    return {v:k for k,v in keymap.items()}

# ---------------------------
# Scoring
# ---------------------------

def score_text(text, lang="de"):
    """ Kombinierter Heuristik-Score: höher ist besser. """
    t = normalize_text(text)
    words = re.findall(r'[A-Z]{2,}', t)
    if lang == "de":
        cw = COMMON_WORDS_DE
        big = COMMON_BIGRAMS_DE
        tri = COMMON_TRIGRAMS_DE
        freq_order = FREQ_ORDER_DE
    else:
        cw = COMMON_WORDS_EN
        big = COMMON_BIGRAMS_EN
        tri = COMMON_TRIGRAMS_EN
        freq_order = FREQ_ORDER_EN

    score = 0.0

    # 1) Treffer bei häufigen Wörtern (logarithmisch)
    if words:
        hits = sum(1 for w in words if w.lower() in cw)
        score += math.log(1 + hits) * 20

    # 2) Bigram-/Trigram-Boni
    big_hits = 0
    tri_hits = 0
    for i in range(len(t)-1):
        bg = t[i:i+2]
        if bg.isalpha() and bg in big:
            big_hits += 1
    for i in range(len(t)-2):
        tg = t[i:i+3]
        if tg.isalpha() and tg in tri:
            tri_hits += 1
    score += big_hits * 1.5 + tri_hits * 3.0

    # 3) Buchstabenfrequenz-Übereinstimmung (Spearman-Rho ähnlicher Ansatz)
    letters = [c for c in t if 'A' <= c <= 'Z']
    if len(letters) >= 50:
        cnt = Counter(letters)
        # Rangpositionen der 10 häufigsten im Text vs. Sprachprofil
        common_text = ''.join([p for p,_ in cnt.most_common(10)])
        # Bonus wenn die häufigsten Textbuchstaben auch in den Top-Regionen des freq_order liegen
        for i, ch in enumerate(common_text):
            pos = freq_order.find(ch)
            if pos >= 0:
                score += max(0, (26 - pos)) * 0.15  # je früher im freq_order, desto mehr Punkte

    # 4) Weiche Strafpunkte für seltsame Muster
    # zu viele Einzelkonsonanten oder fast keine Vokale -> Strafe
    if letters:
        vowel_ratio = sum(1 for c in letters if c in VOWELS) / len(letters)
        if vowel_ratio < 0.25:  # ungewöhnlich wenig Vokale
            score -= (0.25 - vowel_ratio) * 100
        if vowel_ratio > 0.55:  # zu viele Vokale
            score -= (vowel_ratio - 0.55) * 50

    # Q ohne U (Deutsch/Englisch)
    score -= len(re.findall(r'Q(?!U)', t)) * 2.0

    return score

# ---------------------------
# Caesar
# ---------------------------

def caesar_bruteforce(ciphertext, lang="de"):
    best = None
    candidates = []
    for k in range(26):
        pt = caesar_shift(ciphertext, k)
        s = score_text(pt, lang)
        candidates.append((s, k, pt))
        if best is None or s > best[0]:
            best = (s, k, pt)
    candidates.sort(reverse=True, key=lambda x: x[0])
    return best, candidates[:5]

# ---------------------------
# Substitution via Hill-Climbing + SA
# ---------------------------

def neighbor_key(keymap):
    a, b = random.sample(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 2)
    newk = dict(keymap)
    newk[a], newk[b] = newk[b], newk[a]
    return newk

def solve_substitution(ciphertext, lang="de", iterations=5000, restarts=15, seed_freq=True, verbose=False):
    best_global = None
    rng = random.Random(42)

    for r in range(restarts):
        if seed_freq:
            key = freq_key_from_text(ciphertext, lang)
            # auffüllen/verwürfeln: sicherstellen, dass eine Permutation vorliegt
            used = set(key.values())
            left_plain = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in used]
            rnd_map = {c:p for c,p in zip([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in key], left_plain)}
            key.update(rnd_map)
        else:
            key = random_key()

        temp = 5.0
        cooling = 0.9993

        best_local = None
        cur_key = dict(key)
        cur_plain = apply_substitution(ciphertext, cur_key)
        cur_score = score_text(cur_plain, lang)
        best_local = (cur_score, cur_key, cur_plain)

        for i in range(iterations):
            cand_key = neighbor_key(cur_key)
            cand_plain = apply_substitution(ciphertext, cand_key)
            cand_score = score_text(cand_plain, lang)

            if cand_score > cur_score:
                cur_key, cur_plain, cur_score = cand_key, cand_plain, cand_score
                if cand_score > best_local[0]:
                    best_local = (cand_score, cand_key, cand_plain)
            else:
                # SA-Akzeptanz
                if rng.random() < math.exp((cand_score - cur_score) / max(1e-6, temp)):
                    cur_key, cur_plain, cur_score = cand_key, cand_plain, cand_score

            temp *= cooling
            if verbose and (i % 1000 == 0 or i == iterations-1):
                print(f"[Restart {r+1}/{restarts}] iter={i+1} temp={temp:.3f} score={cur_score:.2f}")

        if best_global is None or best_local[0] > best_global[0]:
            best_global = best_local

    final_score, final_key, final_plain = best_global
    return final_score, final_key, final_plain

# ---------------------------
# Interaktiver Modus
# ---------------------------

def interactive_loop(ciphertext, lang, init_key):
    key = dict(init_key)
    while True:
        plain = apply_substitution(ciphertext, key)
        s = score_text(plain, lang)
        print("\nAktueller Score:", f"{s:.2f}")
        print(key_to_string(key))
        print("\n--- Vorschau ---")
        print(textwrap.fill(plain, 100))
        print("\nBefehle: 'swap A B' | 'show' | 'score' | 'quit'")
        cmd = input("> ").strip().upper()
        if cmd == "QUIT":
            break
        elif cmd == "SHOW":
            continue
        elif cmd == "SCORE":
            print("Score:", s)
        elif cmd.startswith("SWAP "):
            parts = cmd.split()
            if len(parts) == 3 and len(parts[1]) == 1 and len(parts[2]) == 1:
                a, b = parts[1], parts[2]
                if a in key and b in key:
                    key = swap_in_key(key, a, b)
                else:
                    print("Ungültige Buchstaben.")
            else:
                print("Nutzung: swap A B")
        else:
            print("Unbekannter Befehl.")

# ---------------------------
# CLI
# ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Ersetzungs-/Substitutions-Cipher knacken (DE/EN).")
    ap.add_argument("-i","--input", help="Pfad zur Eingabedatei (sonst STDIN).")
    ap.add_argument("-o","--output", help="Pfad für Ausgabe des besten Klartexts (optional).")
    ap.add_argument("-l","--lang", choices=["de","en"], default="de", help="Sprache für Scoring (Default: de).")
    ap.add_argument("-m","--mode", choices=["auto","caesar","subst"], default="auto", help="Modus (auto/caesar/subst).")
    ap.add_argument("--iterations", type=int, default=6000, help="Iterationen pro Restart (Subst).")
    ap.add_argument("--restarts", type=int, default=20, help="Restarts (Subst).")
    ap.add_argument("--no-seed", action="store_true", help="Kein Frequenz-Seed (zufälliger Startschlüssel).")
    ap.add_argument("--interactive", action="store_true", help="Interaktiver Nachbearbeitungsmodus.")
    ap.add_argument("--top", type=int, default=5, help="Top-N Kandidaten bei Caesar anzeigen.")
    args = ap.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            ciphertext = f.read()
    else:
        ciphertext = sys.stdin.read()

    if not ciphertext.strip():
        print("Keine Eingabe erkannt.")
        sys.exit(1)

    if args.mode in ("auto","caesar"):
        best_c, top = caesar_bruteforce(ciphertext, lang=args.lang)
        best_c_score, best_c_k, best_c_plain = best_c
    else:
        best_c = None

    if args.mode == "caesar":
        print(f"[CAESAR] Bester Shift: {best_c_k} | Score: {best_c_score:.2f}\n")
        print(textwrap.fill(best_c_plain, 100))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(best_c_plain)
        sys.exit(0)

    # Substitution ausprobieren
    best_s_score, best_s_key, best_s_plain = solve_substitution(
        ciphertext, lang=args.lang,
        iterations=args.iterations, restarts=args.restarts,
        seed_freq=not args.no_seed, verbose=False
    )

    # AUTO: wähle das bessere Ergebnis aus Caesar vs. Subst
    if args.mode == "auto":
        cand = [("caesar", best_c_score, None, best_c_plain),
                ("subst",  best_s_score, best_s_key, best_s_plain)]
        cand.sort(key=lambda x: x[1], reverse=True)
        mode, score, key, plain = cand[0]
        if mode == "caesar":
            print(f"[AUTO] Gewählt: CAESAR (Shift {best_c_k}) | Score: {score:.2f}\n")
            print(textwrap.fill(plain, 100))
        else:
            print(f"[AUTO] Gewählt: SUBSTITUTION | Score: {score:.2f}\n")
            print(key_to_string(key))
            print("\n--- Klartext ---")
            print(textwrap.fill(plain, 100))
            if args.interactive:
                interactive_loop(ciphertext, args.lang, key)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(plain)
        # bei Caesar Top-N zeigen
        print("\n[CAESAR Top-Kandidaten]")
        for s, k, pt in top[:args.top]:
            print(f"Shift {k:2d} | Score {s:7.2f} | Vorschau: {pt[:60].replace('\\n',' ')}")
        return

    # Explizit SUBST
    print(f"[SUBSTITUTION] Score: {best_s_score:.2f}\n")
    print(key_to_string(best_s_key))
    print("\n--- Klartext ---")
    print(textwrap.fill(best_s_plain, 100))
    if args.interactive:
        interactive_loop(ciphertext, args.lang, best_s_key)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(best_s_plain)

if __name__ == "__main__":
    main()
