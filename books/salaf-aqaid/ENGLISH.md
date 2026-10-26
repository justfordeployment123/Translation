# English edition of *Salaf-e-Saliheen ke Aqaid o Nazariyat*

How to write the English edition. It follows the Urdu edition page for page, as in [PIPELINE.md](../../PIPELINE.md) step 4: for every Urdu page `page_NNN.txt` you write `en_src/page_NNN.txt`, and `build_english.py` joins it with the Urdu page's Arabic and references into `en/page_NNN.txt`.

English title: **The Beliefs and Doctrines of the Righteous Predecessors**. The book is the Urdu edition of Shaykh Abdullah ibn Abd al-Hamid al-Athari's *al-Wajiz fi Aqidat as-Salaf as-Salih*: the creed of Ahl as-Sunnah wal-Jama'ah, set out principle by principle with Quran and hadith.

## The file

`en_src/page_NNN.txt` holds only English blocks:

- one `[en]` block for every `[ur]` block of the Urdu page,
- one `[hen]` block for every `[h]` block,
- one `[fen]` block for every `[fn]` block (an explanatory footnote or a signature),
- in the same order, and nothing else (no `[ar]`, no `[ref]`: those are copied from the Urdu page by the build).

Start it with one comment line: `# English source for book page NNN`. A page whose Urdu file has no `[ur]`, `[h]` or `[fn]` block gets a file with only that comment line. If the Urdu page has no file at all, write nothing.

Check each page with:

```bash
python3 build_english.py NNN-NNN --book salaf-aqaid --parens      # stops if the blocks don't match the Urdu page
python3 check_pages.py books/salaf-aqaid/en/page_NNN.txt         # must report 0 problems
```

## Translating

- **Translate the Urdu page's meaning completely and faithfully**, sentence by sentence: nothing added, nothing left out, nothing summarised. A block's English must say what that block's Urdu says.
- Plain, natural modern English, as a careful translator would write it for an English reader. Keep the book's tone: a measured, scholarly statement of creed, precise in its terms.
- The Urdu text is final and proofread. Translate the Urdu as it stands. If the Urdu page's header logs a print error that was corrected, translate the corrected text.
- Keep the book's own structure: lists stay lists, headings stay headings, a bold lead-in that opens a paragraph («ایمان بالملائکہ (فرشتوں پر ایمان لانا):») opens the English paragraph the same way.
- **The hadith translations** in `[ur]` blocks are the book's own translations: translate them as they are, in quotation marks “...” where the Urdu has them.
- **Precision matters in this book.** Creed terms are defined carefully and the same term must always get the same English (glossary below). Keep every qualification («بعض», «اکثر», «بلا کیف») and every negation exactly.

## Footnotes (`[fen]`)

- Each `[fn]` block is translated in full in its `[fen]` block, like any other text. It is shown with the page and not spoken.
- A Quran verse filled inside an `[fn]` block (a `# quran` line inside it) becomes `{{QEN s:a}}` at that point of the `[fen]` block, followed by its printed reference in English: `... Allah the Exalted says: {{QEN 36:82}} (Ya-Sin 36:82)`. The verse's printed Urdu translation is then not translated again.
- A reference inside the footnote's text is written in English with the verse number in the usual order: «(البقرة 255:2)» → "(al-Baqarah 2:255)".
- A signature (`[fn]` under the publisher's note, the foreword and the author's introduction) is translated as a signature: "Hoping for the mercy of the Most Forgiving Lord, Abu Muhammad Abdullah ibn Abd al-Hamid Al Isma'il al-Athari, resident of Istanbul, Dhu al-Hijjah 1416 AH".

## Quran

- **The verse's own translation** (the `[ur]` block that translates an `[ar]` verse) is never our own wording. If the Urdu block translates whole ayat, write `{{QEN 2:208}}` (several ayat: `{{QEN 10:62 10:63 10:64}}`) as the whole block, and Sahih International is filled in by the build. The verse numbers are in the Urdu page's `# quran` comments.
- If it translates only part of an ayah, copy the matching words of Sahih International exactly. You may capitalise its first letter and end it with a full stop where Sahih's text continues, and write it without quote marks, like the `{{QEN}}` blocks. Sahih's added words stay in parentheses, as the command below prints them. See the full text with `python3 -c "import build_english as b; b.PARENS = True; print(b.sahih('2:208'))"`.
- A verse quoted inside an Urdu sentence is handled the same way: use Sahih International's words for that part.
- Page 118: the Arabic filled is the end of 9:115 (the print's verse was corrected); its translation is Sahih's words for that part.

## Honorifics

As in the earlier English editions:

| Urdu | English |
|---|---|
| ﷺ / صلی اللہ علیہ وسلم | peace be upon him |
| رضی اللہ عنہ / عنہا / عنہما / عنہم | may Allah be pleased with him / her / them (both) / them |
| رضوان اللہ علیہم اجمعین | may Allah be pleased with them all |
| رحمہ اللہ / رحمۃ اللہ علیہ / رحمہم اللہ | may Allah have mercy on him / them |
| علیہ السلام | peace be upon him |
| علیہ الصلوٰۃ والسلام | peace and blessings be upon him |
| اللہ تعالیٰ | Allah, or Allah the Exalted where the Urdu stresses it |
| سبحانہ وتعالیٰ | Glorified and Exalted is He |
| عز وجل | the Mighty and Majestic |

Write them out in words; never use symbols.

## Glossary (use exactly these)

**The book's own terms.**
- سلف صالحین: the Righteous Predecessors · سلف: the Salaf · سلفی: Salafi · سلفیت / سلفیہ: Salafiyyah
- اہل سنت والجماعت: Ahl as-Sunnah wal-Jama'ah · اہل حدیث / اصحاب الحدیث: the people of hadith · فرقہ ناجیہ: the saved sect · طائفہ منصورہ: the victorious group
- عقیدہ: creed · عقائد: beliefs · اصول (one of the book's principles): principle · منہج: methodology
- ایمان: faith · ارکانِ ایمان: the pillars of faith · ایمان باللہ: faith in Allah · ایمان بالملائکہ: faith in the angels · ایمان بالکتب: faith in the Books · ایمان بالرسل: faith in the Messengers · ایمان بالیوم الآخر: faith in the Last Day · ایمان بالقدر / تقدیر: faith in the divine decree · قدر / تقدیر: the divine decree · مرتبہ (of the decree): level · مشیت: will · لوحِ محفوظ: the Preserved Tablet
- توحید: Tawhid · توحید ربوبیت: the Oneness of Lordship (Tawhid ar-Rububiyyah) · توحید الوہیت: the Oneness of worship (Tawhid al-Uluhiyyah) · اسماء و صفات: the Names and Attributes · صفات: attributes · استوا: rising over (istiwa') · عرش: the Throne · کرسی: the Footstool · نزول: descent
- شرک: shirk (associating partners with Allah) on its first mention in a principle, then shirk · کفر: disbelief · کافر: disbeliever · کفرِ اکبر / اصغر: major / minor disbelief · نفاق: hypocrisy · منافق: hypocrite · نفاقِ اعتقاد / عمل: hypocrisy of belief / of action · تکفیر: declaring someone a disbeliever (takfir) on its first mention in a principle, then takfir · ارتداد / مرتد: apostasy / apostate
- بدعت: innovation · اہل بدعت / بدعتی: the people of innovation / an innovator · سنت: the Sunnah · شریعت: the Shariah · حدیث: hadith (plural hadiths) · قرآن مجید / قرآن کریم: the Noble Quran · کتاب و سنت: the Quran and the Sunnah
- وعدہ وعید: the promises and the warnings · دوستی اور دشمنی (الولاء والبراء): loyalty and disavowal · ولی / اولیاء / اولیاء اللہ: friend / friends of Allah · کرامت / کرامات: karamah / karamat (wonders granted to the friends of Allah) on the first mention in the sixth principle, then karamah / karamat · معجزہ: miracle · استدراج: istidraj (being given respite and led on step by step), as the Urdu explains it
- شفاعت: intercession · مقامِ محمود: the Praiseworthy Station · میدانِ محشر: the plain of gathering · حوض: the Pond · پل صراط / صراط: the Bridge (as-Sirat) · میزان: the Scale · اعمال نامہ: record of deeds · عذابِ قبر: the punishment of the grave · جنت / جہنم: Paradise / Hell · دجال: the Dajjal · یاجوج ماجوج: Gog and Magog
- تقلید: taqlid (following an opinion without its evidence) on its first mention, then taqlid · مقلد: follower (muqallid) · اجتہاد / مجتہد: ijtihad / mujtahid · اجماع: consensus (ijma') · قیاس: analogy (qiyas) · دلیل: evidence · استدلال: reasoning from evidence
- حکمران: ruler · امیر / امام (of the Muslims): ruler / imam, as the Urdu means · اطاعت: obedience · خروج / بغاوت: rebellion · خلفائے راشدین: the Rightly Guided Caliphs

**People.** صحابہ: the Companions · صحابہ کرام: the noble Companions · تابعین: the Successors · ائمہ: the imams · Abu Hurairah · Abdullah ibn Mas'ud · Abdullah ibn Umar · Abdullah ibn Abbas · Abdullah ibn Amr · Anas ibn Malik · Aishah · Abu Sa'id al-Khudri · Mu'awiyah · al-Irbad ibn Sariyah · Abu ad-Darda' · Buraydah · Umar ibn al-Khattab · Ali ibn Abi Talib · Imam Malik ibn Anas · Imam Abu Hanifah · Imam ash-Shafi'i · Imam Ahmad ibn Hanbal · al-Awza'i · Sufyan ath-Thawri · al-Humaydi · Ishaq ibn Rahawayh · al-Lalaka'i · al-Baghawi · al-Fudayl ibn Iyad · al-Hasan al-Basri · Ibn Taymiyyah · Ibn al-Qayyim · Ibn Qudamah · Ibn Hajar · Imam an-Nawawi · Shaykh al-Albani · Iblis. The book's people: the author, Shaykh Abdullah ibn Abd al-Hamid al-Athari · the foreword writer, Salih ibn Abd al-Aziz ibn Muhammad Al ash-Shaykh · the publisher, Abdul Malik Mujahid, Darussalam · the translator, Hafiz Qamar Hasan. For a name not listed, use the usual English spelling of the Arabic name, without diacritics, and keep it the same everywhere it appears in your pages.

**Headings.**
- `پہلا اصول: ایمان اور ارکانِ ایمان` → `The First Principle: Faith and the Pillars of Faith`. The principle's number is an ordinal in words: The First Principle ... The Eighth Principle.
- `عرضِ ناشر` → `Publisher's Note`; `پیش لفظ` → `Foreword`; `مقدمہ` → `Introduction`; `ضروری تعریفیں` → `Essential Definitions`.
- Headings use title case, with short words such as a, the, and, of, in, on, for, to, from, among and with in lower case unless they come first.

**Set phrases** (always these forms): ان شاء اللہ: in sha Allah · ما شاء اللہ: ma sha Allah · الحمد للہ: praise be to Allah · سبحان اللہ: glory be to Allah · اللہ اکبر: Allah is the Greatest · جزاک اللہ (خیراً): may Allah reward you (with good) · استغفر اللہ: I seek Allah's forgiveness · نعوذ باللہ: we seek refuge in Allah · انا للہ و انا الیہ راجعون: to Allah we belong and to Him we return · لا الہ الا اللہ: there is no god but Allah · آمین: Amin · واللہ اعلم: and Allah knows best.

**Titles and address.** حضرت / سیدنا / سیدہ before a name: left out ("Anas", "Aishah") · نبی اکرم / نبی کریم / نبی مکرم: the noble Prophet · رسول اللہ / اللہ کے رسول: the Messenger of Allah · رسول اکرم: the noble Messenger · نبی اقدس: the blessed Prophet · شیخ الاسلام: Shaykh al-Islam · علامہ: the great scholar · امام: Imam · حافظ (as a title): Hafiz · مولانا: Maulana.

**Spelling.** British spelling (behaviour, honour, recognise), as in the earlier books. Sahih International's text keeps its own spelling.

## Settled during translation (use these too)

- **Introducing a quotation:** ارشادِ باری تعالیٰ ہے: "Allah the Exalted says:" · ارشادِ الٰہی ہے / ارشادِ ربانی ہے / فرمانِ الٰہی ہے: "Allah says:" · ارشادِ نبوی ہے: "The Prophet said:" · before a verse, اللہ تعالیٰ نے فرمایا / فرمایا: "Allah the Exalted says:" / "He says:" (Allah's words are quoted in the present) · فرمایا (after the Prophet): "he said:".
- **The generations:** صحابہ: the Companions · تابعین: the Successors · تابعین عظام: the eminent Successors · تبع تابعین: the followers of the Successors · اسلاف: the Salaf ("our Salaf"), except where the book discusses the word itself (page 35: "aslaf") · محدثین: the scholars of hadith.
- **Community:** امت / امتِ مسلمہ: the Ummah / the Muslim Ummah · دیگر امتیں: the other nations · جماعت: the Jama'ah · ملت (in the hadith of the seventy-three): sect · اہل قبلہ: the people of the qiblah · موحدین / اہل توحید / توحید پرست: the people of Tawhid · موحد: a believer in Tawhid · مشرکین: the polytheists.
- **Sects:** the Kharijites · the Jahmiyyah · the Qadariyyah · the Mu'tazilah · the Murji'ah · the Rafidah.
- **Tawhid:** توحید اسماء و صفات: the Oneness of the Names and Attributes (Tawhid al-Asma' was-Sifat) · توحیدِ عبادت: the Oneness of worship. The bracketed Arabic name goes with the first mention only (page 62). معبود / معبودِ برحق: deity / the true deity («لا الہ الا اللہ» spelled out: "there is no god but Allah"; «نہیں کوئی معبودِ برحق سوائے اللہ کے»: "there is no true god but Allah").
- **The Names and Attributes:** کیفیت: how ("without asking how") · تاویل: ta'wil (figurative interpretation), and in takfir a mistaken interpretation · تعطیل: ta'til (denial) · تحریف: tahrif (changing their meanings) · تکییف: takyif (describing how they are) · تمثیل / تشبیہ: tamthil / tashbih (likening) · الحاد: ilhad · معیت: ma'iyyah (being with) · اسمائے حسنیٰ: the most beautiful Names · آسمانِ دنیا: the lowest heaven · نقل / عقل: transmission / reason.
- **Disbelief and takfir:** فاسق / فسق: a transgressor (fasiq) on first mention, then transgressor / transgression · معصیت: sin · ناقص الایمان: deficient in faith · نواقضِ ایمان: the nullifiers of faith · شہادتین: the two testimonies · ایمان میں استثنا: the exception in faith · متعین شخص: a specific person · حجت قائم کرنا: establishing the proof · شرائط / موانع: conditions / impediments · کفرِ اعتقادی: creedal disbelief · the kinds of disbelief as "the disbelief of denial", "the disbelief of arrogance with affirmation", "the disbelief of turning away", "the disbelief of hypocrisy", "the disbelief of doubt"; نفاقِ اکبر / اصغر: major / minor hypocrisy · دائرہ اسلام سے خارج: out of the fold of Islam · جھٹلانا: belie · انکار: deny · شارع: the Lawgiver.
- **Other:** فتنہ: tribulation · جاہلیت: Jahiliyyah (ignorance) · فطرت: the natural disposition (fitrah) · شیطان: Satan · عشرہ مبشرہ: the ten who were given the good news of Paradise · ازواج مطہرات: the pure wives · حفظہ اللہ: may Allah preserve him · رسالت مآب: the bearer of the Message · ختمی مرتبت: the Seal of the Prophets · رسولِ کریم: the noble Messenger.
- **The Last Day and the decree:** قیامت: the Hour (its signs: the minor / major signs of the Hour) · روزِ قیامت: the Day of Resurrection · عالمِ برزخ: the Barzakh · صور: the Trumpet · ارادہ: intention, kept apart from مشیت: will · قلم: the Pen · اہل بیت: the Prophet's Household · مہدی: the Mahdi.
- **The Books and Messengers:** توریت / انجیل / زبور: the Torah / the Gospel / the Psalms · صحیفے: the Scrolls · کلام اللہ: the Speech of Allah · حروفِ مقطعات: the disjointed letters · اولو العزم: the Messengers of firm resolve · اسراء و معراج: the Night Journey and the Ascension (al-Isra' wal-Mi'raj) · prophets by their Arabic names: Nuh, Ibrahim, Musa, Isa, Dawud, Sulayman, Yunus ...
- **Sources and rulers:** مسلک: school (madhhab on its first mention) · اتباع: following (ittiba') · مکلف: a legally accountable person · امیر (in hadith): ruler · سمع و طاعت: listening and obeying · اہل حل و عقد: those with authority to appoint and remove (ahl al-hall wal-aqd) · امیر المومنین: the Commander of the Believers · مہاجرین و انصار: the Emigrants and the Helpers. اسلاف is always "the Salaf", never "forebears".
- **Glosses go in parentheses** ( ), never square brackets (the checks reject them).
- **A part of an ayah inside a `[fen]`** is written in Sahih's words for that part, followed by its reference, not `{{QEN}}` (which would insert the whole ayah; page 114).
- **First-mention glosses** (shirk, takfir, karamat, taqlid) go on the first mention in the body text of the principle, not in a heading.
- **Transliteration:** no leading apostrophe for an initial ayn (aqidah, ijtima', uqdah), so the voice does not stumble.
- **Volume and page references** inside a `[fen]`: volume/page, as "8/173".
- **A verse quoted inside a sentence that the Urdu does not translate** (3:106 on page 54, 20:5 on page 81): give Sahih International's words for it in brackets where the English sentence needs them, so an English listener understands it.

## Numbers, lists and punctuation

- Numbers may be written as digits or words in English, whichever reads naturally. Hijri dates: "1416 AH".
- Ordinal list items «پہلی: ...» → `First: ...`, «دوسری:» → `Second: ...`; «پہلی قسم، کفر اکبر:» → `The first kind, major disbelief: ...`; «پہلا مرتبہ، علم:» → `The first level, knowledge: ...`.
- Use “ ” for quotations and ’ or ' for apostrophes as normal English. No «» or Arabic punctuation.
- Arabic terms the Urdu keeps inside a sentence are written in English transliteration and explained the way the Urdu explains them. When the Urdu leaves the Arabic unexplained (an Urdu reader understands it, an English listener would not), add its short meaning in brackets.
- Doubled «!!» / «؟؟» become one mark.

## Before a page is done

Read the English block by block against the Urdu once more: every sentence there, the meaning right, the terms from the glossary. Then build and check it as above.
