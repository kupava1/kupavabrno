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
    cs: {text:'Používáme cookies Google Analytics a Google Ads, abychom věděli, jak návštěvníci web používají a jak fungují naše reklamy. Bez vašeho souhlasu cookies neukládáme.', yes:'Povolit', no:'Odmítnout', settings:'Nastavení cookies'},
    uk: {text:'Ми використовуємо cookies Google Analytics і Google Ads, щоб розуміти, як відвідувачі користуються сайтом і як працює наша реклама. Без вашої згоди cookies не зберігаються.', yes:'Дозволити', no:'Відхилити', settings:'Налаштування cookies'},
    en: {text:'We use Google Analytics and Google Ads cookies to understand how visitors use this website and how our ads perform. Without your consent, no cookies are stored.', yes:'Allow', no:'Decline', settings:'Cookie settings'}
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
