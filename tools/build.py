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
            press_p="Фотографії у високій роздільній здатності, логотип і коротка довідка про ансамбль для фестивальних програм, афіш і прес-релізів. Використовуючи фото, просимо зазначати джерело «Ансамбль Купава».",
            bio_h="Коротка довідка", copy="Копіювати текст", copied="Скопійовано",
            dl_zip="Повний пакет (ZIP)", dl_logo="Логотип (PNG)", dl_bio="Довідки CZ / UA / EN (TXT)", dl_photos="Фотографії",
            bio="«Купава» – український фольклорний ансамбль з Брно, заснований у лютому 2023 року. Ансамбль займається традиційним українським багатоголосим співом і народною музикою з різних регіонів України – співає українською, у народних строях, під живу музику. Виступав, зокрема, на Міжнародному фольклорному фестивалі у Стражніце, фестивалі Smetanova Litomyšl, Ходському святі та в прямому ефірі «Концерту для життя II» на TV Noe. Художня керівниця: Mgr. Катерина Михайлова.",
            foot_press="Для медіа", other_perf="Інші виступи"),
 "en": dict(nav_news="News", news_k="News", news_h="What’s new", more="Read more", back="← Back to the home page", all_news="More news", all_btn="All news", arch_desc="News from Kupava, the Ukrainian folk ensemble from Brno – performances, festivals and concerts.",
            press_k="For media and organisers", press_h="Press kit",
            press_p="High-resolution photographs, logo and a short biography of the ensemble for festival programmes, posters and press releases. When using the photographs, please credit “Kupava ensemble”.",
            bio_h="Short biography", copy="Copy text", copied="Copied",
            dl_zip="Complete press kit (ZIP)", dl_logo="Logo (PNG)", dl_bio="Biographies CZ / UA / EN (TXT)", dl_photos="Photographs",
            bio="Kupava is a Ukrainian folk ensemble from Brno, Czech Republic, founded in February 2023. It is dedicated to traditional Ukrainian polyphonic singing and folk music from many regions of Ukraine, performed in Ukrainian, in traditional costume and with live music. The ensemble has performed at the Strážnice International Folklore Festival, Smetana’s Litomyšl, the Chod Festival and in the live TV Noe broadcast of Concert for Life II. Artistic director: Kateryna Mykhaylova.",
            foot_press="Press kit", other_perf="Other performances"),
}
PRESS_PHOTOS = [("soubor-portret","Kupava – skupinový portrét / group portrait"),("vanoce-viden-2023","Staroukrajinské Vánoce / Old Ukrainian Christmas"),
                ("program-regiony","Kupava na pódiu / on stage"),("koncert-kostel","Koncert v kostele / Church concert"),("festival-podium","Festivalové vystoupení / Festival performance")]
N_PAST = len(PAST)

def uk_pl(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11: return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return few
    return many

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
 ("Ой чи є, чи нема пан господар дома?", "Je, či není pan hospodář doma?", "Is the Master at Home?"),
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
 ("soubor-v-krojich", {"cs":"Soubor Kupava v krojích","uk":"«Купава» у народних строях","en":"Kupava in traditional costume"}),
 ("festival-podium", {"cs":"Den národnostních menšin Jihomoravského kraje","uk":"День національних меншин Південноморавського краю","en":"South Moravian National Minorities Day"}),
 ("koledy-podium-kostel", {"cs":"Staroukrajinské Vánoce","uk":"Староукраїнське Різдво","en":"Old Ukrainian Christmas"}),
 ("housle-podium", {"cs":"Živá hudba na pódiu","uk":"Жива музика на сцені","en":"Live music on stage"}),
 ("viden-hvezda-2025", {"cs":"Koleda ve Vídni 2025","uk":"Коляда у Відні 2025","en":"Carols in Vienna 2025"}),
 ("zpev-radost", {"cs":"Vícehlasý zpěv","uk":"Багатоголосий спів","en":"Polyphonic singing"}),
 ("koncert-kostel", {"cs":"Koncert v kostele","uk":"Концерт у храмі","en":"Concert in a church"}),
 ("podium-celek", {"cs":"Kupava na festivalovém pódiu","uk":"«Купава» на фестивальній сцені","en":"Kupava on a festival stage"}),
 ("palac-hvezda-2024", {"cs":"Vánoční koncert v Paláci šlechtičen","uk":"Різдвяний концерт у Палаці шляхетних панн","en":"Christmas concert at the Palace of Noblewomen"}),
 ("akordeon-trava", {"cs":"Živá hudba a zpěv","uk":"Жива музика і спів","en":"Live music and singing"}),
 ("zpevacky-podium", {"cs":"Zpěvačky v krojích","uk":"Співачки у строях","en":"Singers in traditional costume"}),
 ("usmev-kroj", {"cs":"Ukrajinský kroj","uk":"Український народний стрій","en":"Ukrainian traditional costume"}),
]

T = {
"cs": dict(
  title="Kupava – folklorní soubor a pěvecký sbor z Brna | lidové písně a koledy",
  h1_pre="Ukrajinský folklorní soubor",
  desc="Folklorní soubor a pěvecký sbor Kupava z Brna – ukrajinské lidové písně a koledy ve vícehlasém zpěvu, lidová hudba a kroje. Adventní a vánoční koncerty, festivaly.",
  brand_sub="ukrajinský folklorní soubor",
  nav=[("#o-nas","O nás"),("#repertoar","Repertoár"),("#vystoupeni","Vystoupení"),("#video","Video"),("#galerie","Galerie")],
  nav_cta="Kontakt",
  eyebrow="Ukrajinský folklorní soubor · Brno",
  lead="Tradiční vícehlasý zpěv a živá lidová hudba z různých regionů Ukrajiny.",
  cta1="Poslechnout si nás", cta2="Napište nám",
  photo_alt="Folklorní soubor a pěvecký sbor Kupava v lidových krojích",
  stats=[("2023","založení souboru"),(str(N_PAST),"vystoupení"),("10+","folklorních festivalů"),("3","země – Česko, Slovensko, Rakousko")],
  stages_k="Vystupovali jsme mimo jiné",
  stages=["MFF Strážnice","Smetanova Litomyšl","Chodské slavnosti","Jánošíkův dukát","TV Noe"],
  about_k="O nás", about_h="Píseň, která spojuje",
  about_p=[
   "Ukrajinský folklorní soubor <b>Kupava</b> vznikl v únoru 2023 za podpory Ukrajinského centra v Brně. Jsme folklorní soubor i pěvecký sbor: věnujeme se tradičnímu ukrajinskému vícehlasému zpěvu a lidové hudbě z různých regionů Ukrajiny – zpíváme v originále, v krojích a za doprovodu živé hudby.",
   "Soubor tvoří Ukrajinky dlouhodobě žijící v Česku, ženy, které musely odejít z Ukrajiny po plnohodnotné ruské invazi v roce 2022, i Češi, kteří mají ukrajinský folklór rádi.",
   "Vystupujeme na folklorních festivalech, adventních a vánočních koncertech, v kostelích i na kulturních akcích měst a obcí."],
  director="Umělecká vedoucí", director_name="Mgr. Kateryna Mykhaylova",
  name_note="Kupava je staré slovanské jméno – „krásná, slavnostně oblečená“ nebo „žena s ladnou a hrdou chůzí“.",
  pillars_h="Naše poslání",
  pillars=[("Uchováváme","Studujeme a uchováváme ukrajinské lidové písně, hudbu a tradiční kroje."),
           ("Představujeme","Přinášíme ukrajinský folklór na pódia festivalů, do koncertních sálů i kostelů."),
           ("Spojujeme","Podporujeme setkávání a porozumění mezi ukrajinskou a českou kulturou.")],
  tv_k="Koncert pro život II", tv_h="Živě na TV Noe",
  tv_p="V dubnu 2025 jsme vystoupili v kostele sv. Václava v Ostravě na benefičním Koncertu pro život II, který živě vysílala TV Noe. Spolu s písničkářem Pavlem Helanem, česko-ukrajinským sborem Sonjašnyk a dětským sborem Spivanočky jsme podpořili rehabilitaci válečných veteránů a zraněných dětí z Ukrajiny – diváci přispěli 200 000 Kč.",
  tv_meta="6. dubna 2025 · Ostrava · TV Noe",
  rep_k="Repertoár", rep_h="Koncertní programy",
  progs=[("vanoce-viden-2023","Staroukrajinské Vánoce","Koledy a ščedrivky s vánoční hvězdou. Sváteční program, který každoročně uvádíme v Brně a ve Vídni."),
         ("program-regiony","Písně ukrajinských regionů","Lyrické, obřadní a taneční písně v tradičním vícehlasu s živou hudbou – pro festivaly, koncertní sály a kulturní události.")],
  rep_list="Z repertoáru", rep_note="Písně zpíváme v ukrajinštině; uvádíme český překlad názvů.",
  perf_k="Vystoupení", perf_h="Významná vystoupení", up_k="Připravujeme",
  perf_note=f"Celkem {N_PAST} vystoupení od roku 2023 – folklorní festivaly, adventní a vánoční koncerty, koncerty v kostelích i kulturní akce v Česku, na Slovensku a v Rakousku.",
  quote="„Zaplněný kostel v Brně si užil atmosféru staroukrajinských Vánoc.“", quote_src="ČTK / České noviny, 5. 1. 2025",
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
  title="Купава – фольклорний ансамбль і хор з Брно | народні пісні й колядки",
  h1_pre="Український фольклорний ансамбль",
  desc="Фольклорний ансамбль і хор «Купава» з Брно (Чехія) – українські народні пісні й колядки в багатоголоссі, жива народна музика та строї. Різдвяні концерти й фестивалі.",
  brand_sub="український фольклорний ансамбль",
  nav=[("#o-nas","Про нас"),("#repertoar","Репертуар"),("#vystoupeni","Виступи"),("#video","Відео"),("#galerie","Галерея")],
  nav_cta="Контакти",
  eyebrow="Український фольклорний ансамбль · Брно",
  lead="Традиційний багатоголосий спів і жива народна музика з різних регіонів України.",
  cta1="Послухати нас", cta2="Напишіть нам",
  photo_alt="Український фольклорний ансамбль «Купава» у народних строях",
  stats=[("2023","рік заснування"),(str(N_PAST),uk_pl(N_PAST,"виступ","виступи","виступів")),("10+","фольклорних фестивалів"),("3","країни – Чехія, Словаччина, Австрія")],
  stages_k="Ми виступали, зокрема",
  stages=["Фестиваль у Стражніце","Smetanova Litomyšl","Ходське свято","Яношиків дукат","TV Noe"],
  about_k="Про нас", about_h="Пісня, що єднає",
  about_p=[
   "Український фольклорний ансамбль <b>«Купава»</b> заснований у лютому 2023 року за підтримки Українського центру в Брно. Ми – фольклорний ансамбль і водночас хор: займаємося традиційним українським багатоголосим співом і народною музикою з різних регіонів України – співаємо українською, у строях, під живу музику.",
   "В ансамблі співають українки, які давно живуть у Чехії, жінки, що були змушені покинути Україну після повномасштабного російського вторгнення 2022 року, а також чехи, які люблять український фольклор.",
   "Ми виступаємо на фольклорних фестивалях, адвентних і різдвяних концертах, у храмах і на культурних подіях міст і громад."],
  director="Художня керівниця", director_name="Mgr. Катерина Михайлова",
  name_note="Купава – давнє слов’янське ім’я: «гарна, святково вбрана» або «жінка з граціозною і гордою ходою».",
  pillars_h="Наша місія",
  pillars=[("Зберігаємо","Вивчаємо й зберігаємо українські народні пісні, музику та традиційні строї."),
           ("Представляємо","Несемо український фольклор на сцени фестивалів, у концертні зали й храми."),
           ("Єднаємо","Підтримуємо зустрічі та порозуміння між українською і чеською культурами.")],
  tv_k="Концерт для життя II", tv_h="Наживо на TV Noe",
  tv_p="У квітні 2025 року ми виступили в храмі св. Вацлава в Остраві на благодійному «Концерті для життя II», який наживо транслювало TV Noe. Разом зі співаком Павлом Геланом, чесько-українським хором «Соняшник» і дитячим хором «Співаночки» ми підтримали реабілітацію ветеранів війни та поранених дітей з України – глядачі пожертвували 200 000 крон.",
  tv_meta="6 квітня 2025 · Острава · TV Noe",
  rep_k="Репертуар", rep_h="Концертні програми",
  progs=[("vanoce-viden-2023","Староукраїнське Різдво","Колядки й щедрівки з різдвяною зіркою. Святкова програма, яку ми щороку представляємо в Брно та Відні."),
         ("program-regiony","Пісні українських регіонів","Ліричні, обрядові й танцювальні пісні в традиційному багатоголоссі з живою музикою – для фестивалів, концертних залів і культурних подій.")],
  rep_list="З репертуару", rep_note="Ми співаємо українською мовою.",
  perf_k="Виступи", perf_h="Визначні виступи", up_k="Найближчі виступи",
  perf_note=f"Загалом {N_PAST} {uk_pl(N_PAST,'виступ','виступи','виступів')} з 2023 року – фольклорні фестивалі, адвентні й різдвяні концерти, концерти в храмах і культурні події в Чехії, Словаччині та Австрії.",
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
  foot_seat="Юридична адреса: Městečko 68, 664 61 Rajhrad", foot_reg="IČO 23686766 · громадське об’єднання, зареєстроване Крайовим судом у Брно, L 31074",
),
"en": dict(
  title="Kupava – Folk Ensemble & Choir from Brno | Folk Songs and Carols",
  h1_pre="Ukrainian folk ensemble",
  desc="Kupava is a folk ensemble and choir from Brno, Czech Republic – Ukrainian folk songs and Christmas carols in polyphony, live folk music and traditional costume. Christmas concerts and festivals.",
  brand_sub="Ukrainian folk ensemble",
  nav=[("#o-nas","About"),("#repertoar","Repertoire"),("#vystoupeni","Performances"),("#video","Video"),("#galerie","Gallery")],
  nav_cta="Contact",
  eyebrow="Ukrainian folk ensemble · Brno, Czech Republic",
  lead="Traditional Ukrainian polyphonic singing and live folk music from many regions of Ukraine.",
  cta1="Listen to us", cta2="Get in touch",
  photo_alt="Kupava folk ensemble and choir in traditional costume",
  stats=[("2023","founded"),(str(N_PAST),"performances"),("10+","folklore festivals"),("3","countries – Czech Republic, Slovakia, Austria")],
  stages_k="We have performed at",
  stages=["Strážnice International Folklore Festival","Smetana’s Litomyšl","Chod Festival","Jánošík’s Ducat","TV Noe"],
  about_k="About us", about_h="Songs that connect",
  about_p=[
   "The Ukrainian folk ensemble <b>Kupava</b> was founded in February 2023 in Brno, Czech Republic, with the support of the Ukrainian Centre in Brno. We are both a folk ensemble and a choir, dedicated to traditional Ukrainian polyphonic singing and folk music from many regions of Ukraine – sung in Ukrainian, in traditional costume and with live music.",
   "The ensemble brings together Ukrainian women long settled in the Czech Republic, women who had to leave Ukraine after Russia’s full-scale invasion in 2022, and Czechs who love Ukrainian folklore.",
   "We perform at folklore festivals, Advent and Christmas concerts, in churches and at cultural events of towns and villages."],
  director="Artistic director", director_name="Kateryna Mykhaylova",
  name_note="Kupava is an old Slavic name meaning “beautiful, festively dressed” or “a woman with a graceful, proud walk”.",
  pillars_h="Our mission",
  pillars=[("We preserve","We study and preserve Ukrainian folk songs, music and traditional costume."),
           ("We present","We bring Ukrainian folklore to festival stages, concert halls and churches."),
           ("We connect","We foster encounters and understanding between Ukrainian and Czech culture.")],
  tv_k="Concert for Life II", tv_h="Live on TV Noe",
  tv_p="In April 2025 we performed at St Wenceslas Church in Ostrava in the charity Concert for Life II, broadcast live by TV Noe. Together with singer-songwriter Pavel Helan, the Czech-Ukrainian choir Sonjašnyk and the Spivanočky children’s choir, we supported the rehabilitation of war veterans and injured children from Ukraine – viewers donated CZK 200,000.",
  tv_meta="6 April 2025 · Ostrava · TV Noe",
  rep_k="Repertoire", rep_h="Concert programmes",
  progs=[("vanoce-viden-2023","Old Ukrainian Christmas","Carols and shchedrivky with the Christmas star – a festive programme we present every year in Brno and Vienna."),
         ("program-regiony","Songs of Ukraine’s Regions","Lyrical, ritual and dance songs in traditional polyphony with live music – for festivals, concert halls and cultural events.")],
  rep_list="From our repertoire", rep_note="We sing in Ukrainian; English translations of the titles are given.",
  perf_k="Performances", perf_h="Selected performances", up_k="Upcoming",
  perf_note=f"{N_PAST} performances since 2023 in total – folklore festivals, Advent and Christmas concerts, church concerts and cultural events in the Czech Republic, Slovakia and Austria.",
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
  foot_seat="Registered office: Městečko 68, 664 61 Rajhrad, Czech Republic", foot_reg="Reg. no. 23686766 · association registered with the Regional Court in Brno, L 31074",
)}

GTAG_HEAD = """<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
(function(){var g=false;try{g=localStorage.getItem('kupava_consent_v1')==='granted'}catch(e){}var v=g?'granted':'denied';
gtag('consent','default',{ad_storage:v,ad_user_data:v,ad_personalization:'denied',analytics_storage:v,wait_for_update:500});})();
gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',true);
gtag('js',new Date());gtag('config','G-X6NC9E6Y45');gtag('config','AW-18567655723');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X6NC9E6Y45"></script>"""
ORN = '<svg class="orn" viewBox="0 0 240 44" aria-hidden="true"><g fill="currentColor"><path d="M8 21.3h72v1.4H8zM160 21.3h72v1.4h-72z"/><circle cx="90" cy="22" r="2.2"/><circle cx="150" cy="22" r="2.2"/><path d="M111.51 1.85L117.21 7.62L117.21 17.85L111.51 12.08ZM99.85 13.51L105.62 19.21L115.85 19.21L110.08 13.51ZM111.51 42.15L117.21 36.38L117.21 26.15L111.51 31.92ZM140.15 13.51L134.38 19.21L124.15 19.21L129.92 13.51ZM128.49 1.85L122.79 7.62L122.79 17.85L128.49 12.08ZM99.85 30.49L105.62 24.79L115.85 24.79L110.08 30.49ZM128.49 42.15L122.79 36.38L122.79 26.15L128.49 31.92ZM140.15 30.49L134.38 24.79L124.15 24.79L129.92 30.49Z"/><circle cx="120" cy="22" r="2.9"/></g></svg>'


# Písma jsou uložená přímo na webu (assets/fonts) – žádné načítání z Google Fonts.
def fonts_head(pre, lang):
    sub = "cyrillic" if lang == "uk" else "latin"
    return (f'<link rel="preload" href="{pre}assets/fonts/manrope-normal-{sub}.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="preload" href="{pre}assets/fonts/cormorant-garamond-normal-{sub}.woff2" as="font" type="font/woff2" crossorigin>')
FONTS_HEAD = ""  # (nahrazeno funkcí fonts_head)

SKIP = {"cs": "Přeskočit na obsah", "uk": "Перейти до змісту", "en": "Skip to content"}

# Obrázky: <picture> s WebP a správnými rozměry (rozměry se čtou ze souboru)
try:
    from PIL import Image as _PILImage
except Exception:
    _PILImage = None
_DIM = {}
def _dims(rel):
    if rel not in _DIM:
        w = h = None
        try:
            with _PILImage.open(os.path.join(OUT, rel)) as im: w, h = im.size
        except Exception: pass
        _DIM[rel] = (w, h)
    return _DIM[rel]
def pic(pre, rel_noext, alt, attrs='loading="lazy"'):
    w, h = _dims(rel_noext + ".jpg")
    wh = f' width="{w}" height="{h}"' if w else ""
    webp = os.path.exists(os.path.join(OUT, rel_noext + ".webp"))
    src = f'<source srcset="{pre}{rel_noext}.webp" type="image/webp">' if webp else ""
    return f'<picture>{src}<img src="{pre}{rel_noext}.jpg" alt="{e(alt)}"{wh} {attrs}></picture>'

def footer(lang, pre, langs):
    t = T[lang]
    return (f'<footer><div class="wrap foot">\n <div><b>Ukrajinský folklorní soubor KUPAVA, z.s.</b><br>{e(t["foot_seat"])}<br>{e(t["foot_reg"])}'
            f'<br><a class="cookie-link" href="{priv_href(lang, pre)}">{e(PRIV_LBL[lang])}</a></div>\n <div class="lang">{langs}</div>\n</div></footer>')


# Časté otázky – odpovědi na to, co lidé hledají (ukrajinské Vánoce, koledy, kroj, písně, sbor). Slouží i pro AI vyhledávače (FAQPage).
FAQ_HEAD = {"cs": ("Časté otázky", "Ukrajinský folklór a Kupava"), "uk": ("Часті запитання", "Український фольклор і «Купава»"), "en": ("FAQ", "Ukrainian folklore and Kupava")}
def faq_items(lang):
    nxt = UPCOMING[0] if UPCOMING else None
    if lang == "cs":
        up = f" Nejbližší vystoupení: {nxt['cs']}, {fdate(nxt, 'cs')} ({nxt['place']['cs']})." if nxt else ""
        return [
         ("Co je Kupava?", "Kupava je ukrajinský folklorní soubor a pěvecký sbor z Brna, založený v únoru 2023. Zpívá ukrajinské lidové písně a koledy v tradičním vícehlasu, v krojích a za doprovodu živé hudby. Umělecká vedoucí je Mgr. Kateryna Mykhaylova."),
         ("Je v Brně ukrajinský sbor?", "Ano. Kupava je ukrajinský folklorní soubor a sbor, který působí v Brně a vystupuje v Česku, na Slovensku a v Rakousku. Soubor tvoří Ukrajinky žijící v Česku i Češi, kteří mají rádi ukrajinský folklór."),
         ("Jaké ukrajinské písně Kupava zpívá?", "Lyrické, obřadní a taneční lidové písně z různých regionů Ukrajiny a vánoční koledy a ščedrivky – vždy v ukrajinštině a v tradičním vícehlasém podání. Například „Зеленеє жито, зелене“, „Ой, устану ранесенько“ nebo „Добрий вечір тобі, пане господарю“."),
         ('Je Kupava folklorní soubor, nebo pěvecký sbor?', 'Obojí. Jako pěvecký sbor zpívá Kupava ve vícehlasu – sborový zpěv je základem každého vystoupení. Jako folklorní soubor uvádí lidové písně v krojích a za doprovodu živé lidové hudby: housle, akordeon, kontrabas, bandura a cimbál.'),
         ('Co je vícehlasý zpěv?', 'Vícehlasý zpěv znamená, že píseň zní v několika hlasech zároveň. V ukrajinské lidové tradici melodii často nesou spodní hlasy a nad nimi zní vysoký horní hlas – pidholosok. Takto zpívá Kupava lidové písně i koledy.'),
         ('Vystupuje Kupava na adventních a vánočních koncertech?', 'Ano. V adventu a o Vánocích uvádí program Staroukrajinské Vánoce s koledami a ščedrivkami – v posledních letech v kostele sv. Josefa v Brně, u Jošta na Moravském náměstí a ve Vídni.'),
         ("Kde můžu Kupavu slyšet živě?", "Na folklorních festivalech (např. MFF Strážnice, Chodské slavnosti), na festivalu Smetanova Litomyšl, na koncertech a vánočních programech v Brně i ve Vídni." + up + " Ukázky najdete na YouTube."),
         ("Jak se slaví ukrajinské Vánoce?", "Od roku 2023 jsou Vánoce na Ukrajině oficiálně 25. prosince. Na Štědrý večer se schází rodina u dvanácti postních jídel, koledníci chodí s osmicípou vánoční hvězdou a zpívají koledy. Na Ščedryj večir, předvečer Nového roku, se zpívají ščedrivky. Kupava každoročně uvádí program Staroukrajinské Vánoce."),
         ("Co jsou koledy a ščedrivky?", "Koledy (koljadky) jsou vánoční písně, které se zpívají od Štědrého večera. Ščedrivky jsou novoroční písně s přáním hojnosti a štěstí hospodáři a jeho rodině. Nejznámější ščedrivkou je Ščedryk v úpravě Mykoly Leontovyče, ve světě známý jako Carol of the Bells."),
         ("Jak vypadá ukrajinský kroj?", "Základem je vyšívaná košile – vyšyvanka – s ornamenty typickými pro daný region. Ženy k ní nosí sukni nebo zavinutou plachtu, vestu, korálové náhrdelníky a na hlavě věnec z květů se stuhami (vinok) nebo šátek. Členky a členové Kupavy vystupují v krojích z různých regionů Ukrajiny."),
         ("Jak se se souborem spojit?", "Pro informace o vystoupení nebo společném projektu napište na kupava@kupavabrno.cz, zavolejte na +420 777 072 433 nebo použijte kontaktní formulář na tomto webu."),
        ]
    if lang == "uk":
        up = f" Найближчий виступ: {nxt['uk']}, {fdate(nxt, 'uk')} ({nxt['place']['uk']})." if nxt else ""
        return [
         ("Що таке «Купава»?", "«Купава» – український фольклорний ансамбль і хор з Брно (Чехія), заснований у лютому 2023 року. Ансамбль виконує українські народні пісні та колядки в традиційному багатоголоссі, у народних строях і під живу музику. Художня керівниця – Mgr. Катерина Михайлова."),
         ("Чи є в Брно український хор?", "Так. «Купава» – український фольклорний ансамбль і хор, що діє в Брно та виступає в Чехії, Словаччині та Австрії. В ансамблі співають українки, які живуть у Чехії, а також чехи, які люблять український фольклор."),
         ("Які українські пісні співає «Купава»?", "Ліричні, обрядові й танцювальні народні пісні з різних регіонів України, а також колядки й щедрівки – українською мовою, у традиційному багатоголоссі. Наприклад, «Зеленеє жито, зелене», «Ой, устану ранесенько», «Добрий вечір тобі, пане господарю»."),
         ('«Купава» – це фольклорний ансамбль чи хор?', 'І те, і те. Як хор «Купава» співає багатоголосо – хоровий спів є основою кожного виступу. Як фольклорний ансамбль виконує народні пісні в строях і під живу народну музику: скрипка, акордеон, контрабас, бандура й цимбали.'),
         ('Що таке багатоголосий спів?', 'Багатоголосий спів означає, що пісня звучить кількома голосами одночасно. В українській народній традиції мелодію часто ведуть нижні голоси, а над ними звучить високий верхній голос – підголосок. Саме так «Купава» співає народні пісні й колядки.'),
         ('Чи виступає «Купава» на адвентних і різдвяних концертах?', 'Так. Під час адвенту й на Різдво ансамбль представляє програму «Староукраїнське Різдво» з колядками й щедрівками – останніми роками в храмі св. Йосифа в Брно, біля Йошта на Моравській площі та у Відні.'),
         ("Де можна почути «Купаву» наживо?", "На фольклорних фестивалях (зокрема в Стражніце та на Ходському святі), на фестивалі Smetanova Litomyšl, на концертах і різдвяних програмах у Брно та Відні." + up + " Записи є на YouTube."),
         ("Як святкують українське Різдво?", "З 2023 року Різдво в Україні офіційно святкують 25 грудня. На Святвечір родина збирається за дванадцятьма пісними стравами, колядники ходять з восьмипроменевою різдвяною зіркою й колядують. На Щедрий вечір, напередодні Нового року, співають щедрівки. «Купава» щороку представляє програму «Староукраїнське Різдво»."),
         ("Що таке колядки й щедрівки?", "Колядки – різдвяні пісні, які співають від Святвечора. Щедрівки – новорічні пісні з побажанням щедрості, добра й щастя господарям. Найвідоміша у світі щедрівка – «Щедрик» Миколи Леонтовича, відома як Carol of the Bells."),
         ("Який вигляд має український народний стрій?", "Основа – вишита сорочка, вишиванка, з орнаментами, характерними для певного регіону. Жінки вдягають до неї спідницю або плахту, керсетку, коралове намисто, а на голову – вінок із квітами та стрічками або хустку. Учасниці й учасники «Купави» виступають у строях різних регіонів України."),
         ("Як зв’язатися з ансамблем?", "Щодо виступу чи спільного проєкту пишіть на kupava@kupavabrno.cz, телефонуйте +420 777 072 433 або скористайтеся контактною формою на сайті."),
        ]
    up = f" Next performance: {nxt['en']}, {fdate(nxt, 'en')} ({nxt['place']['en']})." if nxt else ""
    return [
     ("What is Kupava?", "Kupava is a Ukrainian folk ensemble and choir from Brno, Czech Republic, founded in February 2023. It performs Ukrainian folk songs and Christmas carols in traditional polyphony, in traditional costume and with live music. Artistic director: Kateryna Mykhaylova."),
     ("Is there a Ukrainian choir in Brno?", "Yes. Kupava is a Ukrainian folk ensemble and choir based in Brno that performs in the Czech Republic, Slovakia and Austria. It brings together Ukrainian women living in the Czech Republic and Czechs who love Ukrainian folklore."),
     ("What Ukrainian songs does Kupava sing?", "Lyrical, ritual and dance folk songs from many regions of Ukraine, as well as Christmas carols (koliadky) and New Year songs (shchedrivky) – always in Ukrainian and in traditional polyphony, e.g. “Zeleneie zhyto, zelene” or “Dobryi vechir tobi, pane hospodariu”."),
     ('Is Kupava a folk ensemble or a choir?', 'Both. As a choir, Kupava sings in polyphony – choral singing is the heart of every performance. As a folk ensemble, it presents folk songs in traditional costume with live folk music: violin, accordion, double bass, bandura and cimbalom.'),
     ('What is polyphonic singing?', 'Polyphonic singing means a song is sung in several voices at once. In Ukrainian folk tradition the lower voices often carry the melody while a high upper voice – the pidholosok – soars above them. This is how Kupava sings folk songs and carols.'),
     ('Does Kupava perform at Advent and Christmas concerts?', 'Yes. During Advent and at Christmas the ensemble presents its programme Old Ukrainian Christmas with carols and shchedrivky – in recent years at St Joseph’s Church in Brno, by the Jošt statue on Moravské náměstí and in Vienna.'),
     ("Where can I hear Kupava live?", "At folklore festivals (e.g. the Strážnice International Folklore Festival and the Chod Festival), at Smetana’s Litomyšl, and at concerts and Christmas programmes in Brno and Vienna." + up + " Recordings are on YouTube."),
     ("How is Ukrainian Christmas celebrated?", "Since 2023 Christmas in Ukraine has officially been celebrated on 25 December. On Christmas Eve families gather for a meal of twelve meatless dishes, and carol singers go from house to house with an eight-pointed star. On Shchedryi Vechir, New Year’s Eve, people sing shchedrivky. Every year Kupava presents its programme Old Ukrainian Christmas."),
     ("What are koliadky and shchedrivky?", "Koliadky are Christmas carols sung from Christmas Eve onwards. Shchedrivky are New Year songs wishing abundance and happiness to the household. The world’s best-known shchedrivka is Shchedryk by Mykola Leontovych – known in English as Carol of the Bells."),
     ("What does Ukrainian traditional costume look like?", "Its heart is the embroidered shirt, the vyshyvanka, with ornaments typical of each region. Women wear it with a skirt or wrap-around plakhta, a vest, coral necklaces and a flower wreath with ribbons (vinok) or a headscarf. Kupava’s members perform in traditional costume from different regions of Ukraine."),
     ("How can I contact the ensemble?", "For performances or joint projects, write to kupava@kupavabrno.cz, call +420 777 072 433 or use the contact form on this website."),
    ]

def faq_section(lang):
    k, h = FAQ_HEAD[lang]
    items = "".join(f'<details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_items(lang))
    return f'<section id="otazky"><div class="wrap faq"><div class="faq-head"><p class="kicker">{e(k)}</p><h2>{e(h)}</h2></div><div class="faq-list">{items}</div></div></section>'

def page(lang):
    t = T[lang]; pre = "" if lang == "cs" else "../"
    home = pre + ("" if lang == "cs" else lang + "/") or "./"
    name = "Купава" if lang == "uk" else "Kupava"
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in LANGS.items())
    SAME = ["https://www.facebook.com/KupavaBrno","https://www.instagram.com/soubor_kupava/","https://www.youtube.com/playlist?list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5"]
    INLANG = {"cs":"cs-CZ","uk":"uk-UA","en":"en"}[lang]
    group = {"@type":["MusicGroup","PerformingGroup"],"@id":BASE+"/#kupava","name":"Kupava","alternateName":["Купава","Kupava Brno","Ukrajinský folklorní soubor Kupava","Ukrajinský sbor Kupava","Ансамбль «Купава»","Український хор «Купава»","Kupava Ukrainian Choir"],
          "legalName":"Ukrajinský folklorní soubor KUPAVA, z.s.","description":t["desc"],"url":BASE+"/","logo":BASE+"/img/logo.png","image":BASE+"/img/soubor-portret.jpg",
          "genre":["Folk music","Ukrainian folk music","Choral music","Polyphonic singing","Christmas carols","World music"],"knowsAbout":["Folk songs","Folklore","Choral singing","Polyphonic singing","Christmas carols","Traditional costume","Ukrainian Christmas traditions"],"foundingDate":"2023-02","foundingLocation":{"@type":"Place","name":"Brno"},
          "identifier":{"@type":"PropertyValue","propertyID":"IČO","value":"23686766"},"nonprofitStatus":"Nonprofit",
          "email":"kupava@kupavabrno.cz","telephone":"+420777072433",
          "address":{"@type":"PostalAddress","streetAddress":"Městečko 68","postalCode":"66461","addressLocality":"Rajhrad","addressCountry":"CZ"},
          "areaServed":["CZ","SK","AT","Europe"],"sameAs":SAME}
    EVDESC = {"cs":"Vystoupení ukrajinského folklorního souboru Kupava – tradiční vícehlasý zpěv a živá lidová hudba.","uk":"Виступ українського фольклорного ансамблю «Купава» – традиційний багатоголосий спів і жива народна музика.","en":"A performance by Kupava, the Ukrainian folk ensemble – traditional polyphonic singing and live folk music."}
    def evdesc(ev):
        po = next((p for p in POSTS if p.get("event_date") == ev["date"]), None)
        return po[lang]["perex"] if po else EVDESC[lang]
    events = [{"@type":"MusicEvent","name":ev[lang],"description":evdesc(ev),"startDate":ev["date"],"endDate":ev.get("end",ev["date"]),"eventStatus":"https://schema.org/EventScheduled",
               "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","location":{"@type":"Place","name":ev["place"][lang],"address":ev["place"][lang]},
               "performer":{"@id":BASE+"/#kupava"},"organizer":{"@id":BASE+"/#kupava"},"image":BASE+"/img/soubor-portret.jpg","url":BASE+LANGS[lang]+"#vystoupeni"} for ev in UPCOMING]
    ld = {"@context":"https://schema.org","@graph":[group,
          {"@type":"WebSite","@id":BASE+"/#web","url":BASE+"/","name":"Kupava","inLanguage":["cs-CZ","uk-UA","en"],"publisher":{"@id":BASE+"/#kupava"}},
          {"@type":"WebPage","url":BASE+LANGS[lang],"name":t["title"],"description":t["desc"],"inLanguage":INLANG,"isPartOf":{"@id":BASE+"/#web"},"about":{"@id":BASE+"/#kupava"},
           "primaryImageOfPage":BASE+"/img/soubor-portret.jpg"},
          {"@type":"FAQPage","inLanguage":INLANG,"mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faq_items(lang)]}] + events}
    x = X[lang]
    nav = "".join(f'<a href="{h}">{e(n)}</a>' for h, n in t["nav"][:3]) + f'<a href="#aktuality">{e(x["nav_news"])}</a>' + "".join(f'<a href="{h}">{e(n)}</a>' for h, n in t["nav"][3:])
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join('<a href="' + (pre + ("" if l=="cs" else l+"/") or "./") + f'" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    stats = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in t["stats"])
    stages = "".join(f'<li>{e(s)}</li>' for s in t["stages"])
    about = "".join(f"<p>{p}</p>" for p in t["about_p"])
    pillars = "".join(f'<div class="pillar"><span class="num">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(t["pillars"]))
    progs = "".join(f'<article class="prog"><div class="prog-img">{pic(pre, "img/g/" + img, h)}</div><div class="prog-body"><span class="prog-n">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></div></article>' for i, (img, h, p) in enumerate(t["progs"]))
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
    cards = "".join(f'<article class="feat"><div class="feat-img">{pic(pre, "img/g/" + FEATURED_IMG[n], evs[0][lang])}</div><div class="feat-body"><time>{e(when(evs))}</time><h3>{e(evs[0][lang])}</h3><p>{e(evs[0]["place"][lang])}</p></div></article>' for n, evs in feat)
    hl = "".join(f'<li><time>{e(when(evs))}</time><b>{e(evs[0][lang])}</b><span>{e(evs[0]["place"][lang])}</span></li>' for n, evs in rest)
    up = ""
    if UPCOMING:
        def up_item(ev):
            po = next((p for p in POSTS if p.get("event_date") == ev["date"]), None)
            img = f'<a class="up-img" href="aktuality/{po["slug"]}/">{pic(pre, "img/g/" + po["image"], ev[lang])}</a>' if po else ''
            more = f'<a class="link" href="aktuality/{po["slug"]}/">{e(X[lang]["more"])} →</a>' if po else ''
            return f'<li class="up-item">{img}<div class="up-text"><time>{e(fdate(ev, lang))}</time><b>{e(ev[lang])}</b><span>{e(ev["place"][lang])}</span>{more}</div></li>'
        up = f'<div class="upcoming"><p class="kicker">{e(t["up_k"])}</p><ul>' + "".join(up_item(ev) for ev in UPCOMING) + '</ul></div>'
    vids = "".join(f'<div class="vid"><button class="yt" data-id="{vid}" aria-label="{e(title)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"></button><p><b lang="uk">{e(title)}</b><span>{e(sub[lang])}</span></p></div>' for vid, title, sub in VIDEOS)
    gal = "".join(f'<a href="{pre}img/{s}.jpg">{pic(pre, "img/g/" + s, a[lang])}</a>' for s, a in GALLERY)
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
{fonts_head(pre, lang)}
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{GTAG_HEAD}
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#o-nas">{e(SKIP[lang])}</a>
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo-84.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
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
 <figure class="hero-photo wrap"><picture><source type="image/webp" srcset="{pre}img/soubor-portret-800.webp 800w, {pre}img/soubor-portret-1200.webp 1200w, {pre}img/soubor-portret-1600.webp 1600w, {pre}img/soubor-portret-2048.webp 2048w" sizes="(max-width:1300px) 100vw, 1240px"><img src="{pre}img/soubor-portret.jpg" srcset="{pre}img/soubor-portret-1200.jpg 1200w, {pre}img/soubor-portret.jpg 2048w" sizes="(max-width:1300px) 100vw, 1240px" alt="{e(t["photo_alt"])}" width="2048" height="1365" fetchpriority="high"></picture></figure>
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
 <div class="about-pic">{pic(pre, "img/g/zpev-podium", GALLERY[1][1][lang])}</div>
</div>
<div class="wrap mission"><h3 class="mission-h">{e(t["pillars_h"])}</h3><div class="pillars">{pillars}</div></div>
</section>

<section class="tv"><div class="wrap tv-grid">
 <div class="tv-pic">{pic(pre, "img/g/vinky", t["tv_h"])}</div>
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

<section id="video" class="soft"><div class="wrap">
 <div class="sec-head"><div><p class="kicker">{e(t["vid_k"])}</p><h2>{e(t["vid_h"])}</h2></div><a class="link" href="https://www.youtube.com/watch?v=qvbnvvhpYXQ&amp;list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5" target="_blank" rel="noopener">{e(t["vid_more"])} ↗</a></div>
 <div class="videos">{vids}</div>
</div></section>

<section id="galerie"><div class="wrap">
 <p class="kicker">{e(t["gal_k"])}</p>
 <h2>{e(t["gal_h"])}</h2>
 <div class="gallery">{gal}</div>
</div></section>

{press_section(lang, pre)}

{faq_section(lang)}

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

{footer(lang, pre, langs)}

<div class="lb" role="dialog" aria-modal="true" aria-label="{e(t["gal_h"])}"><button class="x" aria-label="×">×</button><button class="p" aria-label="‹">‹</button><img alt=""><button class="n" aria-label="›">›</button></div>
<script src="{pre}assets/site.js?v={VER}"></script>
</body>
</html>
'''

def fmt_post_date(d, lang):
    y, m, dd = map(int, d.split("-"))
    return f"{dd}. {MONTHS[lang][m-1]} {y}" if lang == "cs" else f"{dd} {MONTHS[lang][m-1]} {y}"

def news_section(lang, pre):
    x = X[lang]
    cards = "".join(f'''<article class="news-card"><a href="aktuality/{po['slug']}/">{pic(pre, "img/g/" + po['image'], po[lang]['title'])}</a><div><time datetime="{po.get('event_date', po['date'])}">{e(fmt_post_date(po.get('event_date', po['date']), lang))}</time><h3><a href="aktuality/{po['slug']}/">{e(po[lang]['title'])}</a></h3><p>{e(po[lang]['perex'])}</p><a class="link" href="aktuality/{po['slug']}/">{e(x['more'])} →</a></div></article>''' for po in POSTS[:4])
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
{fonts_head(pre, lang)}
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{GTAG_HEAD}
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body class="article-page">
<a class="skip" href="#obsah">{e(SKIP[lang])}</a>
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo-84.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <nav class="nav nav-simple"><a href="{pre}{LANGS[lang].lstrip("/")}aktuality/">{e(x["nav_news"])}</a><span class="lang">{langs}</span><a class="btn small primary" href="{home}#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>
<article class="post" id="obsah">
 <div class="wrap post-head">
  <p class="kicker">{e(x["news_k"])} · <time datetime="{po.get("event_date", po["date"])}">{e(fmt_post_date(po.get("event_date", po["date"]), lang))}</time></p>
  <h1>{e(P["title"])}</h1>
  <p class="lead">{e(P["perex"])}</p>
 </div>
 <figure class="wrap post-img">{pic(pre, "img/" + po["image"], P["title"], 'fetchpriority="high"')}{('<figcaption>' + e(po["credit"]) + '</figcaption>') if po.get("credit") else ''}</figure>
 <div class="wrap post-body">{body}
  <p class="post-cta"><a class="btn primary" href="{home}#kontakt">{e(t["nav_cta"])}</a> <a class="btn outline" href="{home}">{e(x["back"])}</a></p>
  <h2 class="others-h">{e(x["all_news"])}</h2><ul class="others">{others}</ul>
 </div>
</article>
{footer(lang, pre, langs)}
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
    cards = "".join(f'''<article class="news-card"><a href="{po['slug']}/">{pic(pre, "img/g/" + po['image'], po[lang]['title'])}</a><div><time datetime="{po.get('event_date', po['date'])}">{e(fmt_post_date(po.get('event_date', po['date']), lang))}</time><h3><a href="{po['slug']}/">{e(po[lang]['title'])}</a></h3><p>{e(po[lang]['perex'])}</p><a class="link" href="{po['slug']}/">{e(x['more'])} →</a></div></article>''' for po in POSTS)
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
{fonts_head(pre, lang)}
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
{GTAG_HEAD}
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body class="article-page">
<a class="skip" href="#obsah">{e(SKIP[lang])}</a>
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo-84.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <nav class="nav nav-simple"><span class="lang">{langs}</span><a class="btn small primary" href="{home}#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>
<section class="post" id="obsah"><div class="wrap">
 <p class="kicker">{e(x["news_k"])}</p>
 <h1>{e(x["news_h"])}</h1>
 <div class="news news4 news-arch">{cards}</div>
 <p class="post-cta"><a class="btn outline" href="{home}">{e(x["back"])}</a></p>
</div></section>
{footer(lang, pre, langs)}
</body>
</html>
'''

# ---------- Ochrana osobních údajů (GDPR) ----------
PRIV_SLUG = "ochrana-udaju"
PRIV_LBL = {"cs": "Ochrana osobních údajů", "uk": "Захист персональних даних", "en": "Privacy policy"}
def priv_href(lang, pre): return pre + LANGS[lang].lstrip("/") + PRIV_SLUG + "/"
UOOU = '<a href="https://www.uoou.gov.cz/" target="_blank" rel="noopener">uoou.gov.cz</a>'
MAIL = '<a href="mailto:kupava@kupavabrno.cz">kupava@kupavabrno.cz</a>'
PRIV = {
"cs": dict(
  title="Ochrana osobních údajů",
  lead="Jak Ukrajinský folklorní soubor KUPAVA, z.s. zachází s osobními údaji návštěvníků webu kupavabrno.cz a lidí, kteří nás kontaktují. Platí od 11. listopadu 2026.",
  sections=[
   ("Správce údajů", ["Ukrajinský folklorní soubor KUPAVA, z.s., IČO 23686766, se sídlem Městečko 68, 664 61 Rajhrad, zapsaný u Krajského soudu v Brně, oddíl L, vložka 31074.",
                      f"Kontakt: {MAIL}, tel. +420 777 072 433."]),
   ("Kontaktní formulář a e-mail", ["Když nám napíšete přes formulář nebo e-mailem, zpracujeme vaše jméno, e-mailovou adresu, případně název organizace či akce a text zprávy. Údaje použijeme jen k odpovědi a k navazující komunikaci, například k domluvě vystoupení. Právním základem je náš oprávněný zájem odpovědět na dotaz, případně jednání o smlouvě (čl. 6 odst. 1 písm. f) a b) GDPR).",
                                   "Zprávy uchováváme po dobu nezbytnou k vyřízení a nejdéle tři roky od poslední komunikace.",
                                   "Odeslání formuláře technicky zajišťuje služba FormSubmit (formsubmit.co), která zprávu doručí do naší e-mailové schránky. Zpráva přitom prochází servery této služby, které mohou být i mimo Evropskou unii."]),
   ("Cookies, Google Analytics a Google Ads", ["Ke statistice návštěvnosti a k měření účinnosti našich reklam (program Google Ad Grants pro neziskové organizace) používáme Google Analytics 4 a značku Google Ads společnosti Google Ireland Limited.",
                                              "Analytické a reklamní cookies se ukládají jen s vaším souhlasem, který udělíte v liště cookies (čl. 6 odst. 1 písm. a) GDPR a § 89 odst. 3 zákona č. 127/2005 Sb.). Bez souhlasu web používá režim souhlasu Google (Consent Mode): žádné cookies se neukládají a Google dostává jen omezené signály bez identifikátorů, například že stránka byla zobrazena.",
                                              "Personalizaci reklam nepoužíváme. Data v Google Analytics uchováváme 14 měsíců. Google může údaje zpracovávat i v USA; předávání se řídí rámcem EU–USA pro ochranu osobních údajů (Data Privacy Framework).",
                                              "Souhlas můžete kdykoli změnit nebo odvolat odkazem „Nastavení cookies“ v patičce webu. Vaši volbu si pamatujeme v úložišti vašeho prohlížeče (localStorage)."]),
   ("Videa z YouTube", ["Náhledy videí se načítají ze serveru i.ytimg.com (Google). Samotné video se spustí až po kliknutí, a to v režimu rozšířené ochrany soukromí (youtube-nocookie.com). Teprve potom YouTube zpracovává údaje podle svých zásad."]),
   ("Sociální sítě", ["Na Facebook, Instagram a YouTube na webu pouze odkazujeme. Jejich pluginy ani sledovací kódy nenačítáme."]),
   ("Hosting webu", ["Web běží na službě GitHub Pages (GitHub, Inc., USA). Při návštěvě se zpracovává IP adresa a technické údaje o prohlížeči, které jsou nutné k zobrazení stránky a k ochraně před zneužitím (oprávněný zájem, čl. 6 odst. 1 písm. f) GDPR). Písma jsou uložena přímo na našem webu."]),
   ("Vaše práva", [f"Máte právo na přístup ke svým údajům, na jejich opravu, výmaz, omezení zpracování a přenositelnost, právo vznést námitku a kdykoli odvolat souhlas. Stačí napsat na {MAIL}.",
                   f"Máte také právo podat stížnost u Úřadu pro ochranu osobních údajů ({UOOU})."]),
  ]),
"uk": dict(
  title="Захист персональних даних",
  lead="Як український фольклорний ансамбль «Купава» (Ukrajinský folklorní soubor KUPAVA, z.s.) обробляє персональні дані відвідувачів сайту kupavabrno.cz і людей, які з нами зв’язуються. Діє з 11 листопада 2026 року.",
  sections=[
   ("Контролер даних", ["Ukrajinský folklorní soubor KUPAVA, z.s., IČO 23686766, юридична адреса: Městečko 68, 664 61 Rajhrad (Чехія), зареєстроване Крайовим судом у Брно, розділ L, запис 31074.",
                        f"Контакт: {MAIL}, тел. +420 777 072 433."]),
   ("Контактна форма та e-mail", ["Коли ви пишете нам через форму або e-mail, ми обробляємо ваше ім’я, адресу e-mail, за потреби назву організації чи події та текст повідомлення. Ці дані ми використовуємо лише для відповіді та подальшого спілкування, наприклад щодо виступу. Правова підстава – наш законний інтерес відповісти на запит або переговори щодо договору (ст. 6 ч. 1 п. f) і b) GDPR).",
                                 "Повідомлення зберігаємо стільки, скільки потрібно для їх опрацювання, але не довше трьох років від останнього спілкування.",
                                 "Надсилання форми технічно забезпечує сервіс FormSubmit (formsubmit.co), який доставляє повідомлення до нашої поштової скриньки. Повідомлення проходить через сервери цього сервісу, які можуть бути й поза Європейським Союзом."]),
   ("Файли cookie, Google Analytics і Google Ads", ["Для статистики відвідуваності та вимірювання ефективності нашої реклами (програма Google Ad Grants для неприбуткових організацій) ми використовуємо Google Analytics 4 і тег Google Ads компанії Google Ireland Limited.",
                                                   "Аналітичні та рекламні файли cookie зберігаються лише з вашої згоди, яку ви надаєте на панелі cookie (ст. 6 ч. 1 п. a) GDPR). Без згоди сайт працює в режимі згоди Google (Consent Mode): файли cookie не зберігаються, а Google отримує лише обмежені сигнали без ідентифікаторів, наприклад про перегляд сторінки.",
                                                   "Персоналізацію реклами ми не використовуємо. Дані в Google Analytics зберігаються 14 місяців. Google може обробляти дані й у США; передавання регулює рамкова угода ЄС–США про захист даних (Data Privacy Framework).",
                                                   "Згоду можна будь-коли змінити або відкликати за посиланням «Налаштування файлів cookie» внизу сторінки. Ваш вибір зберігається у сховищі вашого браузера (localStorage)."]),
   ("Відео з YouTube", ["Мініатюри відео завантажуються з сервера i.ytimg.com (Google). Саме відео запускається лише після кліку, у режимі розширеної конфіденційності (youtube-nocookie.com). Лише тоді YouTube обробляє дані відповідно до своїх правил."]),
   ("Соціальні мережі", ["На Facebook, Instagram і YouTube ми лише посилаємося. Їхні плагіни чи коди відстеження на сайті не завантажуються."]),
   ("Хостинг сайту", ["Сайт працює на сервісі GitHub Pages (GitHub, Inc., США). Під час відвідування обробляються IP-адреса та технічні дані браузера, необхідні для показу сторінки та захисту від зловживань (законний інтерес, ст. 6 ч. 1 п. f) GDPR). Шрифти зберігаються безпосередньо на нашому сайті."]),
   ("Ваші права", [f"Ви маєте право на доступ до своїх даних, їх виправлення, видалення, обмеження обробки та перенесення, право заперечити проти обробки та будь-коли відкликати згоду. Достатньо написати на {MAIL}.",
                   f"Ви також маєте право подати скаргу до Управління із захисту персональних даних Чеської Республіки ({UOOU})."]),
  ]),
"en": dict(
  title="Privacy policy",
  lead="How Ukrajinský folklorní soubor KUPAVA, z.s. (the Kupava Ukrainian folk ensemble) handles the personal data of visitors to kupavabrno.cz and of people who contact us. Effective from 11 November 2026.",
  sections=[
   ("Data controller", ["Ukrajinský folklorní soubor KUPAVA, z.s., reg. no. 23686766, registered office Městečko 68, 664 61 Rajhrad, Czech Republic, registered with the Regional Court in Brno, section L, file 31074.",
                        f"Contact: {MAIL}, phone +420 777 072 433."]),
   ("Contact form and e-mail", ["When you write to us via the form or by e-mail, we process your name, e-mail address, where given the name of your organisation or event, and the text of your message. We use these details only to reply and for follow-up communication, for example to arrange a performance. The legal basis is our legitimate interest in answering your enquiry, or steps prior to entering into a contract (Art. 6(1)(f) and (b) GDPR).",
                               "We keep messages for as long as necessary to deal with them and no longer than three years after our last communication.",
                               "The form is delivered by the FormSubmit service (formsubmit.co), which forwards your message to our mailbox. The message passes through this service’s servers, which may be located outside the European Union."]),
   ("Cookies, Google Analytics and Google Ads", ["We use Google Analytics 4 and the Google Ads tag provided by Google Ireland Limited to measure website traffic and the effectiveness of our ads (the Google Ad Grants programme for non-profits).",
                                                "Analytics and advertising cookies are stored only with your consent, given in the cookie bar (Art. 6(1)(a) GDPR). Without consent the website uses Google Consent Mode: no cookies are stored and Google receives only limited signals without identifiers, such as the fact that a page was viewed.",
                                                "We do not use ad personalisation. Google Analytics data is kept for 14 months. Google may also process data in the USA; such transfers are covered by the EU–US Data Privacy Framework.",
                                                "You can change or withdraw your consent at any time via the “Cookie settings” link in the footer. Your choice is remembered in your browser’s local storage."]),
   ("YouTube videos", ["Video thumbnails are loaded from i.ytimg.com (Google). A video only starts after you click it, in YouTube’s privacy-enhanced mode (youtube-nocookie.com). Only then does YouTube process data under its own policy."]),
   ("Social networks", ["We only link to Facebook, Instagram and YouTube. We do not load their plugins or tracking code."]),
   ("Website hosting", ["The website is hosted on GitHub Pages (GitHub, Inc., USA). When you visit, your IP address and technical browser data are processed as needed to deliver the page and protect against abuse (legitimate interest, Art. 6(1)(f) GDPR). Fonts are served directly from our own website."]),
   ("Your rights", [f"You have the right to access your data, to have it corrected or erased, to restrict its processing and to data portability, the right to object and the right to withdraw consent at any time. Just write to {MAIL}.",
                    f"You also have the right to lodge a complaint with the Czech Office for Personal Data Protection ({UOOU})."]),
  ]),
}

def privacy(lang):
    t = T[lang]; x = X[lang]; P = PRIV[lang]
    depth = 1 if lang == "cs" else 2
    pre = "../" * depth
    name = "Купава" if lang == "uk" else "Kupava"
    url = BASE + LANGS[lang] + PRIV_SLUG + "/"
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{LANGS[l]}{PRIV_SLUG}/">' for l in LANGS)
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join(f'<a href="{pre}{LANGS[l].lstrip("/")}{PRIV_SLUG}/" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    home = pre + ("" if lang == "cs" else lang + "/")
    body = "".join(f'<h2>{e(h)}</h2>' + "".join(f'<p>{p}</p>' for p in ps) for h, ps in P["sections"])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(P["title"])} – {name}</title>
<meta name="description" content="{e(P["lead"])}">
<meta name="theme-color" content="#1c2f5a">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/icon-192.png">
{fonts_head(pre, lang)}
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">
{GTAG_HEAD}
<script src="{pre}assets/consent.js?v={VER}" defer></script>
</head>
<body class="article-page">
<a class="skip" href="#obsah">{e(SKIP[lang])}</a>
<header class="top"><div class="wrap">
 <a class="brand" href="{home}"><img src="{pre}img/logo-84.png" alt="" width="42" height="42"><span><b>{name}</b><small>{e(t["brand_sub"])}</small></span></a>
 <nav class="nav nav-simple"><span class="lang">{langs}</span><a class="btn small primary" href="{home}#kontakt">{e(t["nav_cta"])}</a></nav>
</div></header>
<article class="post" id="obsah">
 <div class="wrap post-head">
  <h1>{e(P["title"])}</h1>
  <p class="lead">{e(P["lead"])}</p>
 </div>
 <div class="wrap post-body privacy">{body}
  <p class="post-cta"><a class="btn outline" href="{home}">{e(x["back"])}</a></p>
 </div>
</article>
{footer(lang, pre, langs)}
</body>
</html>
'''

for lang in LANGS:
    ap = os.path.join(OUT, LANGS[lang].lstrip("/"), PRIV_SLUG, "index.html")
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap, "w").write(privacy(lang))

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
AI_BOTS = ["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-User","Claude-SearchBot","PerplexityBot","Perplexity-User","Google-Extended","Applebot-Extended","Bingbot","CCBot"]
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\n# AI vyhledávače a asistenti – vítáni\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS) + f"Sitemap: {BASE}/sitemap.xml\n")
# llms.txt – stručný přehled pro jazykové modely (https://llmstxt.org)
hl_lines = "\n".join(f"- {ev['date'][:4]}: {ev['en']} ({ev['place']['en']})" for ev in HIGHLIGHTS)
up_lines = "\n".join(f"- {ev['date']}: {ev['en']} ({ev['place']['en']})" for ev in UPCOMING) or "- (none announced)"
faq_md = "\n".join(f"### {q}\n{a}\n" for q, a in faq_items("en"))
llms = f"""# Kupava – Ukrainian folk ensemble and choir from Brno (Czech Republic)

> Kupava (Купава; Ukrajinský folklorní soubor KUPAVA, z.s.) is a Ukrainian folk ensemble and choir based in Brno, Czech Republic, founded in February 2023. It performs traditional Ukrainian polyphonic singing – folk songs from many regions of Ukraine, Christmas carols (koliadky) and New Year songs (shchedrivky) – in traditional costume and with live music. Artistic director: Kateryna Mykhaylova. Website in Czech, Ukrainian and English.

## Key facts
- Type: Ukrainian folk ensemble / folk choir (Czech: ukrajinský folklorní soubor, pěvecký sbor; Ukrainian: український фольклорний ансамбль, хор)
- Based in: Brno, Czech Republic (registered office Rajhrad), non-profit association, Reg. no. 23686766
- Founded: February 2023, with the support of the Ukrainian Centre in Brno
- Performances: {N_PAST} since 2023 in the Czech Republic, Slovakia and Austria, incl. the Strážnice International Folklore Festival, Smetana’s Litomyšl, the Chod Festival, Jánošík’s Ducat and a live TV Noe broadcast (Concert for Life II, 2025)
- Programmes: Old Ukrainian Christmas (carols and shchedrivky with the Christmas star); Songs of Ukraine’s Regions
- Contact: kupava@kupavabrno.cz, +420 777 072 433

## Selected performances
{hl_lines}

## Upcoming
{up_lines}

## Pages
- [Czech home page]({BASE}/): about, repertoire, performances, video, gallery, press kit, contact
- [Ukrainian home page]({BASE}/uk/)
- [English home page]({BASE}/en/)
- [News (CZ)]({BASE}/aktuality/), [News (UK)]({BASE}/uk/aktuality/), [News (EN)]({BASE}/en/aktuality/)
- [Press kit (ZIP)]({BASE}/press/kupava-press-kit.zip)
- [Privacy policy]({BASE}/en/ochrana-udaju/)

## FAQ
{faq_md}
## Social
- Facebook: https://www.facebook.com/KupavaBrno
- Instagram: https://www.instagram.com/soubor_kupava/
- YouTube: https://www.youtube.com/playlist?list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5
"""
open(os.path.join(OUT, "llms.txt"), "w").write(llms)
open(os.path.join(OUT, "CNAME"), "w").write("kupavabrno.cz\n")
print(f"ok – {N_PAST} minulých vystoupení, {len(HIGHLIGHTS)} významných, {len(UPCOMING)} připravovaných")
