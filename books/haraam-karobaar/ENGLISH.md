# English edition of *100 Haraam Karobaar aur Tijarti Mamlaat*

How to write the English edition. It follows the Urdu edition page for page, as in [PIPELINE.md](../../PIPELINE.md) step 4: for every Urdu page `page_NNN.txt` you write `en_src/page_NNN.txt`, and `build_english.py` joins it with the Urdu page's Arabic and references into `en/page_NNN.txt`.

English title: **100 Forbidden Trades and Business Dealings**.

## The file

`en_src/page_NNN.txt` holds only English blocks:

- one `[en]` block for every `[ur]` block of the Urdu page,
- one `[hen]` block for every `[h]` block,
- in the same order, and nothing else (no `[ar]`, no `[ref]`: those are copied from the Urdu page by the build).

Start it with one comment line: `# English source for book page NNN`. A page whose Urdu file has no `[ur]` or `[h]` block gets a file with only that comment line. If the Urdu page has no file at all (a blank page), write nothing.

Check each page with:

```bash
python3 build_english.py NNN-NNN --book haraam-karobaar --parens      # stops if the blocks don't match the Urdu page
python3 check_pages.py books/haraam-karobaar/en/page_NNN.txt  # must report 0 problems
```

## Translating

- **Translate the Urdu page's meaning completely and faithfully**, sentence by sentence: nothing added, nothing left out, nothing summarised. A block's English must say what that block's Urdu says.
- Plain, natural modern English, as a careful translator would write it for an English reader. Keep the book's tone: a teacher speaking warmly but firmly to his student.
- The Urdu text is final and proofread. Translate the Urdu as it stands. If the Urdu page's header logs a print error that was corrected, translate the corrected text.
- Keep the book's own structure: dialogue turns stay dialogue turns, lists stay lists, headings stay headings.
- **The hadith translations** in `[ur]` blocks are the book's own translations: translate them as they are, in quotation marks “...” where the Urdu has them.

## Speakers and dialogue

Each Urdu dialogue turn «عمار: ...» becomes `Ammar: ...`, with the speaker's English name from the glossary below and a colon. A block with only a name (before an Arabic quote) becomes just `Teacher:`. When the teacher is addressed as «استاد صاحب!» or «شیخ!» in speech, write «Teacher!» or «Shaykh!» as the Urdu has it. A label followed by narration («عمار: مسکراتے ہوئے بولا: ...») stays as printed: "Ammar: Smiling, he said: ...".

## Quran

- **The verse's own translation** (the `[ur]` block that translates an `[ar]` verse) is never our own wording. If the Urdu block translates whole ayat, write `{{QEN 2:208}}` (several ayat: `{{QEN 83:1 83:2 83:3}}`) as the whole block, and Sahih International is filled in by the build. The verse numbers are in the Urdu page's `# quran` comments.
- If it translates only part of an ayah, copy the matching words of Sahih International exactly. You may capitalise its first letter and end it with a full stop where Sahih's text continues, and write it without quote marks, like the `{{QEN}}` blocks. Sahih's added words stay in parentheses, as the command above prints them («and do not follow the footsteps of Satan (i.e., his ways)»). See the full text with `python3 -c "import build_english as b; b.PARENS = True; print(b.sahih('2:208'))"`.
- A verse quoted inside an Urdu sentence is handled the same way: use Sahih International's words for that part.

## Honorifics

As in the first book's English edition:

| Urdu | English |
|---|---|
| ﷺ / صلی اللہ علیہ وسلم | peace be upon him |
| رضی اللہ عنہ / عنہا / عنہما / عنہم | may Allah be pleased with him / her / them (both) / them |
| رحمہ اللہ / رحمۃ اللہ علیہ / رحمہم اللہ | may Allah have mercy on him / them |
| علیہ السلام | peace be upon him |
| اللہ تعالیٰ | Allah, or Allah the Exalted where the Urdu stresses it |

Write them out in words; never use symbols.

## Glossary (use exactly these)

**People.** استاد: Teacher (as a speaker label; "the teacher" in narration) · عمار: Ammar · شیخ: Shaykh · دکاندار: Shopkeeper · آدمی: Man · نوجوان: Young man · خریدار: Buyer · بائع: Seller · تاجر: Trader · گاہک: Customer · مدیر: Manager · ڈرائیور: Driver · حجام: Barber · مزدور: Worker · چوکیدار: Watchman · لڑکا: Boy · بچہ: Child · غریب: Poor man (but in chapter three, pages 52–59, غریب is a farmer's name: Gharib) · سب لوگ: Everyone · فیصل: Faisal · بھنسی: Bahnasi · حسین: Husain · سالم: Salim · ابو جمعہ: Abu Jum'a · سعد: Sa'd · مصطفیٰ: Mustafa · عبدالرحیم: Abdur-Rahim · محمد: Muhammad · حسن: Hasan · ابوعلی: Abu Ali · ابوفارس: Abu Faris · صلاح: Salah · احمد: Ahmad · عاطف: Atif · عبید: Ubaid · عطیہ: Atiyyah · زید: Zaid · ہیثم: Haitham · لطفی: Lutfi · عبدالخالق: Abdul-Khaliq · ابوشوقی: Abu Shawqi · محمود: Mahmud · کمال: Kamal · حسان: Hassan · منتصر: Muntasir · ابوفہد: Abu Fahd · عباس: Abbas · فوزی: Fawzi · طلعت: Tal'at · عبدالوہاب: Abdul-Wahhab · خدیجہ: Khadijah · حسام: Husam · علی: Ali · جابر: Jabir · عصام: Isam · عیاد: Ayyad · ابوراشد: Abu Rashid · ابوخالد: Abu Khalid · مخیمر: Mukhaimir · خالد: Khalid · حمدان: Hamdan · عبدالجواد: Abdul-Jawwad. For a name not listed, use the usual English spelling of the Arabic name, without diacritics, and keep it the same everywhere it appears in your pages.

**Companions and scholars.** Abu Hurairah · Abdullah ibn Umar · Abdullah ibn Abbas · Anas ibn Malik · Aishah · Jabir ibn Abdullah · Abu Sa'id al-Khudri · Imam an-Nawawi · Ibn Hajar · Ibn Baz · Ibn Uthaymeen · Ibn Qudamah · Shaykh al-Albani.

**Headings.**
- `پہلا باب: ناپ تول میں کمی کرنا` → `Chapter One: Giving Short Measure and Weight`. Chapter numbers are written in words: Chapter One ... Chapter One Hundred.
- `پہلا دورہ` → `The First Tour`; `غلہ منڈی کا دورہ` → `The Grain Market Tour` (each smaller tour named after its place).
- `خلاصہ` → `Summary`; `عرضِ ناشر` → `Publisher's Note`; `مقدمہ` → `Introduction`.

**Terms.** حرام: forbidden · حلال / جائز: lawful / permissible · ناجائز: impermissible · سود: interest (riba) on its first mention in a chapter, then interest · بیع: sale · شریعت: the Shariah · سنت: the Sunnah · حدیث: hadith (plural hadiths) · صحابہ: the Companions · سلف: the early generations · شراب / خمر: alcohol (only Sahih International's own words in a verse keep its "wine" or "intoxicants") · صحابہ کرام: the noble Companions · روپے: rupees · پاؤنڈ: pounds · کلو: kilos · دورہ (a visit to a market): tour.

**More people and places.** صالح (the teacher's name): Salih, «استاد صالح» Teacher Salih · کلرک: Clerk · Hajji Farid Abu Jum'a · Umm Muhammad · Umar ibn al-Khattab · Ibn Taymiyyah · Ibn al-Qayyim · Ahmad ibn Hanbal · ash-Shafi'i · Madinah · Makkah · Lahore · صرافہ بازار: the Gold Market · کرنسی مارکیٹ: the Currency Market · منڈی مویشیاں: the Livestock Market · کرنل چاول / سپر چاول: Kernel rice / Super rice.

**Set phrases** (always these forms): ان شاء اللہ: in sha Allah · ما شاء اللہ: ma sha Allah · الحمد للہ: praise be to Allah · سبحان اللہ: glory be to Allah · اللہ اکبر: Allah is the Greatest · جزاک اللہ (خیراً): may Allah reward you (with good) · بارک اللہ فیک: may Allah bless you · استغفر اللہ: I seek Allah's forgiveness · لا حول ولا قوۃ الا باللہ: there is no might and no power except with Allah · نعوذ باللہ: we seek refuge in Allah · انا للہ و انا الیہ راجعون: to Allah we belong and to Him we return · لا الہ الا اللہ: there is no god but Allah · اللہ کا شکر ہے: thanks be to Allah · قرآن مجید / قرآن کریم: the Noble Quran · آمین: Amin · السلام علیکم ورحمۃ اللہ: As-salamu alaikum wa rahmatullah · with وبرکاتہ: As-salamu alaikum wa rahmatullahi wa barakatuh · the replies: Wa alaikum as-salam wa rahmatullah(i wa barakatuh).

**Titles and address.** حضرت / سیدنا / سیدہ before a name: left out ("Anas", "Aishah") · نبی اکرم / نبی کریم / نبی مکرم: the noble Prophet · رسول اللہ: the Messenger of Allah · استاد صاحب / شیخ صاحب in address: Teacher / Shaykh · a name + صاحب, in address and in narration: just the name ("Salim!", "Is Mustafa here?"; never "Mr") · نبی اقدس: the blessed Prophet · علامہ: the great scholar · امام: Imam · مولانا: Maulana · حاجی: Hajji · حضرت صاحب: Sir · name + بھائی: Brother + name ("Brother Bahnasi") · بھائی جان: Brother · یار: my friend.

**Headings.** A summary: `Summary of the Grain Market Tour` (the tour's name as in its title). A tour title that has no «کا دورہ» is translated as it stands (`The Livestock Market`). «(riba)» goes with the first mention of interest in a chapter, which may be its heading.

**Spelling.** British spelling (jewellery, instalments, behaviour, café), as in the first book; «(riba)» is lower case, also in headings; Sahih International's text keeps its own spelling.

## Numbers, lists and punctuation

- Numbers may be written as digits or words in English, whichever reads naturally («پچاس روپے» → "fifty rupees").
- Ordinal list items «پہلی: ...» → `First: ...`, «دوسری:» → `Second: ...`.
- Use “ ” for quotations and ’ or ' for apostrophes as normal English. No «» or Arabic punctuation.
- Arabic terms the Urdu keeps inside a sentence (`بَيْعُ الْمُصَرَّاةِ`) are written in English transliteration and explained the way the Urdu explains them: "bay' al-musarrat (selling an animal whose milk has been held back)". When the Urdu leaves the Arabic unexplained (an Urdu reader understands it, an English listener would not), add its short meaning in brackets: "yastahillun (they will make lawful)".
- Headings use title case, with short words such as a, the, and, of, in, on, for, to, among and with in lower case unless they come first («Forbidden Things Found among Office Employees», «Chapter Fifty-One: Buying, Selling and Repairing Televisions»). Doubled «!!» / «؟؟» become one mark.

## Before a page is done

Read the English block by block against the Urdu once more: every sentence there, the meaning right, the names and terms from the glossary. Then build and check it as above.
