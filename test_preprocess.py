import unittest

from preprocess import preprocess


class PreprocessTest(unittest.TestCase):
    def test_durood_urdu(self):
        self.assertEqual(preprocess("محمد ﷺ نے فرمایا"), "محمد صلی اللہ علیہ وسلم نے فرمایا")

    def test_durood_english(self):
        self.assertEqual(preprocess("Muhammad ﷺ said", "en"), "Muhammad Sallallahu Alayhi Wasallam said")

    def test_symbol_joined_to_name(self):
        self.assertEqual(preprocess("حضرت عمرؓ اور حضرت موسیٰؑ"), "حضرت عمر رضی اللہ عنہ اور حضرت موسیٰ علیہ السلام")

    def test_page_001_urdu(self):
        raw = "”بلاشبہ یقیناً ہم نے اپنے رسول بھیجے اور لوگ انصاف پر قائم رہیں۔“ ①"
        self.assertEqual(preprocess(raw), "بلاشبہ یقیناً ہم نے اپنے رسول بھیجے اور لوگ انصاف پر قائم رہیں۔")

    def test_arabic_keeps_harakat_and_letters(self):
        raw = "﴿لَقَدْ أَرْسَلْنَا مَعَهُمُ الْكِتَابَ﴾"
        self.assertEqual(preprocess(raw, "ar"), "لَقَدْ أَرْسَلْنَا مَعَهُمُ الْكِتَابَ")

    def test_quranic_marks_removed(self):
        self.assertEqual(preprocess("لَا رَيْبَ ۛ فِيهِ ۛ هُدًى ۝٢", "ar"), "لَا رَيْبَ فِيهِ هُدًى")

    def test_urdu_letters_normalised(self):
        self.assertEqual(preprocess("كتاب يہ الله"), "کتاب یہ اللہ")


if __name__ == "__main__":
    unittest.main()
