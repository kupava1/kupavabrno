/* Lišta souhlasu s cookies – Google Consent Mode v2.
   Značka Google (GA4 + Google Ads) se načítá v hlavičce stránky s výchozím stavem „zamítnuto“:
   bez souhlasu se neukládají žádné cookies, Google dostává jen anonymní signály bez identifikace.
   Po kliknutí na „Povolit“ se souhlas aktualizuje a měření se plně zapne. */
(function(){
  var KEY = 'kupava_consent_v1';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };

  var lang = (document.documentElement.lang || 'cs').slice(0,2);
  var T = {
    cs: {text:'<b>Koledníci chodí jen tam, kde jim otevřou dveře.</b> Stejně tak naše cookies: bez vašeho svolení si nevezmeme ani drobek. Když je pustíte dál, Google Analytics a Google Ads nám prozradí, jak se vám u nás líbí a jak fungují naše reklamy.', yes:'Otevřít dveře (povolit)', no:'Ne, děkuji', settings:'Nastavení cookies'},
    uk: {text:'<b>Колядники заходять лише туди, де їм відчиняють двері.</b> Так і наші cookies: без вашого дозволу не візьмемо й крихти. Якщо впустите їх, Google Analytics і Google Ads підкажуть нам, як вам у нас подобається і як працює наша реклама.', yes:'Відчинити двері (дозволити)', no:'Ні, дякую', settings:'Налаштування cookies'},
    en: {text:'<b>Carol singers only come in where the door is opened.</b> Our cookies are the same: without your permission we won’t take a single crumb. If you let them in, Google Analytics and Google Ads tell us how you like our website and how our ads are doing.', yes:'Open the door (allow)', no:'No, thank you', settings:'Cookie settings'}
  }[lang] || {text:'', yes:'OK', no:'No', settings:'Cookies'};

  function get(){ try { return localStorage.getItem(KEY); } catch(e){ return null; } }
  function set(v){ try { localStorage.setItem(KEY, v); } catch(e){} }

  function update(granted){
    var v = granted ? 'granted' : 'denied';
    gtag('consent','update',{ad_storage:v, ad_user_data:v, analytics_storage:v, ad_personalization:'denied'});
  }

  function banner(){
    if (document.getElementById('cookie-bar')) return;
    var b = document.createElement('div'); b.id = 'cookie-bar'; b.setAttribute('role','dialog'); b.setAttribute('aria-live','polite');
    b.innerHTML = '<p>'+T.text+'</p><div class="cb-btns"><button type="button" class="btn small outline cb-no">'+T.no+'</button><button type="button" class="btn small primary cb-yes">'+T.yes+'</button></div>';
    document.body.appendChild(b);
    b.querySelector('.cb-yes').onclick = function(){ set('granted'); b.remove(); update(true); };
    b.querySelector('.cb-no').onclick = function(){ set('denied'); b.remove(); update(false); };
  }

  function footerLink(){
    var f = document.querySelector('footer .foot > div'); if(!f) return;
    var a = document.createElement('a'); a.href = '#'; a.textContent = T.settings; a.className = 'cookie-link';
    a.onclick = function(e){ e.preventDefault(); banner(); };
    f.appendChild(document.createElement('br')); f.appendChild(a);
  }

  function init(){
    var c = get();
    if (c !== 'granted' && c !== 'denied') banner();
    footerLink();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
