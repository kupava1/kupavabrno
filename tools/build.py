"""Generátor webu Kupava (CZ/UA/EN).
Spuštění:  cd kupava-web && python3 tools/build.py
Data o vystoupeních: data/vystoupeni.json  ("highlight": true = zobrazí se ve výběru významných vystoupení)
"""
import json, os, sys, html, time, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://kupavabrno.cz"
VER = time.strftime("%Y%m%d%H%M%S")
LANGS = {"cs": "/", "uk": "/uk/", "en": "/en/"}
FORM_ENDPOINT = "https://formsubmit.co/ajax/kupava@kupavabrno.cz"
e = html.escape

TODAY = datetime.date.today().isoformat()
EVENTS = sorted(json.load(open(os.path.join(OUT, "data", "vystoupeni.json")))["events"], key=lambda x: x["date"])
PAST = [ev for ev in EVENTS if ev["date"] < TODAY]
UPCOMING = [ev for ev in EVENTS if ev["date"] >= TODAY]
HIGHLIGHTS = [ev for ev in reversed(PAST) if ev.get("highlight")]
POSTS = sorted(json.load(open(os.path.join(OUT, "data", "aktuality.json")))["posts"], key=lambda x: x["date"], reverse=True)
def post_url(lang, slug): return LANGS[lang] + "aktuality/" + slug + "/"

X = {
 "cs": dict(nav_news="Aktuality", news_k="Aktuality", news_h="Z našeho dění", more="Číst dál", back="← Zpět na hlavní stránku", all_news="Další aktuality", all_btn="Všechny aktuality", arch_desc="Aktuality ukrajinského folklorního souboru Kupava z Brna – vystoupení, festivaly a koncerty.",
            press_k="Pro média a pořadatele", press_h="Podklady ke stažení",
            press_p="Fotografie ve vysokém rozlišení, logo a medailonek souboru pro programy festivalů, plakáty a tiskové zprávy. Při použití fotografií prosíme o uvedení zdroje „Soubor Kupava“.",
            bio_h="Krátký medailonek", copy="Kopírovat text", copied="Zkopírováno",
            dl_zip="Kompletní balíček (ZIP)", dl_logo="Logo (PNG)", dl_bio="Medailonky CZ / UA / EN (TXT)", dl_photos="Fotografie",
            bio="Kupava je ukrajinský folklorní soubor z Brna, založený v únoru 2023. Věnuje se tradičnímu ukrajinskému vícehlasému zpěvu a lidové hudbě z různých regionů Ukrajiny – zpívá v originále, v krojích a za doprovodu živé hudby. Soubor vystoupil mimo jiné na MFF Strážnice, festivalu Smetanova Litomyšl, Chodských slavnostech a v přímém přenosu Koncertu pro život II na TV Noe. Umělecká vedoucí: Mgr. Kateryna Mykhaylova.",
            foot_press="Pro média", other_perf="Další vystoupení"),
 "uk": dict(nav_news="Новини", news_k="Новини", news_h="Що в нас нового", more="Читати далі", back="← На головну сторінку", all_news="Інші новини", all_btn="Усі новини", arch_desc="Новини українського фольклорного ансамблю «Купава» з Брно – виступи, фестивалі та концерти.",
            press_k="Для медіа та організаторів", press_h="Матеріали для завантаження",
            press_p="Фотографії у високій роздільній здатності, логотип і коротка довідка про ансамбль для фестивальних програм, афіш і пресрелізів. Використовуючи фото, просимо зазначати джерело «Ансамбль Купава».",
            bio_h="Коротка довідка", copy="Копіювати текст", copied="Скопійовано",
            dl_zip="Повний пакет (ZIP)", dl_logo="Логотип (PNG)", dl_bio="Довідки CZ / UA / EN (TXT)", dl_photos="Фотографії",
            bio="«Купава» – український фольклорний ансамбль з Брно, заснований у лютому 2023 року. Ансамбль присвячує себе традиційному українському багатоголосому співу та народній музиці з різних регіонів України – співає в оригіналі, у народних строях, під живу музику. Виступав, зокрема, на МФФ у Стражніце, фестивалі Smetanova Litomyšl, Ходському святі та в прямому ефірі «Концерту для життя II» на TV Noe. Художня керівниця: Mgr. Катерина Михайлова.",
            foot_press="Для медіа", other_perf="Інші виступи"),
 "en": dict(nav_news="News", news_k="News", news_h="What’s new", more="Read more", back="← Back to the home page", all_news="More news", all_btn="All news", arch_desc="News from Kupava, the Ukrainian folk ensemble from Brno – performances, festivals and concerts.",
            press_k="For media and organisers", press_h="Press kit",
            press_p="High-resolution photographs, logo and a short biography of the ensemble for festival programmes, posters and press releases. When using the photographs, please credit “Kupava ensemble”.",
            bio_h="Short biography", copy="Copy text", copied="Copied",
            dl_zip="Complete press kit (ZIP)", dl_logo="Logo (PNG)", dl_bio="Biographies CZ / UA / EN (TXT)", dl_photos="Photographs",
            bio="Kupava is a Ukrainian folk ensemble from Brno, Czech Republic, founded in February 2023. It is dedicated to traditional Ukrainian polyphonic singing and folk music from many regions of Ukraine, performed in the original language, in traditional dress and with live music. The ensemble has performed at the Strážnice International Folklore Festival, Smetana’s Litomyšl, the Chod Festival and in the live TV Noe broadcast of Concert for Life II. Artistic director: Kateryna Mykhaylova.",
            foot_press="Press kit", other_perf="Other performances"),
}
PRESS_PHOTOS = [("soubor-portret","Kupava – skupinový portrét / group portrait"),("vanoce-viden-2023","Staroukrajinské Vánoce / Old Ukrainian Christmas"),
                ("program-regiony","Kupava na pódiu / on stage"),("koledy-moravske-namesti","Koledování v Brně / Carolling in Brno"),("festival-podium","Festivalové vystoupení / Festival performance")]
N_PAST = len(PAST)

MONTHS = {"cs": ["ledna","února","března","dubna","května","června","července","srpna","září","října","listopadu","prosince"],
          "uk": ["січня","лютого","березня","квітня","травня","червня","липня","серпня","вересня","жовтня","листопада","грудня"],
          "en": ["January","February","March","April","May","June","July","August","September","October","November","December"]}
def fdate(ev, lang, year=True):
    y, m, d = map(int, ev["date"].split("-")); M = MONTHS[lang][m-1]
    d1 = f"{d}." if lang == "cs" else f"{d}"
    if "end" in ev:
        d2 = int(ev["end"].split("-")[2])
        s = f"{d}.–{d2}. {M}" if lang == "cs" else f"{d}–{d2} {M}"
    else:
        s = f"{d1} {M}"
    return f"{s} {y}" if year else s

REPERTOIRE = [
 ("Зеленеє жито, зелене", "Zelené žito, zelené", "Green Rye, So Green"),
 ("Через сад-виноград", "Přes sad a vinohrad", "Through the Orchard and Vineyard"),
 ("Ой, ти, ніченько-чарівниченько", "Ach, ty noci kouzelná", "Oh, Enchanting Night"),
 ("Ой, устану ранесенько", "Ach, vstanu časně zrána", "Oh, I’ll Rise at Dawn"),
 ("Висить ябко", "Visí jablíčko", "The Apple Hangs"),
 ("Добрий вечір тобі, пане господарю", "Dobrý večer, pane hospodáři", "Good Evening, Master of the House"),
 ("Щедрівочка щедрувала", "Koledovala ščedrivočka", "The Little Shchedrivka Went Singing"),
 ("Роди, Боже, жито", "Dej, Bože, úrodu žita", "Lord, Let the Rye Grow"),
 ("Господарський двір на семи стовпах", "Hospodářův dvůr na sedmi sloupech", "The Farmstead on Seven Pillars"),
 ("Славен єси", "Buď pochválen", "Glory Be to You"),
 ("Ой чи є, чи нема пан господар дома?", "Je-li, či není hospodář doma?", "Is the Master at Home?"),
 ("Хай Ісус, мале дитя", "Ať Ježíšek, malé dítě", "May Little Jesus"),
]

# Významná vystoupení s vlastní fotografií z dané akce (klíč = název akce v češtině, fotka v img/g/)
FEATURED_IMG = {
 "Mezinárodní folklorní festival Strážnice": "soubor-straznice",
 "Koncert pro život II – přímý přenos TV Noe": "vinky",
 "Staroukrajinské Vánoce v kostele sv. Josefa": "koledy-sv-josef",
 "Koleda ve Vídni": "viden-hvezda-2025",
 "Mezinárodní folklorní festival Lidový rok": "lidovy-rok-2026",
 "Smetanova Litomyšl – Festivalové zahrady": "smetanova-litomysl-2026",
}

VIDEOS = [
 ("a9-As9ocu7A", "Ой, устану ранесенько", {"cs":"Babylonfest, Brno 2023","uk":"Babylonfest, Брно 2023","en":"Babylonfest, Brno 2023"}),
 ("fvsroGsIgNk", "Славен єси", {"cs":"Ukrajinské koledy","uk":"Українські колядки","en":"Ukrainian carols"}),
 ("ptXL8v-0SIU", "Зеленеє жито, зелене", {"cs":"Babylonfest, Brno 2023","uk":"Babylonfest, Брно 2023","en":"Babylonfest, Brno 2023"}),
]

GALLERY = [
 ("soubor-prerov", {"cs":"Kupava v Přerově","uk":"«Купава» у Пршерові","en":"Kupava in Přerov"}),
 ("festival-podium", {"cs":"Den národnostních menšin Jihomoravského kraje","uk":"День національних меншин Південноморавського краю","en":"South Moravian National Minorities Day"}),
 ("koledy-podium-kostel", {"cs":"Staroukrajinské Vánoce","uk":"Староукраїнське Різдво","en":"Old Ukrainian Christmas"}),
 ("housle-podium", {"cs":"Živá hudba na pódiu","uk":"Жива музика на сцені","en":"Live music on stage"}),
 ("viden-hvezda-2025", {"cs":"Koledy ve Vídni 2025","uk":"Колядки у Відні 2025","en":"Carols in Vienna 2025"}),
 ("zpev-radost", {"cs":"Vícehlasý zpěv","uk":"Багатоголосий спів","en":"Polyphonic singing"}),
 ("koledy-moravske-namesti", {"cs":"Vánoční koledování v Brně","uk":"Різдвяне колядування в Брно","en":"Christmas carolling in Brno"}),
 ("podium-celek", {"cs":"Kupava na festivalovém pódiu","uk":"«Купава» на фестивальній сцені","en":"Kupava on a festival stage"}),
 ("palac-hvezda-2024", {"cs":"Vánoční koncert v Paláci šlechtičen","uk":"Різдвяний концерт у Палаці шляхетних панн","en":"Christmas concert at the Palace of Noblewomen"}),
 ("vinky", {"cs":"Koncert pro život II, TV Noe","uk":"«Концерт для життя II», TV Noe","en":"Concert for Life II, TV Noe"}),
 ("zpevacky-podium", {"cs":"Zpěvačky v krojích","uk":"Співачки у строях","en":"Singers in traditional dress"}),
 ("podium-tanec", {"cs":"Písně a tanec na pódiu","uk":"Пісні й танець на сцені","en":"Songs and dance on stage"}),
]

T = {
"cs": dict(
  title="Kupava – ukrajinský folklorní soubor z Brna",
  h1_pre="Ukrajinský folklorní soubor",
  desc="Ukrajinský folklorní soubor Kupava z Brna – vícehlasý zpěv, živá lidová hudba a kroje. Vystoupení na festivalech, koncertech a v TV Noe. Kontakt pro pořadatele.",
  brand_sub="ukrajinský folklorní soubor",
  nav=[("#o-nas","O nás"),("#repertoar","Repertoár"),("#vystoupeni","Vystoupení"),("#video","Video"),("#galerie","Galerie")],
  nav_cta="Kontakt",
  eyebrow="Ukrajinský folklorní soubor · Brno",
  lead="Tradiční vícehlasý zpěv a živá lidová hudba z různých regionů Ukrajiny.",
  cta1="Poslechnout si nás", cta2="Napište nám",
  photo_alt="Ukrajinský folklorní soubor Kupava v krojích",
  stats=[("2023","založení souboru"),(str(N_PAST),"vystoupení"),("10+","folklorních festivalů"),("3","země – Česko, Slovensko, Rakousko")],
  stages_k="Vystupovali jsme mimo jiné",
  stages=["MFF Strážnice","Smetanova Litomyšl","Chodské slavnosti","Jánošíkov dukát","TV Noe"],
  about_k="O nás", about_h="Píseň, která spojuje",
  about_p=[
   "Ukrajinský folklorní soubor <b>Kupava</b> vznikl v únoru 2023 v Brně za podpory Ukrajinského centra v Brně. Věnujeme se tradičnímu ukrajinskému vícehlasému zpěvu a lidové hudbě z různých regionů Ukrajiny – zpíváme v originále, v krojích a za doprovodu živé hudby.",
   "Soubor tvoří Ukrajinky dlouhodobě žijící v Česku, ženy, které musely odejít z Ukrajiny po ruské invazi v roce 2022, i Češi, kteří mají ukrajinský folklór rádi."],
  director="Umělecká vedoucí", director_name="Mgr. Kateryna Mykhaylova",
  name_note="Kupava je staré slovanské jméno – „krásná, slavnostně oblečená“ nebo „žena s ladnou a hrdou chůzí“.",
  pillars_h="Naše poslání",
  pillars=[("Uchováváme","Studujeme a uchováváme ukrajinské lidové písně, hudbu a tradiční kroje."),
           ("Představujeme","Přinášíme ukrajinský folklór na pódia festivalů, do koncertních sálů i kostelů."),
           ("Spojujeme","Podporujeme setkávání a porozumění mezi ukrajinskou a českou kulturou.")],
  tv_k="Koncert pro život II", tv_h="Živě na TV Noe",
  tv_p="V dubnu 2025 vystoupila Kupava v kostele sv. Václava v Ostravě na benefičním Koncertu pro život II, který živě vysílala TV Noe. Spolu s písničkářem Pavlem Helanem, česko-ukrajinským sborem Sonjašnyk a dětským sborem Spivanočky jsme podpořili rehabilitaci válečných veteránů a zraněných dětí z Ukrajiny – diváci přispěli 200 000 Kč.",
  tv_meta="6. dubna 2025 · Ostrava · TV Noe",
  rep_k="Repertoár", rep_h="Koncertní programy",
  progs=[("vanoce-viden-2023","Staroukrajinské Vánoce","Koledy a ščedrivky s vánoční hvězdou. Sváteční program, který každoročně uvádíme v Brně a ve Vídni."),
         ("program-regiony","Písně ukrajinských regionů","Lyrické, obřadní a taneční písně v tradičním vícehlasu s živou hudbou – pro festivaly, koncertní sály a kulturní události.")],
  rep_list="Z repertoáru", rep_note="Písně zpíváme v ukrajinštině; uvádíme český překlad názvu.",
  perf_k="Vystoupení", perf_h="Významná vystoupení", up_k="Připravujeme",
  perf_note=f"Celkem {N_PAST} vystoupení od roku 2023 – festivaly, koncerty a komunitní akce v Česku, na Slovensku a v Rakousku.",
  quote="„Zaplněný kostel v Brně si užil atmosféru staroukrajinských Vánoc.“", quote_src="ČTK / České noviny, 5. 1. 2025",
  vid_k="Video", vid_h="Poslechněte si nás", vid_more="Další záznamy na YouTube",
  gal_k="Galerie", gal_h="Z našich vystoupení",
  con_k="Kontakt", con_h="Pojďme spolupracovat",
  con_p="Máte zájem o vystoupení souboru Kupava, potřebujete bližší informace, nebo máte nápad na společný projekt? Kontaktujte nás.",
  open_form="Napsat zprávu", close="Zavřít", form_h="Napište nám",
  f=dict(name="Jméno",email="E-mail",org="Organizace / akce (nepovinné)",msg="Zpráva",send="Odeslat zprávu",sending="Odesílám…",
         gdpr="Údaje použijeme pouze k odpovědi na vaši zprávu.",ok="Děkujeme, vaše zpráva byla odeslána. Odpovíme vám co nejdříve.",
         err="Zprávu se nepodařilo odeslat. Napište nám prosím přímo na kupava@kupavabrno.cz.",subject="Zpráva z webu kupavabrno.cz"),
  con_labels=("E-mail","Telefon","Sledujte nás"),
  foot_seat="Sídlo: Městečko 68, 664 61 Rajhrad", foot_reg="IČO 23686766 · spolek zapsaný u Krajského soudu v Brně, L 31074",
),
"uk": dict(
  title="Купава – український фольклорний ансамбль у Брно, Чехія",
  h1_pre="Український фольклорний ансамбль",
  desc="Український фольклорний ансамбль «Купава» з Брно (Чехія): багатоголосий спів, жива народна музика та строї. Фестивалі, концерти, TV Noe. Контакти.",
  brand_sub="український фольклорний ансамбль",
  nav=[("#o-nas","Про нас"),("#repertoar","Репертуар"),("#vystoupeni","Виступи"),("#video","Відео"),("#galerie","Галерея")],
  nav_cta="Контакти",
  eyebrow="Український фольклорний ансамбль · Брно",
  lead="Традиційний багатоголосий спів і жива народна музика з різних регіонів України.",
  cta1="Послухати нас", cta2="Напишіть нам",
  photo_alt="Український фольклорний ансамбль «Купава» у народних строях",
  stats=[("2023","рік заснування"),(str(N_PAST),"виступів"),("10+","фольклорних фестивалів"),("3","країни – Чехія, Словаччина, Австрія")],
  stages_k="Ми виступали, зокрема",
  stages=["МФФ у Стражніце","Smetanova Litomyšl","Ходське свято","Яношіків дукат","TV Noe"],
  about_k="Про нас", about_h="Пісня, що єднає",
  about_p=[
   "Український фольклорний ансамбль <b>«Купава»</b> заснований у лютому 2023 року в Брно за підтримки Українського центру в Брно. Ми присвячуємо себе традиційному українському багатоголосому співу та народній музиці з різних регіонів України – співаємо в оригіналі, у строях, під живу музику.",
   "В ансамблі співають українки, які давно живуть у Чехії, жінки, що були змушені покинути Україну після російського вторгнення 2022 року, а також чехи, які люблять український фольклор."],
  director="Художня керівниця", director_name="Mgr. Катерина Михайлова",
  name_note="Купава – давнє слов’янське ім’я: «гарна, святково вбрана» або «жінка з легкою і гордою ходою».",
  pillars_h="Наша місія",
  pillars=[("Зберігаємо","Досліджуємо й зберігаємо українські народні пісні, музику та традиційні строї."),
           ("Представляємо","Виносимо український фольклор на сцени фестивалів, у концертні зали й храми."),
           ("Єднаємо","Підтримуємо зустрічі та порозуміння між українською і чеською культурами.")],
  tv_k="Концерт для життя II", tv_h="Наживо на TV Noe",
  tv_p="У квітні 2025 року «Купава» виступила в храмі св. Вацлава в Остраві на благодійному «Концерті для життя II», який наживо транслювало TV Noe. Разом зі співаком Павлом Геланом, чесько-українським хором «Соняшник» і дитячим хором «Співаночки» ми підтримали реабілітацію ветеранів війни та поранених дітей з України – глядачі пожертвували 200 000 крон.",
  tv_meta="6 квітня 2025 · Острава · TV Noe",
  rep_k="Репертуар", rep_h="Концертні програми",
  progs=[("vanoce-viden-2023","Староукраїнське Різдво","Колядки й щедрівки з різдвяною зіркою. Святкова програма, яку ми щороку представляємо в Брно та Відні."),
         ("program-regiony","Пісні українських регіонів","Ліричні, обрядові й танцювальні пісні в традиційному багатоголоссі з живою музикою – для фестивалів, концертних залів і культурних подій.")],
  rep_list="З репертуару", rep_note="Ми співаємо українською, в оригінальному звучанні.",
  perf_k="Виступи", perf_h="Визначні виступи", up_k="Найближчі виступи",
  perf_note=f"Загалом {N_PAST} виступів з 2023 року – фестивалі, концерти й громадські події в Чехії, Словаччині та Австрії.",
  quote="«Повний храм у Брно поринув в атмосферу староукраїнського Різдва.»", quote_src="ЧТК / České noviny, 05.01.2025 (переклад)",
  vid_k="Відео", vid_h="Послухайте нас", vid_more="Більше записів на YouTube",
  gal_k="Галерея", gal_h="З наших виступів",
  con_k="Контакти", con_h="Співпрацюймо",
  con_p="Бажаєте запросити ансамбль «Купава», отримати детальнішу інформацію або маєте ідею для спільного проєкту? Зв’яжіться з нами.",
  open_form="Написати повідомлення", close="Закрити", form_h="Напишіть нам",
  f=dict(name="Ім’я",email="E-mail",org="Організація / подія (необов’язково)",msg="Повідомлення",send="Надіслати",sending="Надсилаю…",
         gdpr="Ваші дані використаємо лише для відповіді.",ok="Дякуємо, повідомлення надіслано. Ми відповімо якнайшвидше.",
         err="Не вдалося надіслати. Напишіть нам, будь ласка, на kupava@kupavabrno.cz.",subject="Повідомлення з сайту kupavabrno.cz"),
  con_labels=("E-mail","Телефон","Соцмережі"),
  foot_seat="Адреса: Městečko 68, 664 61 Rajhrad", foot_reg="IČO 23686766 · спілка зареєстрована Крайовим судом у Брно, L 31074",
),
"en": dict(
  title="Kupava – Ukrainian Folk Ensemble from Brno, Czechia",
  h1_pre="Ukrainian folk ensemble",
  desc="Kupava is a Ukrainian folk ensemble from Brno, Czech Republic – polyphonic singing, live folk music and costume. Festivals, concerts, TV Noe. Contact us.",
  brand_sub="Ukrainian folk ensemble",
  nav=[("#o-nas","About"),("#repertoar","Repertoire"),("#vystoupeni","Performances"),("#video","Video"),("#galerie","Gallery")],
  nav_cta="Contact",
  eyebrow="Ukrainian folk ensemble · Brno, Czech Republic",
  lead="Traditional Ukrainian polyphonic singing and live folk music from many regions of Ukraine.",
  cta1="Listen to us", cta2="Get in touch",
  photo_alt="The Kupava Ukrainian folk ensemble in traditional dress",
  stats=[("2023","founded"),(str(N_PAST),"performances"),("10+","folklore festivals"),("3","countries – Czechia, Slovakia, Austria")],
  stages_k="Stages we have performed on include",
  stages=["Strážnice Folklore Festival","Smetana’s Litomyšl","Chod Festival","Jánošík’s Ducat","TV Noe"],
  about_k="About us", about_h="Songs that connect",
  about_p=[
   "The Ukrainian folk ensemble <b>Kupava</b> was founded in February 2023 in Brno, Czech Republic, with the support of the Ukrainian Centre in Brno. We are dedicated to traditional Ukrainian polyphonic singing and folk music from many regions of Ukraine – sung in the original, in traditional dress and with live music.",
   "The ensemble brings together Ukrainian women long settled in the Czech Republic, women who had to leave Ukraine after the Russian invasion in 2022, and Czechs who love Ukrainian folklore."],
  director="Artistic director", director_name="Kateryna Mykhaylova",
  name_note="Kupava is an old Slavic name meaning “beautiful, festively dressed” or “a woman with a graceful, proud walk”.",
  pillars_h="Our mission",
  pillars=[("We preserve","We study and preserve Ukrainian folk songs, music and traditional costume."),
           ("We present","We bring Ukrainian folklore to festival stages, concert halls and churches."),
           ("We connect","We foster encounters and understanding between Ukrainian and Czech culture.")],
  tv_k="Concert for Life II", tv_h="Live on TV Noe",
  tv_p="In April 2025 Kupava performed at St Wenceslas Church in Ostrava in the charity Concert for Life II, broadcast live by TV Noe. Together with singer-songwriter Pavel Helan, the Czech-Ukrainian choir Sonjašnyk and the Spivanočky children’s choir we supported the rehabilitation of war veterans and injured children from Ukraine – viewers donated CZK 200,000.",
  tv_meta="6 April 2025 · Ostrava · TV Noe",
  rep_k="Repertoire", rep_h="Concert programmes",
  progs=[("vanoce-viden-2023","Old Ukrainian Christmas","Carols and shchedrivky with the Christmas star – a festive programme we present every year in Brno and Vienna."),
         ("program-regiony","Songs of Ukraine’s Regions","Lyrical, ritual and dance songs in traditional polyphony with live music – for festivals, concert halls and cultural events.")],
  rep_list="From our repertoire", rep_note="We sing in Ukrainian; English translations of the titles are given.",
  perf_k="Performances", perf_h="Selected performances", up_k="Upcoming",
  perf_note=f"{N_PAST} performances since 2023 in total – festivals, concerts and community events in Czechia, Slovakia and Austria.",
  quote="“A packed church in Brno enjoyed the atmosphere of an old Ukrainian Christmas.”", quote_src="Czech News Agency (ČTK), 5 Jan 2025 (translated)",
  vid_k="Video", vid_h="Listen to us", vid_more="More recordings on YouTube",
  gal_k="Gallery", gal_h="From our performances",
  con_k="Contact", con_h="Let’s work together",
  con_p="Interested in a performance by Kupava, need further information, or have an idea for a joint project? Please get in touch.",
  open_form="Send a message", close="Close", form_h="Write to us",
  f=dict(name="Name",email="E-mail",org="Organisation / event (optional)",msg="Message",send="Send message",sending="Sending…",
         gdpr="We will use your details only to reply to your message.",ok="Thank you, your message has been sent. We will get back to you soon.",
         err="Your message could not be sent. Please write to us at kupava@kupavabrno.cz.",subject="Message from kupavabrno.cz"),
  con_labels=("E-mail","Phone","Follow us"),
  foot_seat="Registered office: Městečko 68, 664 61 Rajhrad, Czech Republic", foot_reg="Reg. no. 23686766 · association registered at the Regional Court in Brno, L 31074",
)}

ORN = '<svg class="orn" viewBox="0 0 150 24" aria-hidden="true"><g fill="currentColor"><path d="M8 11.25h46v1.5H8zM96 11.25h46v1.5H96z"/><circle cx="62" cy="12" r="1.6"/><circle cx="88" cy="12" r="1.6"/><g transform="translate(45 0)"><path d="M33.05 13.26L35.88 16.49L40.16 16.21L37.33 12.98ZM31.26 15.05L30.98 19.33L34.21 22.16L34.49 17.88ZM28.74 15.05L25.51 17.88L25.79 22.16L29.02 19.33ZM26.95 13.26L22.67 12.98L19.84 16.21L24.12 16.49ZM26.95 10.74L24.12 7.51L19.84 7.79L22.67 11.02ZM28.74 8.95L29.02 4.67L25.79 1.84L25.51 6.12ZM31.26 8.95L34.49 6.12L34.21 1.84L30.98 4.67ZM33.05 10.74L37.33 11.02L40.16 7.79L35.88 7.51Z"/><circle cx="30" cy="12" r="1.6"/></g></g></svg>'

def page(lang):
    t = T[lang]; pre = "" if lang == "cs" else "../"
    home = pre + ("" if lang == "cs" else lang + "/") or "./"
    name = "Купава" if lang == "uk" else "Kupava"
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in LANGS.items())
    SAME = ["https://www.facebook.com/KupavaBrno","https://www.instagram.com/soubor_kupava/","https://www.youtube.com/playlist?list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5"]
    INLANG = {"cs":"cs-CZ","uk":"uk-UA","en":"en"}[lang]
    group = {"@type":["MusicGroup","PerformingGroup"],"@id":BASE+"/#kupava","name":"Kupava","alternateName":["Купава","Kupava Brno","Ukrajinský folklorní soubor Kupava"],
          "legalName":"Ukrajinský folklorní soubor KUPAVA, z.s.","description":t["desc"],"url":BASE+"/","logo":BASE+"/img/logo.png","image":BASE+"/img/soubor-portret.jpg",
          "genre":["Ukrainian folk music","Folk","Polyphonic singing"],"foundingDate":"2023-02","foundingLocation":{"@type":"Place","name":"Brno"},
          "identifier":{"@type":"PropertyValue","propertyID":"IČO","value":"23686766"},"nonprofitStatus":"Nonprofit",
          "email":"kupava@kupavabrno.cz","telephone":"+420777072433",
          "address":{"@type":"PostalAddress","streetAddress":"Městečko 68","postalCode":"66461","addressLocality":"Rajhrad","addressCountry":"CZ"},
          "areaServed":["CZ","SK","AT","Europe"],"sameAs":SAME}
    events = [{"@type":"MusicEvent","name":ev[lang],"startDate":ev["date"],"endDate":ev.get("end",ev["date"]),"eventStatus":"https://schema.org/EventScheduled",
               "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","location":{"@type":"Place","name":ev["place"][lang],"address":ev["place"][lang]},
               "performer":{"@id":BASE+"/#kupava"},"organizer":{"@id":BASE+"/#kupava"},"image":BASE+"/img/soubor-portret.jpg","url":BASE+LANGS[lang]+"#vystoupeni"} for ev in UPCOMING]
    ld = {"@context":"https://schema.org","@graph":[group,
          {"@type":"WebSite","@id":BASE+"/#web","url":BASE+"/","name":"Kupava","inLanguage":["cs-CZ","uk-UA","en"],"publisher":{"@id":BASE+"/#kupava"}},
          {"@type":"WebPage","url":BASE+LANGS[lang],"name":t["title"],"description":t["desc"],"inLanguage":INLANG,"isPartOf":{"@id":BASE+"/#web"},"about":{"@id":BASE+"/#kupava"},
           "primaryImageOfPage":BASE+"/img/soubor-portret.jpg"}] + events}
    x = X[lang]
    nav = "".join(f'<a href="{h}">{e(n)}</a>' for h, n in t["nav"][:3]) + f'<a href="#aktuality">{e(x["nav_news"])}</a>' + "".join(f'<a href="{h}">{e(n)}</a>' for h, n in t["nav"][3:])
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join('<a href="' + (pre + ("" if l=="cs" else l+"/") or "./") + f'" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    stats = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in t["stats"])
    stages = "".join(f'<li>{e(s)}</li>' for s in t["stages"])
    about = "".join(f"<p>{p}</p>" for p in t["about_p"])
    pillars = "".join(f'<div class="pillar"><span class="num">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(t["pillars"]))
    progs = "".join(f'<article class="prog"><div class="prog-img"><img src="{pre}img/g/{img}.jpg" alt="{e(h)}" loading="lazy" width="760" height="506"></div><div class="prog-body"><span class="prog-n">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></div></article>' for i, (img, h, p) in enumerate(t["progs"]))
    rep = "".join(f'<li><span class="sn">{i+1:02d}</span><b lang="uk">{e(o)}</b>' + ('' if lang == "uk" else f'<small>{e(c if lang=="cs" else en)}</small>') + '</li>' for i, (o, c, en) in enumerate(REPERTOIRE))
    # významná vystoupení: karty s fotkou (stejnojmenné akce sloučené, např. Strážnice 2023 a 2025) + zbytek v seznamu
    groups = {}
    for ev in HIGHLIGHTS:
        groups.setdefault(ev["cs"], []).append(ev)
    feat, rest = [], []
    for name_cs, evs in groups.items():
        (feat if name_cs in FEATURED_IMG else rest).append((name_cs, evs))
    def when(evs):
        if len(evs) > 1:
            ys = sorted({ev["date"][:4] for ev in evs})
            return (" a " if lang == "cs" else " і " if lang == "uk" else " and ").join(ys)
        return fdate(evs[0], lang)
    cards = "".join(f'<article class="feat"><div class="feat-img"><img src="{pre}img/g/{FEATURED_IMG[n]}.jpg" alt="{e(evs[0][lang])}" loading="lazy" width="760" height="506"></div><div class="feat-body"><time>{e(when(evs))}</time><h3>{e(evs[0][lang])}</h3><p>{e(evs[0]["place"][lang])}</p></div></article>' for n, evs in feat)
    hl = "".join(f'<li><time>{e(when(evs))}</time><b>{e(evs[0][lang])}</b><span>{e(evs[0]["place"][lang])}</span></li>' for n, evs in rest)
    up = ""
    if UPCOMING:
        up = f'<div class="upcoming"><p class="kicker">{e(t["up_k"])}</p><ul>' + "".join(f'<li><time>{e(fdate(ev, lang))}</time><b>{e(ev[lang])}</b><span>{e(ev["place"][lang])}</span></li>' for ev in UPCOMING) + '</ul></div>'
    vids = "".join(f'<div class="vid"><button class="yt" data-id="{vid}" aria-label="{e(title)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"></button><p><b lang="uk">{e(title)}</b><span>{e(sub[lang])}</span></p></div>' for vid, title, sub in VIDEOS)
    gal = "".join(f'<a href="{pre}img/{s}.jpg"><img src="{pre}img/g/{s}.jpg" alt="{e(a[lang])}" loading="lazy"></a>' for s, a in GALLERY)
    f = t["f"]; l1, l2, l3 = t["con_labels"]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="theme-color" content="#1c2f5a">
<link rel="canonical" href="{BASE}{LANGS[lang]}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:image" content="{BASE}/img/soubor-portret.jpg">
<meta property="og:url" content="{BASE}{LANGS[lang]}">
<meta property="og:site_name" content="Kupava">
<meta property="og:image:width" content="2048"><meta property="og:image:height" content="1365">
<meta property="og:image:alt" content="{e(t["photo_alt"])}">
<meta property="og:locale" content="{ {"cs":"cs_CZ","uk":"uk_UA","en":"en_GB"}[lang] }">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/icon-192.png">
<link rel="apple-touch-icon" href="{pre}img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;700;800&display=swap&subset=cyrillic,latin-ext" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#o-nas">Skip</a>
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <button class="menu-btn" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
 <nav class="nav">{nav}<span class="lang">{langs}</span><a class="btn small primary" href="#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>

<section class="hero">
 <div class="wrap hero-text">
  <h1><span class="eyebrow">{e(t["eyebrow"])}</span><span class="h1-name">{name}</span></h1>
  {ORN}
  <p class="lead">{e(t["lead"])}</p>
  <div class="btns"><a class="btn light" href="#video">▶ {e(t["cta1"])}</a><a class="btn outline-light" href="#kontakt" data-open-form>{e(t["cta2"])}</a></div>
 </div>
 <figure class="hero-photo wrap"><img src="{pre}img/soubor-portret.jpg" srcset="{pre}img/soubor-portret-1200.jpg 1200w, {pre}img/soubor-portret.jpg 2048w" sizes="(max-width:1300px) 100vw, 1240px" alt="{e(t["photo_alt"])}" width="2048" height="1365" fetchpriority="high"></figure>
</section>

<section class="stats-sec"><div class="wrap">
 <div class="stats">{stats}</div>
 <div class="stages"><p>{e(t["stages_k"])}</p><ul>{stages}</ul></div>
</div></section>

<section id="o-nas"><div class="wrap about">
 <div class="about-text">
  <p class="kicker">{e(t["about_k"])}</p>
  <h2>{e(t["about_h"])}</h2>
  {about}
  <p class="director"><span>{e(t["director"])}</span><b>{e(t["director_name"])}</b></p>
  <p class="name-note">{e(t["name_note"])}</p>
 </div>
 <div class="about-pic"><img src="{pre}img/zpev-podium.jpg" alt="{e(GALLERY[1][1][lang])}" loading="lazy"></div>
</div>
<div class="wrap mission"><h3 class="mission-h">{e(t["pillars_h"])}</h3><div class="pillars">{pillars}</div></div>
</section>

<section class="tv"><div class="wrap tv-grid">
 <div class="tv-pic"><img src="{pre}img/vinky.jpg" alt="{e(t["tv_h"])}" loading="lazy"></div>
 <div>
  <p class="kicker">{e(t["tv_k"])}</p>
  <h2>{e(t["tv_h"])}</h2>
  <p>{e(t["tv_p"])}</p>
  <p class="tv-meta">{e(t["tv_meta"])}</p>
 </div>
</div></section>

<section id="repertoar"><div class="wrap">
 <p class="kicker">{e(t["rep_k"])}</p>
 <h2>{e(t["rep_h"])}</h2>
 <div class="progs">{progs}</div>
 <div class="songs">
  <div class="songs-head"><h3>{e(t["rep_list"])}</h3><p>{e(t["rep_note"])}</p></div>
  <ol class="song-grid">{rep}</ol>
  <p class="songs-more"><a class="link" href="#video">▶ {e(t["vid_h"])}</a></p>
 </div>
</div></section>

<section id="vystoupeni" class="soft"><div class="wrap">
 <div class="sec-head"><div><p class="kicker">{e(t["perf_k"])}</p><h2>{e(t["perf_h"])}</h2></div><p class="perf-note">{e(t["perf_note"])}</p></div>
 {up}
 <div class="feats">{cards}</div>
 <div class="perf-grid">
  <div><h3 class="sub-h">{e(X[lang]["other_perf"])}</h3><ul class="hl">{hl}</ul></div>
  <blockquote>{e(t["quote"])}<cite><a href="https://www.ceskenoviny.cz/zpravy/2616128" target="_blank" rel="noopener">{e(t["quote_src"])}</a></cite></blockquote>
 </div>
</div></section>

{news_section(lang, pre)}

<section id="video"><div class="wrap">
 <div class="sec-head"><div><p class="kicker">{e(t["vid_k"])}</p><h2>{e(t["vid_h"])}</h2></div><a class="link" href="https://www.youtube.com/watch?v=qvbnvvhpYXQ&amp;list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5" target="_blank" rel="noopener">{e(t["vid_more"])} ↗</a></div>
 <div class="videos">{vids}</div>
</div></section>

<section id="galerie" class="soft"><div class="wrap">
 <p class="kicker">{e(t["gal_k"])}</p>
 <h2>{e(t["gal_h"])}</h2>
 <div class="gallery">{gal}</div>
</div></section>

{press_section(lang, pre)}

<section id="kontakt" class="contact"><div class="wrap contact-grid">
 <div>
  <p class="kicker">{e(t["con_k"])}</p>
  <h2>{e(t["con_h"])}</h2>
  <p class="con-p">{e(t["con_p"])}</p>
  <button class="btn primary big" type="button" data-open-form>✉ {e(t["open_form"])}</button>
 </div>
 <div>
  <dl class="con-list">
   <div><dt>{e(l1)}</dt><dd><a href="mailto:kupava@kupavabrno.cz">kupava@kupavabrno.cz</a></dd></div>
   <div><dt>{e(l2)}</dt><dd><a href="tel:+420777072433">+420 777 072 433</a></dd></div>
   <div><dt>{e(l3)}</dt><dd><a href="https://www.facebook.com/KupavaBrno" target="_blank" rel="noopener">Facebook</a> · <a href="https://www.instagram.com/soubor_kupava/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.youtube.com/watch?v=ptXL8v-0SIU&amp;list=PLs8RLUolQE94FKIigKi2Ps-FzuV7cxNQO" target="_blank" rel="noopener">YouTube</a></dd></div>
  </dl>
 </div>
</div></section>

<dialog id="form-dialog" class="form-dialog" aria-labelledby="form-h">
 <button class="dlg-x" type="button" aria-label="{e(t["close"])}" data-close-form>×</button>
 <h2 id="form-h">{e(t["form_h"])}</h2>
 <form id="contact-form" class="form" action="{FORM_ENDPOINT}" method="post" data-sending="{e(f["sending"])}" data-send="{e(f["send"])}" data-ok="{e(f["ok"])}" data-err="{e(f["err"])}">
  <input type="hidden" name="_subject" value="{e(f["subject"])}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="jazyk" value="{lang}">
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <label>{e(f["name"])}<input name="jmeno" required autocomplete="name"></label>
  <label>{e(f["email"])}<input name="email" type="email" required autocomplete="email"></label>
  <label class="full">{e(f["org"])}<input name="organizace" autocomplete="organization"></label>
  <label class="full">{e(f["msg"])}<textarea name="zprava" required rows="5"></textarea></label>
  <button class="btn primary full" type="submit">{e(f["send"])}</button>
  <p class="full form-note">{e(f["gdpr"])}</p>
  <p class="full form-status" role="status" aria-live="polite"></p>
 </form>
</dialog>

<footer><div class="wrap foot">
 <div><b>Ukrajinský folklorní soubor KUPAVA, z.s.</b><br>{e(t["foot_seat"])}<br>{e(t["foot_reg"])}</div>
 <div class="lang">{langs}</div>
</div></footer>

<div class="lb" role="dialog" aria-modal="true"><button class="x" aria-label="×">×</button><button class="p" aria-label="‹">‹</button><img alt=""><button class="n" aria-label="›">›</button></div>
<script src="{pre}assets/site.js?v={VER}"></script>
</body>
</html>
'''

def fmt_post_date(d, lang):
    y, m, dd = map(int, d.split("-"))
    return f"{dd}. {MONTHS[lang][m-1]} {y}" if lang == "cs" else f"{dd} {MONTHS[lang][m-1]} {y}"

def news_section(lang, pre):
    x = X[lang]
    cards = "".join(f'''<article class="news-card"><a href="aktuality/{po['slug']}/"><img src="{pre}img/g/{po['image']}.jpg" alt="" loading="lazy" width="760" height="506"></a><div><time datetime="{po.get('event_date', po['date'])}">{e(fmt_post_date(po.get('event_date', po['date']), lang))}</time><h3><a href="aktuality/{po['slug']}/">{e(po[lang]['title'])}</a></h3><p>{e(po[lang]['perex'])}</p><a class="link" href="aktuality/{po['slug']}/">{e(x['more'])} →</a></div></article>''' for po in POSTS[:4])
    return f'''<section id="aktuality"><div class="wrap">
 <p class="kicker">{e(x["news_k"])}</p>
 <h2>{e(x["news_h"])}</h2>
 <div class="news news4">{cards}</div>
 <p class="news-all"><a class="btn outline" href="aktuality/">{e(x["all_btn"])} →</a></p>
</div></section>'''

def press_section(lang, pre):
    x = X[lang]
    photos = "".join(f'<li><a href="{pre}img/{f}.jpg" download>{e(c)}</a></li>' for f, c in PRESS_PHOTOS)
    return f'''<section id="pro-media" class="soft"><div class="wrap press">
 <div>
  <p class="kicker">{e(x["press_k"])}</p>
  <h2>{e(x["press_h"])}</h2>
  <p>{e(x["press_p"])}</p>
  <ul class="dl">
   <li><a class="btn primary" href="{pre}press/kupava-press-kit.zip" download>⬇ {e(x["dl_zip"])}</a></li>
   <li><a href="{pre}img/logo.png" download>{e(x["dl_logo"])}</a></li>
   <li><a href="{pre}press/kupava-medailonky.txt" download>{e(x["dl_bio"])}</a></li>
  </ul>
  <p class="dl-h">{e(x["dl_photos"])}</p>
  <ul class="dl small">{photos}</ul>
 </div>
 <div class="bio-box">
  <h3>{e(x["bio_h"])}</h3>
  <p id="bio-{lang}">{e(x["bio"])}</p>
  <button class="btn small outline" type="button" data-copy="bio-{lang}" data-copied="{e(x["copied"])}">{e(x["copy"])}</button>
 </div>
</div></section>'''

def article(lang, po):
    t = T[lang]; x = X[lang]; P = po[lang]
    depth = 2 if lang == "cs" else 3
    pre = "../" * depth
    name = "Купава" if lang == "uk" else "Kupava"
    url = BASE + post_url(lang, po["slug"])
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{post_url(l, po["slug"])}">' for l in LANGS)
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join(f'<a href="{pre}{post_url(l, po["slug"]).lstrip("/")}" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    home = pre + ("" if lang == "cs" else lang + "/")
    body = "".join(f"<p>{e(par)}</p>" for par in P["body"])
    others = "".join(f'<li><a href="{pre}{post_url(lang, o["slug"]).lstrip("/")}">{e(o[lang]["title"])}</a></li>' for o in POSTS if o["slug"] != po["slug"])[:2000]
    ld = {"@context":"https://schema.org","@type":"NewsArticle","headline":P["title"],"description":P["perex"],"datePublished":po["date"],"dateModified":po["date"],
          "inLanguage":{"cs":"cs-CZ","uk":"uk-UA","en":"en"}[lang],"image":[BASE+"/img/"+po["image"]+".jpg"],"mainEntityOfPage":url,
          "author":{"@type":"Organization","name":"Kupava","url":BASE+"/"},"publisher":{"@type":"Organization","name":"Ukrajinský folklorní soubor KUPAVA, z.s.","logo":{"@type":"ImageObject","url":BASE+"/img/logo.png"}}}
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(P["title"])} – {name}</title>
<meta name="description" content="{e(P["perex"])}">
<meta name="theme-color" content="#1c2f5a">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="article">
<meta property="og:title" content="{e(P["title"])}">
<meta property="og:description" content="{e(P["perex"])}">
<meta property="og:image" content="{BASE}/img/{po["image"]}.jpg">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Kupava">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/icon-192.png">
<link rel="apple-touch-icon" href="{pre}img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;700;800&display=swap&subset=cyrillic,latin-ext" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body class="article-page">
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <nav class="nav nav-simple"><a href="{pre}{LANGS[lang].lstrip("/")}aktuality/">{e(x["nav_news"])}</a><span class="lang">{langs}</span><a class="btn small primary" href="{home}#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>
<article class="post">
 <div class="wrap post-head">
  <p class="kicker">{e(x["news_k"])} · <time datetime="{po.get("event_date", po["date"])}">{e(fmt_post_date(po.get("event_date", po["date"]), lang))}</time></p>
  <h1>{e(P["title"])}</h1>
  <p class="lead">{e(P["perex"])}</p>
 </div>
 <figure class="wrap post-img"><img src="{pre}img/{po["image"]}.jpg" alt="{e(P["title"])}" width="2048" height="1365">{('<figcaption>' + e(po["credit"]) + '</figcaption>') if po.get("credit") else ''}</figure>
 <div class="wrap post-body">{body}
  <p class="post-cta"><a class="btn primary" href="{home}#kontakt">{e(t["nav_cta"])}</a> <a class="btn outline" href="{home}">{e(x["back"])}</a></p>
  <h2 class="others-h">{e(x["all_news"])}</h2><ul class="others">{others}</ul>
 </div>
</article>
<footer><div class="wrap foot">
 <div><b>Ukrajinský folklorní soubor KUPAVA, z.s.</b><br>{e(t["foot_seat"])}<br>{e(t["foot_reg"])}</div>
 <div class="lang">{langs}</div>
</div></footer>
</body>
</html>
'''

def archive(lang):
    t = T[lang]; x = X[lang]
    depth = 1 if lang == "cs" else 2
    pre = "../" * depth
    name = "Купава" if lang == "uk" else "Kupava"
    url = BASE + LANGS[lang] + "aktuality/"
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{LANGS[l]}aktuality/">' for l in LANGS)
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join(f'<a href="{pre}{LANGS[l].lstrip("/")}aktuality/" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    home = pre + ("" if lang == "cs" else lang + "/")
    cards = "".join(f'''<article class="news-card"><a href="{po['slug']}/"><img src="{pre}img/g/{po['image']}.jpg" alt="" loading="lazy" width="760" height="506"></a><div><time datetime="{po.get('event_date', po['date'])}">{e(fmt_post_date(po.get('event_date', po['date']), lang))}</time><h3><a href="{po['slug']}/">{e(po[lang]['title'])}</a></h3><p>{e(po[lang]['perex'])}</p><a class="link" href="{po['slug']}/">{e(x['more'])} →</a></div></article>''' for po in POSTS)
    title = f'{x["news_k"]} – {name}'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(x["arch_desc"])}">
<meta name="theme-color" content="#1c2f5a">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(x["arch_desc"])}"><meta property="og:image" content="{BASE}/img/soubor-portret.jpg"><meta property="og:url" content="{url}">
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;700;800&display=swap&subset=cyrillic,latin-ext" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body class="article-page">
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <nav class="nav nav-simple"><span class="lang">{langs}</span><a class="btn small primary" href="{home}#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>
<section class="post"><div class="wrap">
 <p class="kicker">{e(x["news_k"])}</p>
 <h1>{e(x["news_h"])}</h1>
 <div class="news news4 news-arch">{cards}</div>
 <p class="post-cta"><a class="btn outline" href="{home}">{e(x["back"])}</a></p>
</div></section>
<footer><div class="wrap foot">
 <div><b>Ukrajinský folklorní soubor KUPAVA, z.s.</b><br>{e(t["foot_seat"])}<br>{e(t["foot_reg"])}</div>
 <div class="lang">{langs}</div>
</div></footer>
</body>
</html>
'''

for lang in LANGS:
    ap = os.path.join(OUT, LANGS[lang].lstrip("/"), "aktuality", "index.html")
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap, "w").write(archive(lang))

for lang in LANGS:
    for po in POSTS:
        ap = os.path.join(OUT, post_url(lang, po["slug"]).lstrip("/"), "index.html")
        os.makedirs(os.path.dirname(ap), exist_ok=True)
        open(ap, "w").write(article(lang, po))

# press kit: bios txt + zip
import zipfile
os.makedirs(os.path.join(OUT, "press"), exist_ok=True)
bios = "\n\n".join(f"[{l.upper()}]\n{X[l]['bio']}" for l in LANGS)
open(os.path.join(OUT, "press", "kupava-medailonky.txt"), "w").write(bios + "\n\nKontakt: kupava@kupavabrno.cz · +420 777 072 433 · https://kupavabrno.cz\n")
with zipfile.ZipFile(os.path.join(OUT, "press", "kupava-press-kit.zip"), "w", zipfile.ZIP_STORED) as z:
    z.write(os.path.join(OUT, "press", "kupava-medailonky.txt"), "kupava-medailonky.txt")
    z.write(os.path.join(OUT, "img", "logo.png"), "kupava-logo.png")
    for f, c in PRESS_PHOTOS:
        z.write(os.path.join(OUT, "img", f + ".jpg"), "foto/kupava-" + f + ".jpg")

for lang in LANGS:
    path = os.path.join(OUT, "" if lang == "cs" else lang, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(page(lang))
LASTMOD = datetime.date.today().isoformat()
open(os.path.join(OUT, "404.html"), "w").write(f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stránka nenalezena – Kupava</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/style.css?v={VER}"></head><body><section class="hero" style="padding:120px 0 140px"><div class="wrap hero-text"><h1><span class="eyebrow">404</span><span class="h1-name">Kupava</span></h1><p class="lead">Stránka nenalezena · Сторінку не знайдено · Page not found</p><div class="btns"><a class="btn light" href="/">Čeština</a><a class="btn outline-light" href="/uk/">Українська</a><a class="btn outline-light" href="/en/">English</a></div></div></section></body></html>''')
open(os.path.join(OUT, "sitemap.xml"), "w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
 "".join(f'<url><loc>{BASE}{p}</loc><lastmod>{LASTMOD}</lastmod>' + "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{BASE}{p2}"/>' for l2, p2 in LANGS.items()) + '</url>\n' for p in LANGS.values()) + "".join(f'<url><loc>{BASE}{post_url(l, po["slug"])}</loc><lastmod>{po["date"]}</lastmod>' + "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{BASE}{post_url(l2, po["slug"])}"/>' for l2 in LANGS) + '</url>\n' for po in POSTS for l in LANGS) + "".join(f'<url><loc>{BASE}{LANGS[l]}aktuality/</loc><lastmod>{LASTMOD}</lastmod></url>\n' for l in LANGS) + '</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(OUT, "CNAME"), "w").write("kupavabrno.cz\n")
print(f"ok – {N_PAST} minulých vystoupení, {len(HIGHLIGHTS)} významných, {len(UPCOMING)} připravovaných")
