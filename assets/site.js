(function(){
  function track(name, params){ if (typeof window.gtag==='function') window.gtag('event', name, params||{}); }

  // mobilní menu
  var btn=document.querySelector('.menu-btn'), nav=document.querySelector('.nav');
  btn.addEventListener('click', function(){ var o=nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
  nav.querySelectorAll('a[href^="#"]').forEach(function(a){ a.addEventListener('click', function(){ nav.classList.remove('open'); btn.setAttribute('aria-expanded', false); }); });

  // YouTube – iframe se načte až po kliknutí
  document.querySelectorAll('.yt').forEach(function(el){
    el.addEventListener('click', function(){
      var id=el.getAttribute('data-id');
      // přehrávač patří do obyčejného bloku (ne do tlačítka) a bez ikonky přes video – jinak nejde ovládat (pauza apod.)
      var box=document.createElement('div'); box.className='yt playing';
      box.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1" title="'+(el.getAttribute('aria-label')||'Video')+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      el.parentNode.replaceChild(box, el);
      track('video_play', {video_id:id});
    }, {once:true});
  });

  // galerie
  var links=[].slice.call(document.querySelectorAll('.gallery a')), lb=document.querySelector('.lb'), lbImg=lb.querySelector('img'), cur=0;
  function show(i){ cur=(i+links.length)%links.length; lbImg.src=links[cur].href; lbImg.alt=links[cur].querySelector('img').alt; }
  links.forEach(function(a,i){ a.addEventListener('click', function(ev){ ev.preventDefault(); show(i); lb.classList.add('open'); }); });
  lb.querySelector('.x').onclick=function(){ lb.classList.remove('open'); };
  lb.querySelector('.p').onclick=function(ev){ ev.stopPropagation(); show(cur-1); };
  lb.querySelector('.n').onclick=function(ev){ ev.stopPropagation(); show(cur+1); };
  lb.addEventListener('click', function(ev){ if(ev.target===lb) lb.classList.remove('open'); });
  document.addEventListener('keydown', function(ev){ if(!lb.classList.contains('open')) return; if(ev.key==='Escape') lb.classList.remove('open'); if(ev.key==='ArrowLeft') show(cur-1); if(ev.key==='ArrowRight') show(cur+1); });

  // okno s formulářem
  var dlg=document.getElementById('form-dialog');
  if(dlg){
    document.querySelectorAll('[data-open-form]').forEach(function(b){ b.addEventListener('click', function(ev){
      ev.preventDefault(); nav.classList.remove('open');
      if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');
      var first=dlg.querySelector('input:not([type=hidden]):not(.hp)'); if(first) first.focus();
      track('form_open');
    }); });
    dlg.querySelector('[data-close-form]').addEventListener('click', function(){ dlg.close(); });
    dlg.addEventListener('click', function(ev){
      if(ev.target!==dlg) return;
      var r=dlg.getBoundingClientRect();
      if(ev.clientX<r.left||ev.clientX>r.right||ev.clientY<r.top||ev.clientY>r.bottom) dlg.close();
    });
  }

  // kopírování medailonku
  document.querySelectorAll('[data-copy]').forEach(function(b){ b.addEventListener('click', function(){
    var el=document.getElementById(b.getAttribute('data-copy')); if(!el) return;
    var txt=el.textContent, label=b.textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function(){ b.textContent=b.dataset.copied; setTimeout(function(){ b.textContent=label; },2000); }).catch(function(){});
    track('press_bio_copy');
  }); });
  document.querySelectorAll('a[download]').forEach(function(a){ a.addEventListener('click', function(){ track('file_download',{file_name:a.getAttribute('href')}); }); });

  // kontaktní formulář – odeslání přímo z webu
  var form=document.getElementById('contact-form');
  if(form){
    var status=form.querySelector('.form-status'), submit=form.querySelector('button[type=submit]');
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      if(form._honey && form._honey.value) return;
      submit.disabled=true; submit.textContent=form.dataset.sending; status.className='full form-status'; status.textContent='';
      var data={}; new FormData(form).forEach(function(v,k){ data[k]=v; });
      data._replyto=data.email;
      fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
        .then(function(r){ return r.json().then(function(j){ return {ok:r.ok && String(j.success)!=='false'}; }); })
        .then(function(res){
          if(!res.ok) throw new Error('send');
          status.textContent=form.dataset.ok; status.classList.add('ok'); form.reset();
          track('generate_lead', {form:'contact'});
        })
        .catch(function(){ status.textContent=form.dataset.err; status.classList.add('err'); })
        .finally(function(){ submit.disabled=false; submit.textContent=form.dataset.send; });
    });
  }
  document.querySelectorAll('a[href^="mailto:"]').forEach(function(a){ a.addEventListener('click', function(){ track('contact_email'); }); });
  document.querySelectorAll('a[href^="tel:"]').forEach(function(a){ a.addEventListener('click', function(){ track('contact_phone'); }); });
})();
