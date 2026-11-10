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

VIDEOS = [
 ("a9-As9ocu7A", "Ой, устану ранесенько", {"cs":"Babylonfest, Brno 2023","uk":"Babylonfest, Брно 2023","en":"Babylonfest, Brno 2023"}),
 ("fvsroGsIgNk", "Славен єси", {"cs":"Ukrajinské koledy","uk":"Українські колядки","en":"Ukrainian carols"}),
 ("ptXL8v-0SIU", "Зеленеє жито, зелене", {"cs":"Babylonfest, Brno 2023","uk":"Babylonfest, Брно 2023","en":"Babylonfest, Brno 2023"}),
]

GALLERY = [
 ("soubor-prerov", {"cs":"Kupava v Přerově","uk":"«Купава» у Пршерові","en":"Kupava in Přerov"}),
 ("koledy-podium-kostel", {"cs":"Staroukrajinské Vánoce","uk":"Староукраїнське Різдво","en":"Old Ukrainian Christmas"}),
 ("koledy-moravske-namesti", {"cs":"Vánoční koledování v Brně","uk":"Різдвяне колядування в Брно","en":"Christmas carolling in Brno"}),
 ("housle-podium", {"cs":"Živá hudba na pódiu","uk":"Жива музика на сцені","en":"Live music on stage"}),
 ("vinok-portret", {"cs":"Zpěvačka ve věnci","uk":"Співачка у вінку","en":"Singer wearing a floral wreath"}),
 ("zpev-radost", {"cs":"Vícehlasý zpěv","uk":"Багатоголосий спів","en":"Polyphonic singing"}),
 ("kroje-detail", {"cs":"Vyšívané kroje a korále","uk":"Вишиті строї та коралі","en":"Embroidered costumes and coral beads"}),
 ("soubor-v-krojich", {"cs":"Vánoční koncert","uk":"Різдвяний концерт","en":"Christmas concert"}),
 ("koledy-hvezda", {"cs":"Koledy s vánoční hvězdou","uk":"Колядки з різдвяною зіркою","en":"Carols with the Christmas star"}),
 ("zpevacky-podium", {"cs":"Zpěvačky v krojích","uk":"Співачки у строях","en":"Singers in traditional dress"}),
 ("akordeon", {"cs":"Harmonika","uk":"Акордеон","en":"Accordion"}),
 ("soubor-straznice", {"cs":"MFF Strážnice","uk":"МФФ у Стражніце","en":"Strážnice Folklore Festival"}),
 ("zpev-vinok", {"cs":"Sólový zpěv","uk":"Сольний спів","en":"Solo singing"}),
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
  lead="Autentický vícehlasý zpěv a živá lidová hudba z různých regionů Ukrajiny.",
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
  tv_p="V dubnu 2025 vystoupila Kupava v Ostravě v přímém přenosu benefičního Koncertu pro život II na podporu Ukrajiny, který vysílala TV Noe. Na jednom pódiu spolu s Pavlem Helanem, kapelou Sonjašnyk se smyčcovým kvartetem a dětským sborem Spivanočky.",
  tv_meta="6. dubna 2025 · Ostrava · TV Noe",
  rep_k="Repertoár", rep_h="Koncertní programy",
  progs=[("program-vanoce","Staroukrajinské Vánoce","Koledy a ščedrivky s vánoční hvězdou. Sváteční program, který každoročně uvádíme v Brně a ve Vídni."),
         ("program-regiony","Písně ukrajinských regionů","Lyrické, obřadní a taneční písně v autentickém vícehlasu s živou hudbou – pro festivaly, koncertní sály a kulturní události.")],
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
  lead="Автентичний багатоголосий спів і жива народна музика з різних регіонів України.",
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
  tv_p="У квітні 2025 року «Купава» виступила в Остраві в прямому ефірі благодійного «Концерту для життя II» на підтримку України, який транслювало TV Noe. На одній сцені з Павлом Геланом, гуртом «Соняшник» зі струнним квартетом і дитячим хором «Співаночки».",
  tv_meta="6 квітня 2025 · Острава · TV Noe",
  rep_k="Репертуар", rep_h="Концертні програми",
  progs=[("program-vanoce","Староукраїнське Різдво","Колядки й щедрівки з різдвяною зіркою. Святкова програма, яку ми щороку представляємо в Брно та Відні."),
         ("program-regiony","Пісні українських регіонів","Ліричні, обрядові й танцювальні пісні в автентичному багатоголоссі з живою музикою – для фестивалів, концертних залів і культурних подій.")],
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
  lead="Authentic Ukrainian polyphonic singing and live folk music from many regions of Ukraine.",
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
  tv_p="In April 2025 Kupava performed in Ostrava in the live broadcast of the charity Concert for Life II in support of Ukraine, aired by TV Noe – sharing the stage with Pavel Helan, the band Sonjašnyk with a string quartet, and the Spivanočky children’s choir.",
  tv_meta="6 April 2025 · Ostrava · TV Noe",
  rep_k="Repertoire", rep_h="Concert programmes",
  progs=[("program-vanoce","Old Ukrainian Christmas","Carols and shchedrivky with the Christmas star – a festive programme we present every year in Brno and Vienna."),
         ("program-regiony","Songs of Ukraine’s Regions","Lyrical, ritual and dance songs in authentic polyphony with live music – for festivals, concert halls and cultural events.")],
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

ORN = '<svg class="orn" viewBox="0 0 120 12" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M0 6h44M76 6h44"/><path d="M60 1l5 5-5 5-5-5z"/><path d="M50 3l3 3-3 3-3-3zM70 3l3 3-3 3-3-3z"/></g></svg>'

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
    nav = "".join(f'<a href="{h}">{e(n)}</a>' for h, n in t["nav"])
    LBL = {"cs":"CZ","uk":"UA","en":"EN"}; CUR = ' aria-current="page"'
    langs = "".join('<a href="' + (pre + ("" if l=="cs" else l+"/") or "./") + f'" hreflang="{l}" lang="{l}"' + (CUR if l==lang else "") + f'>{LBL[l]}</a>' for l in LANGS)
    stats = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in t["stats"])
    stages = "".join(f'<li>{e(s)}</li>' for s in t["stages"])
    about = "".join(f"<p>{p}</p>" for p in t["about_p"])
    pillars = "".join(f'<div class="pillar"><span class="num">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(t["pillars"]))
    progs = "".join(f'<article class="prog"><img src="{pre}img/g/{img}.jpg" alt="{e(h)}" loading="lazy" width="760" height="506"><div><h3>{e(h)}</h3><p>{e(p)}</p></div></article>' for img, h, p in t["progs"])
    if lang == "uk":
        rep = "".join(f'<li><b>{e(o)}</b></li>' for o, c, en in REPERTOIRE)
    else:
        rep = "".join(f'<li><b>{e(c if lang=="cs" else en)}</b><span lang="uk">{e(o)}</span></li>' for o, c, en in REPERTOIRE)
    hl = "".join(f'<li><time>{e(fdate(ev, lang))}</time><b>{e(ev[lang])}</b><span>{e(ev["place"][lang])}</span></li>' for ev in HIGHLIGHTS)
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
<!-- GOOGLE-TAG -->
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
 <div class="about-pic"><img src="{pre}img/zpev-podium.jpg" alt="{e(GALLERY[4][1][lang])}" loading="lazy"></div>
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
 <div class="rep">
  <div class="progs">{progs}</div>
  <aside class="songs"><h3>{e(t["rep_list"])}</h3><ul>{rep}</ul><p>{e(t["rep_note"])}</p></aside>
 </div>
</div></section>

<section id="vystoupeni" class="soft"><div class="wrap">
 <p class="kicker">{e(t["perf_k"])}</p>
 <h2>{e(t["perf_h"])}</h2>
 <div class="perf-grid">
  <div>{up}<ul class="hl">{hl}</ul><p class="perf-note">{e(t["perf_note"])}</p></div>
  <blockquote>{e(t["quote"])}<cite><a href="https://www.ceskenoviny.cz/zpravy/2616128" target="_blank" rel="noopener">{e(t["quote_src"])}</a></cite></blockquote>
 </div>
</div></section>

<section id="video"><div class="wrap">
 <div class="sec-head"><div><p class="kicker">{e(t["vid_k"])}</p><h2>{e(t["vid_h"])}</h2></div><a class="link" href="https://www.youtube.com/watch?v=qvbnvvhpYXQ&amp;list=PLs8RLUolQE94t0YRGZ3u8ZIh3bfrB9ls5" target="_blank" rel="noopener">{e(t["vid_more"])} ↗</a></div>
 <div class="videos">{vids}</div>
</div></section>

<section id="galerie" class="soft"><div class="wrap">
 <p class="kicker">{e(t["gal_k"])}</p>
 <h2>{e(t["gal_h"])}</h2>
 <div class="gallery">{gal}</div>
</div></section>

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

for lang in LANGS:
    path = os.path.join(OUT, "" if lang == "cs" else lang, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(page(lang))
LASTMOD = datetime.date.today().isoformat()
open(os.path.join(OUT, "404.html"), "w").write(f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stránka nenalezena – Kupava</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/style.css?v={VER}"></head><body><section class="hero" style="padding:120px 0 140px"><div class="wrap hero-text"><h1><span class="eyebrow">404</span><span class="h1-name">Kupava</span></h1><p class="lead">Stránka nenalezena · Сторінку не знайдено · Page not found</p><div class="btns"><a class="btn light" href="/">Čeština</a><a class="btn outline-light" href="/uk/">Українська</a><a class="btn outline-light" href="/en/">English</a></div></div></section></body></html>''')
open(os.path.join(OUT, "sitemap.xml"), "w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
 "".join(f'<url><loc>{BASE}{p}</loc><lastmod>{LASTMOD}</lastmod>' + "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{BASE}{p2}"/>' for l2, p2 in LANGS.items()) + '</url>\n' for p in LANGS.values()) + '</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(OUT, "CNAME"), "w").write("kupavabrno.cz\n")
print(f"ok – {N_PAST} minulých vystoupení, {len(HIGHLIGHTS)} významných, {len(UPCOMING)} připravovaných")
