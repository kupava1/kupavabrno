/* Souhlas s cookies + Google Analytics 4 (načte se až po souhlasu návštěvníka) */
(function(){
  var GA_ID = 'G-X6NC9E6Y45', ADS_ID = 'AW-18567655723', KEY = 'kupava_consent_v1';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };

  var lang = (document.documentElement.lang || 'cs').slice(0,2);
  var T = {
    cs: {text:'Používáme analytické cookies (Google Analytics), abychom věděli, jak návštěvníci web používají. Pomůžete nám, když je povolíte.', yes:'Povolit', no:'Odmítnout', settings:'Nastavení cookies'},
    uk: {text:'Ми використовуємо аналітичні cookies (Google Analytics), щоб розуміти, як відвідувачі користуються сайтом. Ви нам допоможете, якщо дозволите їх.', yes:'Дозволити', no:'Відхилити', settings:'Налаштування cookies'},
    en: {text:'We use analytics cookies (Google Analytics) to understand how visitors use this website. You help us by allowing them.', yes:'Allow', no:'Decline', settings:'Cookie settings'}
  }[lang] || null;
  if(!T) T = {text:'', yes:'OK', no:'No', settings:'Cookies'};

  function get(){ try { return localStorage.getItem(KEY); } catch(e){ return null; } }
  function set(v){ try { localStorage.setItem(KEY, v); } catch(e){} }

  function loadGA(){
    if (window.__gaLoaded) return; window.__gaLoaded = true;
    gtag('consent','default',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted',ad_personalization:'denied'});
    gtag('js', new Date());
    gtag('config', GA_ID, {anonymize_ip:true});
    gtag('config', ADS_ID);
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function banner(){
    if (document.getElementById('cookie-bar')) return;
    var b = document.createElement('div'); b.id = 'cookie-bar'; b.setAttribute('role','dialog'); b.setAttribute('aria-live','polite');
    b.innerHTML = '<p>'+T.text+'</p><div class="cb-btns"><button type="button" class="btn small outline cb-no">'+T.no+'</button><button type="button" class="btn small primary cb-yes">'+T.yes+'</button></div>';
    document.body.appendChild(b);
    b.querySelector('.cb-yes').onclick = function(){ set('granted'); b.remove(); loadGA(); };
    b.querySelector('.cb-no').onclick = function(){ set('denied'); b.remove(); };
  }

  function footerLink(){
    var f = document.querySelector('footer .foot > div'); if(!f) return;
    var a = document.createElement('a'); a.href = '#'; a.textContent = T.settings; a.className = 'cookie-link';
    a.onclick = function(e){ e.preventDefault(); banner(); };
    f.appendChild(document.createElement('br')); f.appendChild(a);
  }

  function init(){
    var c = get();
    if (c === 'granted') loadGA(); else if (c !== 'denied') banner();
    footerLink();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
