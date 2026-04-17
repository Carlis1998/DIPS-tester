# DIPS NotebookLM Production Spec

Det här är den praktiska NotebookLM-produktionsdelen för DIPS-Tester.

Mål:
- producera djupa, tydliga spanska audio overviews för DIPS-förberedelse
- använda små, hårt kurerade källpaket
- undvika gloslistor, överstyrda prompts och onödig token-spill

Grundprinciper:
- 4–7 källor per notebook
- primärkällor först
- en fast master prompt för alla avsnitt
- en kort ämnesbrief per notebook
- fokus på analys, kronologi, institutioner, rättsliga distinktioner och provrelevans
- ingen separat vocabulary training

Körordning:
1. Svensk utrikespolitik och Utrikesdeklarationen 2026
2. FN-systemet och FN-stadgan
3. EU:s institutioner och von der Leyen II-kommissionen
4. NATO och Sveriges medlemskap
5. Wienkonventionerna och diplomatisk praktik
6. Ukraina 2022–2026
7. Mellanöstern: Gaza, Iran, Libanon, Syrien efter Assad
8. Regeringen Kristersson och svensk politik 2022–2026
9. Trump II och den transatlantiska relationen
10. Folkrätt: ICJ, ICC, Europadomstolen och CJEU

Arbetsgång per notebook:
1. skapa en notebook
2. ladda upp 4–7 källor i den ordning som packet-filen anger
3. klistra in master prompt + ämnesbrief i Customize
4. sätt output-språk till spanska i NotebookLM
5. generera audio overview
6. kvalitetskontrollera de första 2–3 minuterna

Lyssna efter:
- naturlig spanska
- snabb och tydlig ämnesöppning
- verklig analys i stället för gloslista
- god struktur och upprepning av viktiga skillnader

Om output blir svag:
- justera först master prompten, inte ämnesbriefen
- minska antal källor om notebooken blivit för bred
- ta bort sekundärkällor som ger brus
