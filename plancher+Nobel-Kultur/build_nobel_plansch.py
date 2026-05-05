"""
DIPS 2026 Nobel & Kulturpriser-plansch v1
Bygger en A3-plansch i två sidor som täcker:
  Sida 1: Nobels fredspris + Nobels litteraturpris (senaste 10 åren)
  Sida 2: 10 historiska klassiker (fred + litteratur) + svenska/europeiska/världens kulturpriser

Modellerad på samma stilsystem som plancher+Världsledare/build_plansch_v3.py.
Foton hämtas från photos/{key}.jpg via separat download_nobel_photos.py.
Saknas foto används en gradient-initial-avatar.

Run: python3 build_nobel_plansch.py
Output: DIPS_2026_Nobel_Kultur.pdf
"""
import os
import base64
import weasyprint

PHOTO_DIR = "photos"
OUTPUT_HTML = "plansch_nobel.html"
OUTPUT_PDF = "DIPS_2026_Nobel_Kultur.pdf"

# Färgpalett för regioner / kategorier
REGION = {
    'fred':       ('#0a4d8c', '#3a7fb8'),  # Fred — blått (FN-blått)
    'litt':       ('#7a1f2e', '#b04a5a'),  # Litteratur — burgundy
    'klassiker':  ('#5a4a2a', '#8a7a4a'),  # Historiska klassiker — sepia/guld
    'sve':        ('#005293', '#3a8fcc'),  # Svenska priser — Sverige-blå
    'sve2':       ('#b8860b', '#dba840'),  # Sverige guld
    'eu':         ('#003399', '#5575c7'),  # Europa — EU-blå
    'varld':      ('#1a1a1a', '#5a5a5a'),  # Världens priser — svart/guld
    'org':        ('#1a1a1a', '#5a5a5a'),
}


def photo_or_avatar(key, initials, region):
    """HTML för porträtt: riktigt foto om det finns, annars initial-avatar."""
    jpg = os.path.join(PHOTO_DIR, f"{key}.jpg")
    png = os.path.join(PHOTO_DIR, f"{key}.png")
    path = jpg if os.path.exists(jpg) else (png if os.path.exists(png) else None)
    if path:
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        ext = 'jpeg' if path.endswith('.jpg') else 'png'
        return f'<span class="portrait"><img src="data:image/{ext};base64,{data}" alt="{initials}"/></span>'
    c1, c2 = REGION.get(region, REGION['org'])
    return f'<span class="portrait avatar" style="background: radial-gradient(circle at 30% 30%, {c2}, {c1});">{initials}</span>'


# ============ DATA: NOBELS FREDSPRIS 2016-2025 ============
# (year, key, initials, region, flag, name, country, motivation)
PEACE_LAUREATES = [
    ("2025", "machado", "MM", "fred", "🇻🇪", "María Corina Machado", "Venezuela",
     "För outtröttligt arbete för Venezuelas demokratiska rättigheter och kamp för fredlig övergång från diktatur till demokrati. Oppositionsledare som tvingats leva i exil/gömställe under Maduro."),
    ("2024", "hidankyo", "NH", "fred", "🇯🇵", "Nihon Hidankyo", "Japan (organisation)",
     "Japansk gräsrotsorg av <i>hibakusha</i> (atombombsöverlevare från Hiroshima/Nagasaki). För arbete mot kärnvapen och vittnesmål om varför kärnvapen aldrig får användas igen."),
    ("2023", "mohammadi", "NMo", "fred", "🇮🇷", "Narges Mohammadi", "Iran",
     "För kampen mot förtrycket av kvinnor i Iran och kampen för mänskliga rättigheter och frihet för alla. Satt fängslad när priset tillkännagavs (Evin-fängelset)."),
    ("2022", "memorial", "BMC", "fred", "🇧🇾🇷🇺🇺🇦", "Bialiatski / Memorial / CCL", "Belarus, Ryssland, Ukraina",
     "Tre civilsamhälleslaureater: <b>Ales Bialiatski</b> (människorätt Belarus), <b>Memorial</b> (Sovjet-arkiv, mr-org Ryssland — tvångsupplöst 2021), <b>Center for Civil Liberties</b> (Ukraina, krigsbrott)."),
    ("2021", "ressa", "MR", "fred", "🇵🇭🇷🇺", "Maria Ressa & Dmitry Muratov", "Filippinerna & Ryssland",
     "För arbete att försvara yttrandefrihet — en förutsättning för demokrati och varaktig fred. Ressa: grundare Rappler. Muratov: chefredaktör Novaja Gazeta."),
    ("2020", "wfp", "WFP", "fred", "🇺🇳", "World Food Programme (WFP)", "FN-organisation",
     "För kampen mot hunger, bidrag till fred i konfliktområden och som drivande kraft i förebyggandet av hunger som vapen. FN-organ baserat i Rom."),
    ("2019", "abiy", "AA", "fred", "🇪🇹", "Abiy Ahmed Ali", "Etiopien",
     "För insatser för fred och internationellt samarbete, särskilt det avgörande initiativet att lösa gränskonflikten med grannlandet Eritrea. <b>OBS provfälla:</b> ledde sedan Tigray-kriget 2020-2022 (kontroversiell)."),
    ("2018", "mukwege", "DM", "fred", "🇨🇩🇮🇶", "Denis Mukwege & Nadia Murad", "DR Kongo & Irak",
     "För deras ansträngningar att stoppa användningen av sexuellt våld som vapen i krig. Mukwege: gynekolog/Panzi-sjukhuset. Murad: yazidisk överlevare av IS, MR-aktivist."),
    ("2017", "ican", "ICN", "fred", "🇨🇭", "ICAN", "International Campaign to Abolish Nuclear Weapons",
     "För arbete att uppmärksamma de katastrofala humanitära konsekvenserna av kärnvapen och banbrytande insatser för förbudstraktatet (TPNW). HQ: Genève."),
    ("2016", "santos", "JMS", "fred", "🇨🇴", "Juan Manuel Santos", "Colombia",
     "För hans beslutsamma insatser att avsluta över 50 år av inbördeskrig mellan Colombias regering och FARC-gerillan — fredsavtal undertecknat 2016."),
]

# ============ DATA: NOBELS LITTERATURPRIS 2016-2025 ============
# (year, key, initials, region, flag, name, country, language, work1, work2, citation_short)
LIT_LAUREATES = [
    ("2025", "krasznahorkai", "LK", "litt", "🇭🇺", "László Krasznahorkai", "Ungern", "ungerska",
     "<b>Sátántangó</b> (1985)", "<b>Motståndets melankoli</b> / The Melancholy of Resistance (1989)",
     "För hans gripande och visionära oeuvre som mitt i apokalyptisk skräck bekräftar konstens kraft."),
    ("2024", "hankang", "HK", "litt", "🇰🇷", "Han Kang", "Sydkorea", "koreanska",
     "<b>Vegetarianen</b> / The Vegetarian (2007, Booker Int'l 2016)", "<b>Levande och döda</b> / Human Acts (2014)",
     "För hennes intensiva poetiska prosa som konfronterar historiska trauman och blottlägger människolivets sårbarhet."),
    ("2023", "fosse", "JF", "litt", "🇳🇴", "Jon Fosse", "Norge", "nynorska",
     "<b>Septologien</b> (Det andra namnet, Jag är en annan, Ett nytt namn) 2019-21", "<b>Morgon och kväll</b> (2000)",
     "För hans nyskapande pjäser och prosa som ger röst åt det osägbara."),
    ("2022", "ernaux", "AE", "litt", "🇫🇷", "Annie Ernaux", "Frankrike", "franska",
     "<b>Åren</b> / Les Années (2008)", "<b>Platsen</b> / La Place (1983)",
     "För modet och den kliniska skärpan med vilken hon avtäcker rötterna, främlingskapen och kollektiva spärrar i den personliga minnet."),
    ("2021", "gurnah", "AG", "litt", "🇹🇿🇬🇧", "Abdulrazak Gurnah", "Tanzania/UK", "engelska",
     "<b>Paradiset</b> / Paradise (1994, Booker-shortlist)", "<b>Liv efter livet</b> / Afterlives (2020)",
     "För hans kompromisslösa och medkännande utforskning av kolonialismens effekter och flyktingars öden."),
    ("2020", "gluck", "LG", "litt", "🇺🇸", "Louise Glück", "USA", "engelska",
     "<b>The Wild Iris</b> (1992, Pulitzer)", "<b>Faithful and Virtuous Night</b> (2014)",
     "För hennes omisskännliga poetiska röst som med strikt skönhet gör individens existens universell."),
    ("2019", "handke", "PH", "litt", "🇦🇹", "Peter Handke", "Österrike", "tyska",
     "<b>Målvaktens skräck vid straffsparken</b> (1970)", "<b>Långsam hemkomst</b> (1979)",
     "För ett inflytelserikt verk som med språklig uppfinningsrikedom utforskat människans erfarenhets periferi och specificitet. <b>Provfälla:</b> kontroversiellt — Serbien-vänlig hållning under Balkankrigen."),
    ("2018", "tokarczuk", "OT", "litt", "🇵🇱", "Olga Tokarczuk", "Polen", "polska",
     "<b>Löparna</b> / Bieguni (2007, Booker Int'l 2018)", "<b>Jakobsböckerna</b> / Księgi Jakubowe (2014)",
     "För en narrativ fantasi som med encyklopedisk passion gestaltar gränsöverskridande som en livsform. <b>Obs:</b> tilldelat 2019 (efter Akademins skandal)."),
    ("2017", "ishiguro", "KI", "litt", "🇬🇧", "Kazuo Ishiguro", "UK (f. Japan)", "engelska",
     "<b>Återstoden av dagen</b> / The Remains of the Day (1989, Booker)", "<b>Never Let Me Go</b> (2005)",
     "Som i romaner med stor känslomässig kraft har avtäckt avgrunden bortom vår illusoriska känsla av samhörighet med världen."),
    ("2016", "dylan", "BD", "litt", "🇺🇸", "Bob Dylan", "USA", "engelska",
     "<b>Chronicles, Vol. 1</b> (2004) — memoarer", "<b>Sångtexter</b> (Blowin' in the Wind, Like a Rolling Stone, The Times They Are A-Changin')",
     "För att ha skapat nya poetiska uttryck inom den stora amerikanska sångtraditionen. <b>Provfälla:</b> första musiker att vinna Nobel Lit; tackade nej att åka."),
]

# Bonusrad: 2015 Svetlana Alexievich
LIT_BONUS_2015 = ("2015", "alexievich", "SA", "litt", "🇧🇾", "Svetlana Aleksijevitj", "Belarus", "ryska",
                  "<b>Kriget har inget kvinnligt ansikte</b> (1985)", "<b>Tiden second hand</b> / Secondhand Time (2013)",
                  "För hennes polyfona författarskap, ett monument över lidande och mod i vår tid.")
PEACE_BONUS_2015 = ("2015", "ndq", "NDQ", "fred", "🇹🇳", "Nationella dialogkvartetten", "Tunisien (4 org)",
                    "För dess avgörande bidrag till uppbyggnaden av en pluralistisk demokrati i Tunisien efter jasminrevolutionen 2011 (UGTT, UTICA, LTDH, advokatsamfundet).")

# ============ HISTORISKA KLASSIKER (10 must-know) ============
# (key, initials, region, year, type, flag, name, country, work_or_cause)
HISTORIC = [
    ("dunant", "HD", "klassiker", "1901", "FRED", "🇨🇭", "Henry Dunant", "Schweiz",
     "Grundade <b>Röda Korset</b> (1863) efter att ha bevittnat slaget vid Solferino. Inspirerade <b>Genèvekonventionerna</b>. <b>Första Nobels fredspris någonsin</b> (delat med fransmannen Frédéric Passy)."),
    ("lagerlof", "SL", "klassiker", "1909", "LITT", "🇸🇪", "Selma Lagerlöf", "Sverige",
     "<b>Första kvinnan</b> + <b>första svensk</b> som fick Nobels litteraturpris. Verk: <b>Gösta Berlings saga</b> (1891), <b>Nils Holgerssons underbara resa</b> (1906-07). Första kvinna i Sv. Akademien (1914)."),
    ("hemingway", "EH", "klassiker", "1954", "LITT", "🇺🇸", "Ernest Hemingway", "USA",
     "Verk: <b>Den gamle och havet</b> / The Old Man and the Sea (1952, Pulitzer 1953), <b>För vem klockan klämtar</b> / For Whom the Bell Tolls (1940). Stilbildande knapp prosa, the Lost Generation."),
    ("mlk", "MLK", "klassiker", "1964", "FRED", "🇺🇸", "Martin Luther King Jr.", "USA",
     "För ledarskapet i den icke-våldsbaserade <b>medborgarrättsrörelsen</b> mot rassegregation i USA. <b>\"I have a dream\"</b>-talet 1963. Yngsta laureat då (35 år). Mördad 1968."),
    ("teresa", "MT", "klassiker", "1979", "FRED", "🇮🇳", "Moder Teresa", "Albanien/Indien",
     "Grundare av <b>Missionaries of Charity</b> i Calcutta. För arbete bland de fattigaste och döende. Albanskfödd, verksam Indien. Helgonförklarad 2016."),
    ("marquez", "GM", "klassiker", "1982", "LITT", "🇨🇴", "Gabriel García Márquez", "Colombia",
     "Mästare av <b>magisk realism</b>. Verk: <b>Hundra år av ensamhet</b> / Cien años de soledad (1967), <b>Kärlek i kolerans tid</b> / El amor en los tiempos del cólera (1985)."),
    ("morrison", "TM", "klassiker", "1993", "LITT", "🇺🇸", "Toni Morrison", "USA",
     "<b>Första afroamerikanska kvinna</b> att vinna Nobel Lit. Verk: <b>Älskade</b> / Beloved (1987, Pulitzer 1988), <b>Sula</b> (1973). Tema: USA:s ras- och slaverihistoria."),
    ("mandela", "NM", "klassiker", "1993", "FRED", "🇿🇦", "Nelson Mandela & F.W. de Klerk", "Sydafrika",
     "Delat pris för det fredliga avskaffandet av <b>apartheid</b> och grunden för ett demokratiskt Sydafrika. Mandela: ANC, 27 år i fängelse. de Klerk: National Party, släppte Mandela 1990."),
    ("tranströmer", "TT", "klassiker", "2011", "LITT", "🇸🇪", "Tomas Tranströmer", "Sverige",
     "<b>Senaste svensk Nobel Lit</b>. Lyriker. Verk: <b>Östersjöar</b> (1974), <b>Den stora gåtan</b> (2004). \"Kondenserade, genomlysta bilder som ger oss ny tillgång till verkligheten.\""),
    ("eu", "EU", "klassiker", "2012", "FRED", "🇪🇺", "Europeiska unionen (EU)", "Bryssel",
     "För över sex decenniers bidrag till <b>fred, försoning, demokrati och mänskliga rättigheter</b> i Europa. Mottogs av Van Rompuy, Barroso och Schulz. Kontroversiellt under eurokrisen."),
]

# ============ SVERIGES 5 KÄNDASTE KULTURPRISER ============
# (key, initials, region, prize, latest, winner_or_winners, work_or_note)
SVE_PRIZES = [
    ("augustpriset", "AUG", "sve", "Augustpriset",
     "1989-, delas ut årligen av Sv. Förläggareföreningen i tre klasser",
     "<b>2025 vinnare:</b><br>• <b>Skön:</b> Lina Wolff — \"Liken vi begravde\"<br>• <b>Fack:</b> Bea Uusma — \"Vitön\" (uppföljare till \"Expeditionen\")<br>• <b>Barn:</b> Fabian Göranson — \"Klara — Tvättbjörnarnas stad\"",
     "Sveriges mest prestigefyllda litteraturpris. Wolff och Uusma båda andra gången."),
    ("polar", "POL", "sve2", "Polar Music Prize",
     "Grundat 1989 av ABBA-managern Stikkan Anderson, ofta kallat \"musikens Nobel\"",
     "<b>2025 vinnare</b> (3 mottagare för första gången, 1 milj SEK var):<br>• <b>Pop/rock:</b> <b>Queen</b> (Brian May, Roger Taylor)<br>• <b>Jazz:</b> <b>Herbie Hancock</b> (USA)<br>• <b>Klassiskt:</b> <b>Barbara Hannigan</b> (sopran/dirigent, Kanada)",
     "Ceremoni 27 maj 2025 på Grand Hôtel, Stockholm. Delas ut av Kung Carl XVI Gustaf."),
    ("alma", "ALMA", "sve", "ALMA — Litteraturpris till Astrid Lindgrens minne",
     "Grundat 2002 efter A. Lindgrens död. Världens största barn- och ungdomslitteraturpris (5 milj SEK)",
     "<b>2026 vinnare:</b> <b>Jon Klassen</b> (Kanada) — illustratör/bilderboksförfattare<br><i>(2025 vinnare: Marion Brunet, Frankrike)</i>",
     "Ceremoni 25 maj 2026 på Konserthuset av kronprinsessan Victoria. 263 nominerade från 74 länder."),
    ("guldbaggen", "GB", "sve2", "Guldbaggen",
     "Sveriges främsta filmpris, delas ut av Svenska Filminstitutet sedan 1964",
     "<b>2026 vinnare — bästa film:</b> <b>Eagles of the Republic</b> av Tarik Saleh (politisk thriller, 6 Guldbaggar totalt)<br>Andra: \"Kevlarsjäl\", \"Rörelser\" (2 baggar var); publikens pris: \"Filmen om Siw\"",
     "Galan jan 2026."),
    ("nordrad", "NRL", "sve", "Nordiska rådets litteraturpris",
     "Sedan 1962 — nordiskt litteraturpris, gemensamt för alla nordiska länder och självstyrande områden",
     "<b>2025 vinnare:</b> <b>Vónbjørt Vang</b> (Färöarna) — diktsamlingen \"Svørt Orkidé\" om en mors rädsla att förlora sin tonårsson.",
     "300 000 DKK. Tema: nutida moderskapslitteratur."),
]

# Bonus svensk: Stora Journalistpriset
SVE_BONUS = ("stora_jp", "SJP", "sve2", "Stora Journalistpriset",
             "Sveriges mest prestigefyllda journalistpris (Bonniers, sedan 1966)",
             "<b>2025 vinnare:</b><br>• <b>Lukas Bonniers Stora pris:</b> Katarina Gunnarsson (SR)<br>• <b>Årets Berättare:</b> Liza Alexandrova-Zorina — \"De livegnas land\"<br>• <b>Årets Avslöjande:</b> Lindkvist & Örstadius (DN) — Landerholmsaffären<br>• <b>Årets Förnyare:</b> Hamidi-Nia & Hörnqvist (SVT) — \"Gaza — till sista andetaget\"<br>• <b>Årets Röst:</b> Messiah Hallberg (\"Svenska nyheter\")",
             "Galan 20 nov 2025, Bonniers konsthall.")

# ============ EUROPAS 5 KÄNDASTE KULTURPRISER ============
EU_PRIZES = [
    ("booker", "BP", "eu", "Booker Prize (UK)",
     "Sedan 1969 (anglosaxisk litteratur). 2025 års pris £50 000",
     "<b>2025 vinnare:</b> <b>David Szalay</b> — \"<b>Flesh</b>\"<br>Första ungersk-brittiska författare att vinna. Spannar livet från ungersk förort till Londons rika elit.",
     "Tilldelades 10 nov 2025."),
    ("goncourt", "GO", "eu", "Prix Goncourt (Frankrike)",
     "Sedan 1903, Frankrikes mest prestigefyllda litteraturpris (€10 symboliskt)",
     "<b>2025 vinnare:</b> <b>Laurent Mauvignier</b> — \"<b>La Maison vide</b>\" (Éditions de Minuit)<br>Familjeminnen genom generationer från 1976. Vald i första röstomgången.",
     "Tilldelat 4 nov 2025 (på restaurang Drouant, Paris)."),
    ("cervantes", "CER", "eu", "Premio Cervantes (Spanien)",
     "Sedan 1976, viktigaste priset för spanskspråkig litteratur (€125 000)",
     "<b>2025 vinnare:</b> <b>Gonzalo Celorio</b> (Mexiko, f. 1948)<br>Berättare, essäist. Erkänns för \"exceptionellt litterärt verk\" och bidrag till hispansk kultur. Jubileum: 50:e upplagan.",
     "Utdelat 23 april 2026 (Cervantes dödsdag) av kung Felipe VI vid Univ. Alcalá."),
    ("strega", "STR", "eu", "Premio Strega (Italien)",
     "Sedan 1947, Italiens mest prestigefyllda litteraturpris",
     "<b>2025 vinnare:</b> <b>Andrea Bajani</b> — \"<b>L'anniversario</b>\" (Feltrinelli)<br>194/646 röster. Roman om bryta med patriarkalt arv.",
     "79:e upplagan, Villa Giulia, Rom 3 juli 2025."),
    ("palme", "PdO", "eu", "Cannes Palme d'Or (Frankrike)",
     "Världens mest prestigefyllda filmfestival, Cannes (sedan 1955)",
     "<b>2025 vinnare:</b> <b>Jafar Panahi</b> (Iran) — \"<b>It Was Just an Accident</b>\"<br>Iransk regissör, fängslad regimkritiker. Trippel: vunnit topp på alla 3 stora europ. festivaler (Berlin Bear 2015, Venedig Lion 2000, Cannes Palme 2025).",
     "78:e Cannes-festivalen, juryn ledd av Juliette Binoche."),
]

# Bonus europeisk: Berlin Golden Bear 2026
EU_BONUS = ("berlin", "BB", "eu", "Berlin Golden Bear (Berlinalen)",
            "Tysklands prestigefilmfestival sedan 1951",
            "<b>2026 vinnare:</b> <b>İlker Çatak</b> (Tyskland-Turkiet) — \"<b>Yellow Letters</b>\"<br>Om vänsterturkiskt par i Ankara under press från staten. Första tyska Golden Bear på 22 år. Jury under Wim Wenders.",
            "76:e Berlinalen, 21 feb 2026.")

# ============ VÄRLDENS MEST KÄNDA KULTURPRISER ============
WORLD_PRIZES = [
    ("oscar", "OS", "varld", "Academy Awards / Oscars (USA, film)",
     "Världens mest kända filmpris, sedan 1929",
     "<b>2026 (98:e galan, 15 mars 2026):</b><br>• <b>Bästa film:</b> \"<b>One Battle After Another</b>\" (Paul Thomas Anderson)<br>• <b>Bästa regi:</b> Paul Thomas Anderson<br>• <b>Bästa adapterade manus:</b> P.T. Anderson (hans första Oscars någonsin)<br>• <b>Bästa skådespelare:</b> Michael B. Jordan; <b>Bästa kvinnliga huvudroll:</b> Jessie Buckley<br>• Filmen vann 6 Oscars totalt.",
     "Dolby Theatre, Hollywood. Ny kategori: bästa casting."),
    ("pulitzer", "PUL", "varld", "Pulitzer Prize (USA, journalistik+konst)",
     "Sedan 1917, journalistik & litteratur i USA",
     "<b>2025 — Pulitzer Fiction:</b> <b>Percival Everett</b> — \"<b>James</b>\" (omtolkning av Huckleberry Finn)<br>• Drama: \"Purpose\" av Branden Jacobs-Jenkins<br>• Public Service: ProPublica (kvinnors abortvård)<br>• National Reporting: AP/FRONTLINE (gränsbevakning)",
     "Utdelat 5 maj 2025."),
    ("grammy", "GR", "varld", "Grammy Awards (USA, musik)",
     "Världens mest kända musikpris (sedan 1959). 68:e galan 1 feb 2026",
     "<b>2026 vinnare:</b><br>• <b>Album of the Year:</b> Bad Bunny — \"DeBÍ TiRAR MáS FOToS\" — <b>första spanskspråkiga albumet att vinna</b><br>• <b>Record of the Year:</b> \"luther\" — Kendrick Lamar & SZA<br>• <b>Song of the Year:</b> \"Wildflower\" — Billie Eilish<br>• Kvällens kung: Kendrick Lamar (5 vinster, mest priser någonsin för hiphopartist)",
     ""),
    ("pritzker", "PR", "varld", "Pritzker Architecture Prize (arkitektur)",
     "\"Arkitekturens Nobel\". Sedan 1979, $100 000",
     "<b>2025 vinnare:</b> <b>Liu Jiakun</b> (Kina, Chengdu) — 54:e laureaten<br>Grundare av Jiakun Architecture (1999). För arkitektur som svarar mot social/miljömässig förändring.",
     "Ceremoni i Abu Dhabi våren 2025."),
    ("venice", "GL", "varld", "Venice Golden Lion (Italien, film)",
     "Världens äldsta filmfestival (sedan 1932)",
     "<b>2025 vinnare:</b> <b>Jim Jarmusch</b> (USA) — \"<b>Father Mother Sister Brother</b>\"<br>Triptyk om vuxna barn och deras avlägsna föräldrar i tre länder. Första gången Jarmusch tävlat i Venedig.<br>• Grand Jury Prize: \"The Voice of Hind Rajab\" (Gaza-drama)<br>• Werner Herzog: Golden Lion for Lifetime Achievement",
     "82:a Venedig-festivalen, 6 sep 2025."),
]

# Bonus världsliga: Tony Awards
WORLD_BONUS = ("tony", "TONY", "varld", "Tony Awards (USA, teater Broadway)",
               "USA:s främsta teaterpris (sedan 1947). 78:e galan 8 juni 2025",
               "<b>2025 vinnare:</b><br>• <b>Best Musical:</b> \"<b>Maybe Happy Ending</b>\" — kvällens stora vinnare med 6 Tonys<br>• <b>Best Play:</b> \"<b>Purpose</b>\" av Branden Jacobs-Jenkins (även Pulitzer Drama)<br>• Best Musical Revival: \"Sunset Boulevard\"; Best Play Revival: \"Eureka Day\"",
               "Radio City Music Hall. Värd: Cynthia Erivo.")


# ============ HTML RENDERING ============

def render_peace_row(row):
    year, key, initials, region, flag, name, country, motivation = row
    portrait = photo_or_avatar(key, initials, region)
    return f'''
    <div class="laureate peace">
      {portrait}
      <div class="lflag">{flag}</div>
      <div class="linfo">
        <div class="lyear">{year}</div>
        <div class="lname">{name} <span class="lcountry">· {country}</span></div>
        <div class="lcite">{motivation}</div>
      </div>
    </div>'''


def render_lit_row(row):
    year, key, initials, region, flag, name, country, language, work1, work2, citation = row
    portrait = photo_or_avatar(key, initials, region)
    return f'''
    <div class="laureate lit">
      {portrait}
      <div class="lflag">{flag}</div>
      <div class="linfo">
        <div class="lyear">{year}</div>
        <div class="lname">{name} <span class="lcountry">· {country} · skriver på {language}</span></div>
        <div class="lworks">{work1} &nbsp;·&nbsp; {work2}</div>
        <div class="lcite-small"><i>Motivering:</i> {citation}</div>
      </div>
    </div>'''


def render_historic(row):
    key, initials, region, year, ptype, flag, name, country, body = row
    portrait = photo_or_avatar(key, initials, region)
    type_class = "type-fred" if ptype == "FRED" else "type-litt"
    return f'''
    <div class="historic">
      {portrait}
      <div class="hflag">{flag}</div>
      <div class="hinfo">
        <div class="hhead">
          <span class="hyear">{year}</span>
          <span class="htype {type_class}">{ptype}</span>
          <span class="hname">{name}</span>
          <span class="hcountry">· {country}</span>
        </div>
        <div class="hbody">{body}</div>
      </div>
    </div>'''


def render_prize(row, region_class):
    key, initials, region, prize, sub, body, foot = row
    portrait = photo_or_avatar(key, initials, region)
    foot_html = f'<div class="prize-foot">{foot}</div>' if foot else ''
    return f'''
    <div class="prize {region_class}">
      <div class="prize-head">
        {portrait}
        <div class="prize-title-block">
          <div class="prize-name">{prize}</div>
          <div class="prize-sub">{sub}</div>
        </div>
      </div>
      <div class="prize-body">{body}</div>
      {foot_html}
    </div>'''


# ============ CSS ============
CSS = """
@page { size: A3 portrait; margin: 6mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  font-family: "DejaVu Sans", "Noto Sans", sans-serif;
  font-size: 7.6pt;
  line-height: 1.22;
  color: #1a1a1a;
  background: #fafaf7;
}
.page { page-break-after: always; position: relative; }
.page:last-child { page-break-after: auto; }

/* HEADER */
header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 2mm 4mm 1.5mm;
  border-bottom: 2pt solid #1a1a1a;
  margin-bottom: 2mm;
}
.title-block h1 {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 22pt;
  font-weight: 900;
  letter-spacing: -0.5pt;
  line-height: 0.95;
}
.title-block h1 span { color: #c1272d; }
.title-block .sub {
  font-size: 8.5pt;
  margin-top: 0.8mm;
  color: #555;
  font-style: italic;
}
.meta-block {
  text-align: right;
  font-size: 7pt;
  color: #333;
}
.meta-block .date {
  font-weight: 700;
  font-size: 8.5pt;
  color: #c1272d;
}
.meta-block .verified {
  background: #1a1a1a;
  color: #fafaf7;
  padding: 0.8mm 1.8mm;
  margin-top: 0.8mm;
  display: inline-block;
  font-size: 6.5pt;
  letter-spacing: 0.5pt;
  text-transform: uppercase;
}

/* SECTION TITLES */
.section-title {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 11pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.6pt;
  margin: 1.5mm 4mm 1.0mm;
  padding-bottom: 0.5mm;
  border-bottom: 1.5pt solid #1a1a1a;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.section-title .stag {
  font-family: "DejaVu Sans", sans-serif;
  font-size: 7pt;
  font-weight: 400;
  color: #888;
  font-style: italic;
  letter-spacing: 0;
  text-transform: none;
}
.section-title.peace { color: #0a4d8c; border-bottom-color: #0a4d8c; }
.section-title.lit   { color: #7a1f2e; border-bottom-color: #7a1f2e; }
.section-title.hist  { color: #5a4a2a; border-bottom-color: #5a4a2a; }
.section-title.sve   { color: #005293; border-bottom-color: #005293; }
.section-title.eu    { color: #003399; border-bottom-color: #003399; }
.section-title.varld { color: #c1272d; border-bottom-color: #c1272d; }

/* PORTRAIT */
.portrait {
  width: 9mm;
  height: 9mm;
  border-radius: 50%;
  display: block;
  overflow: hidden;
  position: relative;
  border: 0.8pt solid #1a1a1a;
  flex-shrink: 0;
}
.portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.portrait.avatar {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 6.5pt;
  color: white;
  text-align: center;
  line-height: 9mm;
  letter-spacing: -0.3pt;
  text-shadow: 0.3pt 0.3pt 0.5pt rgba(0,0,0,0.3);
}

/* LAUREATE ROW (Peace + Lit) */
.laureates-grid {
  padding: 0 4mm;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 3mm;
}
.laureate {
  display: grid;
  grid-template-columns: 9mm 5mm 1fr;
  gap: 1.5mm;
  padding: 1.0mm 0;
  border-bottom: 0.4pt dotted #b8b8b8;
  align-items: start;
  break-inside: avoid;
}
.laureate:last-child { border-bottom: none; }
.laureate.peace { border-left: 2pt solid #0a4d8c; padding-left: 1.5mm; margin-left: -1.5mm;}
.laureate.lit { border-left: 2pt solid #7a1f2e; padding-left: 1.5mm; margin-left: -1.5mm;}
.lflag {
  font-size: 11pt;
  font-family: "Noto Color Emoji", "DejaVu Sans";
  text-align: center;
  line-height: 1.0;
  padding-top: 0.5mm;
}
.linfo { font-size: 6.7pt; line-height: 1.2; min-width: 0;}
.lyear {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 9pt;
  color: #c1272d;
  letter-spacing: 0.3pt;
  display: inline-block;
  margin-right: 1.5mm;
}
.peace .lyear { color: #0a4d8c; }
.lit .lyear { color: #7a1f2e; }
.lname {
  display: inline;
  font-weight: 700;
  font-size: 7.6pt;
}
.lcountry {
  font-weight: 400;
  color: #555;
  font-size: 6.6pt;
}
.lcite {
  font-size: 6.4pt;
  color: #444;
  margin-top: 0.4mm;
  line-height: 1.25;
}
.lworks {
  font-size: 6.7pt;
  color: #1a1a1a;
  margin-top: 0.4mm;
}
.lcite-small {
  font-size: 6.0pt;
  color: #777;
  margin-top: 0.3mm;
  line-height: 1.2;
}
.bonus-tag {
  display: inline-block;
  font-size: 5.5pt;
  background: #f0d043;
  color: #1a1a1a;
  padding: 0.2mm 0.8mm;
  border-radius: 1mm;
  margin-left: 1.2mm;
  font-weight: 700;
  letter-spacing: 0.3pt;
}

/* HISTORIC */
.historic-grid {
  padding: 0 4mm;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1mm 3mm;
}
.historic {
  display: grid;
  grid-template-columns: 9mm 5mm 1fr;
  gap: 1.5mm;
  padding: 1.0mm 1.5mm;
  border: 0.6pt solid #c5b89a;
  background: #fdfaf2;
  border-left: 2.5pt solid #5a4a2a;
  align-items: start;
  break-inside: avoid;
}
.hflag {
  font-size: 11pt;
  font-family: "Noto Color Emoji", "DejaVu Sans";
  text-align: center;
  padding-top: 0.5mm;
}
.hinfo { font-size: 6.6pt; line-height: 1.25; min-width: 0;}
.hhead {
  font-size: 7.4pt;
  margin-bottom: 0.4mm;
}
.hyear {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 8.5pt;
  color: #5a4a2a;
  margin-right: 1.2mm;
}
.htype {
  display: inline-block;
  font-size: 5.8pt;
  font-weight: 700;
  padding: 0.2mm 0.9mm;
  border-radius: 1mm;
  margin-right: 1.2mm;
  letter-spacing: 0.3pt;
  color: white;
  vertical-align: 1px;
}
.htype.type-fred { background: #0a4d8c; }
.htype.type-litt { background: #7a1f2e; }
.hname { font-weight: 700; }
.hcountry { color: #555; font-weight: 400; font-size: 6.5pt; }
.hbody { font-size: 6.4pt; color: #1a1a1a; }

/* PRIZE BOXES (Sve/EU/World) */
.prizes-grid {
  padding: 0 4mm;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.5mm;
}
.prize {
  border: 0.8pt solid #1a1a1a;
  background: #fff;
  padding: 1.5mm 1.8mm;
  break-inside: avoid;
  border-top-width: 3pt;
}
.prize.sve { border-top-color: #005293; }
.prize.sve2 { border-top-color: #b8860b; }
.prize.eu { border-top-color: #003399; }
.prize.varld { border-top-color: #c1272d; }
.prize-head {
  display: grid;
  grid-template-columns: 9mm 1fr;
  gap: 1.5mm;
  align-items: center;
  margin-bottom: 1.0mm;
  padding-bottom: 0.7mm;
  border-bottom: 0.5pt solid #ddd;
}
.prize-title-block { min-width: 0; }
.prize-name {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 8.5pt;
  letter-spacing: 0.2pt;
  line-height: 1.1;
}
.prize.sve .prize-name { color: #005293; }
.prize.sve2 .prize-name { color: #8a6209; }
.prize.eu .prize-name { color: #003399; }
.prize.varld .prize-name { color: #c1272d; }
.prize-sub {
  font-size: 5.8pt;
  color: #666;
  font-style: italic;
  margin-top: 0.3mm;
  line-height: 1.2;
}
.prize-body {
  font-size: 6.5pt;
  line-height: 1.32;
  color: #1a1a1a;
}
.prize-foot {
  font-size: 5.8pt;
  color: #888;
  margin-top: 0.7mm;
  padding-top: 0.5mm;
  border-top: 0.3pt dotted #ccc;
  font-style: italic;
}

/* TWO-COL FOR PRIZES (when only 2 columns) */
.prizes-grid.two-col {
  grid-template-columns: 1fr 1fr;
}

/* INFO PANEL — Sveriges Nobel-historik */
.swedish-panel {
  margin: 1.0mm 4mm 1.5mm;
  padding: 1.5mm 2.5mm;
  background: #fff8e0;
  border: 0.8pt solid #d4a012;
  border-left: 3pt solid #d4a012;
  font-size: 6.4pt;
  line-height: 1.32;
}
.swedish-panel h4 {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 8.0pt;
  font-weight: 900;
  color: #8a6209;
  margin-bottom: 0.5mm;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
}
.swedish-panel b { color: #5a4a2a; }

/* FOOTER */
footer {
  margin: 1.5mm 4mm 0;
  display: flex;
  justify-content: space-between;
  font-size: 6pt;
  color: #888;
  border-top: 0.5pt solid #ccc;
  padding-top: 0.6mm;
}
"""


# ============ PAGE BUILDERS ============

def build_page1():
    """Sida 1: Senaste 10 åren — Fredspris + Litteraturpris."""
    peace_html = ''.join(render_peace_row(r) for r in PEACE_LAUREATES)
    bonus_peace = render_peace_row(PEACE_BONUS_2015).replace(
        '<div class="lyear">2015</div>',
        '<div class="lyear">2015<span class="bonus-tag">+1 BONUS</span></div>'
    )

    lit_html = ''.join(render_lit_row(r) for r in LIT_LAUREATES)
    bonus_lit = render_lit_row(LIT_BONUS_2015).replace(
        '<div class="lyear">2015</div>',
        '<div class="lyear">2015<span class="bonus-tag">+1 BONUS</span></div>'
    )

    return f'''
    <div class="page">
      <header>
        <div class="title-block">
          <h1>NOBEL <span>FRED</span> &amp; <span>LITTERATUR</span></h1>
          <div class="sub">Senaste 10 åren (2016-2025) · DIPS-plansch · Sida 1</div>
        </div>
        <div class="meta-block">
          <div class="date">Provdatum: 18 maj 2026</div>
          <div>Uppdaterad: maj 2026 · 10 år + 1 bonus (2015)</div>
          <div class="verified">VERIFIERAD MOT NOBELPRIZE.ORG</div>
        </div>
      </header>

      <div class="section-title peace">
        Nobels Fredspris 2016-2025
        <span class="stag">Vad/varför kämpar de? · 10 år + 2015 bonus</span>
      </div>
      <div class="laureates-grid">
        {peace_html}
        {bonus_peace}
      </div>

      <div class="section-title lit">
        Nobels Litteraturpris 2016-2025
        <span class="stag">Två mest kända verk per laureat · 10 år + 2015 bonus</span>
      </div>
      <div class="laureates-grid">
        {lit_html}
        {bonus_lit}
      </div>

      <footer>
        <span>DIPS 2026 · Nobel &amp; Kulturpriser-plansch v1 · Källa: nobelprize.org, Sv. Akademien</span>
        <span>Sida 1/2</span>
      </footer>
    </div>'''


def build_page2():
    """Sida 2: Historiska klassiker + Sveriges/Europas/Världens kulturpriser."""
    historic_html = ''.join(render_historic(r) for r in HISTORIC)

    sve_html = ''.join(render_prize(r, r[2]) for r in SVE_PRIZES)
    sve_bonus_html = render_prize(SVE_BONUS, SVE_BONUS[2])

    eu_html = ''.join(render_prize(r, r[2]) for r in EU_PRIZES)
    eu_bonus_html = render_prize(EU_BONUS, EU_BONUS[2])

    world_html = ''.join(render_prize(r, r[2]) for r in WORLD_PRIZES)
    world_bonus_html = render_prize(WORLD_BONUS, WORLD_BONUS[2])

    return f'''
    <div class="page">
      <header>
        <div class="title-block">
          <h1>HISTORISKA <span>KLASSIKER</span> &amp; <span>KULTURPRISER</span></h1>
          <div class="sub">10 must-know Nobel-laureater &amp; kulturpriser · DIPS-plansch · Sida 2</div>
        </div>
        <div class="meta-block">
          <div class="date">Provdatum: 18 maj 2026</div>
          <div>Sverige + Europa + Världen · senaste vinnare</div>
          <div class="verified">VERIFIERAD MAJ 2026</div>
        </div>
      </header>

      <div class="section-title hist">
        10 historiska Nobel-laureater man bör kunna
        <span class="stag">Mix av fred + litteratur · klassiska provfrågor</span>
      </div>
      <div class="historic-grid">
        {historic_html}
      </div>

      <div class="swedish-panel">
        <h4>★ Sveriges 7 Nobel-laureater i litteratur — alla genom tiderna ★</h4>
        <b>1909 Selma Lagerlöf</b> (Gösta Berlings saga · Nils Holgersson) ·
        <b>1916 Verner von Heidenstam</b> (Karolinerna) ·
        <b>1931 Erik Axel Karlfeldt</b> (postumt — Fridolins visor) ·
        <b>1951 Pär Lagerkvist</b> (Barabbas · Dvärgen) ·
        <b>1974 Eyvind Johnson &amp; Harry Martinson</b> (Aniara · Strändernas svall) — kontroversiellt: båda satt själva i Sv. Akademien ·
        <b>2011 Tomas Tranströmer</b> (Östersjöar · Den stora gåtan) — senaste svensk
      </div>

      <div class="section-title sve">
        Sveriges 5 kändaste kulturpriser
        <span class="stag">Augustpriset · Polar Music · ALMA · Guldbaggen · Nordiska rådets · + bonus</span>
      </div>
      <div class="prizes-grid">
        {sve_html}
        {sve_bonus_html}
      </div>

      <div class="section-title eu">
        Europas 5 kändaste kulturpriser
        <span class="stag">Booker · Goncourt · Cervantes · Strega · Cannes Palme d'Or · + Berlin Bear</span>
      </div>
      <div class="prizes-grid">
        {eu_html}
        {eu_bonus_html}
      </div>

      <div class="section-title varld">
        Världens kändaste kulturpriser
        <span class="stag">Oscars · Pulitzer · Grammy · Pritzker · Venice Lion · + Tony</span>
      </div>
      <div class="prizes-grid">
        {world_html}
        {world_bonus_html}
      </div>

      <footer>
        <span>DIPS 2026 · Källa: officiella prissajter, SVT, BBC, NPR · Lycka till på provet, Moa! 🇸🇪</span>
        <span>Sida 2/2</span>
      </footer>
    </div>'''


# ============ MAIN ============

def build():
    html = f'''<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="utf-8"/>
  <title>DIPS 2026 — Nobel &amp; Kulturpriser-plansch</title>
  <style>{CSS}</style>
</head>
<body>
  {build_page1()}
  {build_page2()}
</body>
</html>'''
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ HTML skriven: {OUTPUT_HTML}")
    weasyprint.HTML(string=html, base_url='.').write_pdf(OUTPUT_PDF)
    print(f"✓ PDF genererad: {OUTPUT_PDF}")


if __name__ == "__main__":
    build()
