"""Text pre-processing / mapping layer, run on every segment before it is sent to ElevenLabs.

Replaces Islamic honorific symbols (ﷺ, ؑ, ؓ, ...) with the fully written words and removes
characters a voice should not try to read: footnote markers, Quranic pause marks, ornate
brackets, decorative quotes and tatweel.
"""
import re

# symbol -> spoken words, chosen by the language of the segment the symbol appears in.
# Note: ؓ is printed for anhu / anha / anhum alike. Where the person is female or plural,
# type the full words in the page text instead of the symbol.
HONORIFICS = {
    "ﷺ": {"ur": "صلی اللہ علیہ وسلم", "ar": "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ", "en": "Sallallahu Alayhi Wasallam"},  # ﷺ
    "ؐ": {"ur": "صلی اللہ علیہ وسلم", "ar": "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ", "en": "Sallallahu Alayhi Wasallam"},  # ؐ
    "ﷻ": {"ur": "جل جلالہ", "ar": "جَلَّ جَلَالُهُ", "en": "Jalla Jalaluhu"},  # ﷻ
    "﷾": {"ur": "سبحانہ و تعالیٰ", "ar": "سُبْحَانَهُ وَتَعَالَى", "en": "Subhanahu wa Ta'ala"},  # ﷾
    "﷿": {"ur": "عزوجل", "ar": "عَزَّ وَجَلَّ", "en": "Azza wa Jal"},  # ﷿
    "ؑ": {"ur": "علیہ السلام", "ar": "عَلَيْهِ السَّلَامُ", "en": "Alayhis Salam"},  # ؑ
    "ؒ": {"ur": "رحمۃ اللہ علیہ", "ar": "رَحْمَةُ اللَّهِ عَلَيْهِ", "en": "Rahmatullah Alayh"},  # ؒ
    "ؓ": {"ur": "رضی اللہ عنہ", "ar": "رَضِيَ اللَّهُ عَنْهُ", "en": "Radiyallahu Anhu"},  # ؓ
    "﷽": {"ur": "بسم اللہ الرحمن الرحیم", "ar": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "en": "Bismillahir Rahmanir Raheem"},  # ﷽
    "ﷲ": {"ur": "اللہ", "ar": "الله", "en": "Allah"},  # ﷲ
    "ﷴ": {"ur": "محمد", "ar": "مُحَمَّد", "en": "Muhammad"},  # ﷴ
}

# End-of-ayah sign ۝ together with the ayah number written inside it.
AYAH_END = re.compile(r"۝[0-9٠-٩۰-۹]*")

REMOVE = re.compile(
    "["
    "﴾﴿"          # ornate brackets ﴾ ﴿
    "ۖ-ۜ"         # Quranic pause marks (waqf signs)
    "۞۩"          # rub el hizb ۞, sajdah sign ۩
    "ؔ؎؏"    # takhallus, poetic verse signs
    "ـ"                # tatweel
    "①-⑳⓪"   # circled footnote numbers ① ... ⑳
    "❶-➓"         # dingbat circled numbers ❶ ...
    "¹²³⁰-⁹"  # superscript footnote numbers
    "“”„«»\""  # decorative quotes “ ” „ « » "
    "]"
)

# Arabic code points that Urdu text typed on Arabic keyboards often contains.
URDU_LETTERS = str.maketrans({"ك": "ک", "ي": "ی", "ى": "ی", "ه": "ہ"})


def preprocess(text, lang="ur"):
    """Return `text` ready for TTS in `lang` ("ur", "ar" or "en")."""
    for symbol, spoken in HONORIFICS.items():
        # symbols like ؓ are joined straight onto the name ("عمرؓ"), so pad with spaces
        text = text.replace(symbol, f" {spoken[lang]} ")
    text = AYAH_END.sub(" ", text)
    text = REMOVE.sub("", text)
    if lang == "ur":
        text = text.translate(URDU_LETTERS)
    text = text.replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()
