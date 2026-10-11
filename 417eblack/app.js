(function(){
  var C = window.SITE_CONFIG || {};
  var phone = (C.phone||"").replace(/\D/g,"");
  var pretty = phone.length===10 ? "("+phone.slice(0,3)+") "+phone.slice(3,6)+"-"+phone.slice(6) : "";
  var smsBody = encodeURIComponent("Hi, I'm interested in the office suites at 417 E Black St.");
  document.querySelectorAll("[data-tel]").forEach(function(a){
    if(!phone){a.href="#tour";return;} a.href="tel:+1"+phone; a.title=pretty;});
  document.querySelectorAll("[data-sms]").forEach(function(a){
    if(!phone){a.href="#tour";return;} a.href="sms:+1"+phone+"?&body="+smsBody;});

  if (pretty) document.querySelectorAll(".contact-btns [data-tel]").forEach(function(a){ a.lastChild.textContent=" Call "+pretty; });

  // hide offer after deadline
  if (C.offerEnds && Date.now() > new Date(C.offerEnds).getTime())
    document.querySelectorAll("[data-offer]").forEach(function(e){e.classList.add("off");});

  // remember where the visitor came from (e.g. ?src=fb-rockhill-biz)
  var q = new URLSearchParams(location.search);
  var src = q.get("src") || q.get("utm_source") || "";
  try { if (src) sessionStorage.setItem("src", src); else src = sessionStorage.getItem("src") || ""; } catch(e){}
  if (!src && document.referrer) { try { src = new URL(document.referrer).hostname; } catch(e){} }

  // "Book a tour" on a suite card preselects that suite
  var sel = document.querySelector('#tour-form select[name="suite"]');
  document.querySelectorAll("[data-suite]").forEach(function(a){
    a.addEventListener("click", function(){
      var n=a.getAttribute("data-suite");
      [].forEach.call(sel.options,function(o,i){ if(o.text.indexOf(n+" ")===0) sel.selectedIndex=i; });
    });
  });

  // share button on suite pages
  document.querySelectorAll("[data-share]").forEach(function(b){
    b.addEventListener("click", function(){
      var d={title:document.title,url:location.origin+location.pathname};
      if (navigator.share) navigator.share(d).catch(function(){});
      else if (navigator.clipboard) navigator.clipboard.writeText(d.url).then(function(){b.textContent="Link copied";});
    });
  });

  // tour form
  var f = document.getElementById("tour-form"); if(!f) return;
  var msg = f.querySelector(".form-msg");
  f.addEventListener("submit", function(ev){
    ev.preventDefault();
    if (f.company_site.value) return; // bot
    var ok = true;
    ["name","phone"].forEach(function(k){ var el=f[k]; var bad=!el.value.trim(); el.classList.toggle("invalid",bad); if(bad) ok=false; });
    if (f.phone.value.replace(/\D/g,"").length < 10) { f.phone.classList.add("invalid"); ok=false; }
    if (!ok){ msg.className="form-msg err"; msg.textContent="Please add your name and a 10-digit phone number."; return; }
    var lead = { name:f.name.value.trim(), phone:f.phone.value.trim(), email:f.email.value.trim(),
      suite:f.suite.value, business:f.business.value.trim(), move_in:f.move_in.value.trim(),
      notes:f.notes.value.trim(), source:src, page:location.pathname };
    var btn=f.querySelector("button"); btn.disabled=true; btn.textContent="Sending…";
    function done(){ f.reset(); btn.textContent="Request sent"; msg.className="form-msg ok";
      msg.textContent="Thanks, "+lead.name.split(" ")[0]+"! We'll reach out within 15 minutes during business hours."+(pretty?" Need us sooner? Call or text "+pretty+".":""); }
    function fallback(){
      btn.disabled=false; btn.textContent="Request a tour";
      var body = "Tour request - 417 E Black St%0A%0A" + Object.keys(lead).map(function(k){return k+": "+encodeURIComponent(lead[k]);}).join("%0A");
      if (phone) { location.href="sms:+1"+phone+"?&body="+encodeURIComponent("Tour request 417 E Black: "+lead.name+", "+lead.phone+", "+lead.suite); done(); }
      else if (C.email) { location.href="mailto:"+C.email+"?subject="+encodeURIComponent("Tour request: "+lead.suite)+"&body="+body; done(); }
      else { msg.className="form-msg err"; msg.textContent="Sorry, something went wrong. Please try again shortly."; }
    }
    if (!C.email) return fallback();
    var payload = Object.assign({
      _subject: "Tour request: " + lead.suite + " - 417 E Black St",
      _template: "table", _captcha: "false", _replyto: lead.email || undefined
    }, lead);
    fetch("https://formsubmit.co/ajax/" + C.email, {method:"POST",
      headers:{"Content-Type":"application/json","Accept":"application/json"},
      body:JSON.stringify(payload)})
      .then(function(r){ return r.json(); })
      .then(function(j){ if (String(j.success) !== "true") throw 0; done(); })
      .catch(fallback);
  });
})();
