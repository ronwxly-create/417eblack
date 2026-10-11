#!/usr/bin/env python3
"""Generates the 417 E Black St listing site into /mnt/user-data/outputs/417eblack."""
import json, html
OUT = '/mnt/user-data/outputs/417eblack/'
SITE = 'https://417eblack.com'   # change once the domain is picked

SUITES = {
  'office-1': dict(n='Office 1', sf=179, rent=595, tag='Fits a 2–3 person team',
     blurb='Bright front office with three windows and room for up to three workstations. Great for a small practice, CPA or insurance team.',
     feats=['Three windows, lots of natural light','Up to 3 workstations','Built-in desks']),
  'office-2': dict(n='Office 2', sf=122, rent=625, tag='Bay window · L-shaped desks',
     blurb='Private office with a bay window and L-shaped built-in desks. Ideal for a counselor, coach, advisor or solo professional.',
     feats=['Bay window','L-shaped built-in desks','Quiet, private layout']),
  'office-6': dict(n='Office 6', sf=154, rent=650, tag='Built-in shelving · window desk',
     blurb='Private office with built-in shelving and a window desk. Ideal for a therapist, solo attorney or advisor.',
     feats=['Built-in shelving','Window desk','Separate from the main hall']),
}
INCLUDED = [('door','Private exterior entrance'),('bath','Private bathroom'),('desk','Built-in desks'),
            ('temp','Your own HVAC & thermostat'),('wifi','Utilities & Wi-Fi included'),('car','14 free dedicated parking spaces'),
            ('people','Shared conference room'),('clock','24-hour access'),('cup','Coffee station & microwave')]
ICON = {
 'door':'<path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17M3 21h18M14 12h.01"/>',
 'bath':'<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-3zM6 12V5a2 2 0 0 1 4 0M7 20l-1 2M17 20l1 2"/>',
 'desk':'<path d="M3 8h18M5 8v12M19 8v12M5 13h6v7"/>',
 'temp':'<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/>',
 'wifi':'<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 19.5h.01"/>',
 'car':'<path d="M5 17h14M6 17v2M18 17v2M4 13l2-6h12l2 6v4H4v-4zM7.5 14h.01M16.5 14h.01"/>',
 'people':'<path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20a6 6 0 0 1 12 0M17 11a3 3 0 1 0 0-6M21 20a6 6 0 0 0-4-5.6"/>',
 'clock':'<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2"/>',
 'cup':'<path d="M4 8h12v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8zM16 10h2a2 2 0 0 1 0 4h-2M8 2v3M12 2v3"/>',
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'msg':'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11zM12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>',
}
def ic(k, cls='ic'): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

CSS = open('/tmp/claude-0/-home-claude/43978b19-c0b9-559a-8fb0-2125dfe162af/scratchpad/style.css').read()

def suite_card(k, s, featured=False):
    feats = ''.join(f'<li>{f}</li>' for f in s['feats'])
    return f'''<article class="suite{' featured' if featured else ''}" id="{k}">
  <a class="suite-img" href="/{k}"><img src="/img/{k}.jpg" alt="{s['n']} interior, {s['sf']} square feet" loading="lazy" width="640" height="480"></a>
  <div class="suite-body">
    <div class="suite-top"><h3>{s['n']}</h3><span class="sf">{s['sf']} SF</span></div>
    <p class="price">${s['rent']}<span>/mo all-in</span></p>
    <p class="tag">{s['tag']}</p>
    <ul class="feats">{feats}</ul>
    <div class="suite-actions">
      <a class="btn btn-primary" href="#tour" data-suite="{s['n']}">Book a tour</a>
      <a class="btn btn-ghost" href="/{k}">Details &amp; share</a>
    </div>
  </div>
</article>'''

def page(slug, title, desc, og, hero_html, main_html, preselect=''):
    url = SITE + ('/' if slug == 'index' else '/' + slug)
    opts = ''.join(f'<option{" selected" if s["n"]==preselect else ""}>{s["n"]} · {s["sf"]} SF · ${s["rent"]}/mo</option>' for s in SUITES.values())
    included = ''.join(f'<li>{ic(k)}<span>{t}</span></li>' for k, t in INCLUDED)
    ld = {"@context":"https://schema.org","@type":"Offer","name":title,"url":url,
          "itemOffered":{"@type":"Place","name":"417 E Black Street Executive Office Suites",
          "address":{"@type":"PostalAddress","streetAddress":"417 E Black St","addressLocality":"Rock Hill","addressRegion":"SC","postalCode":"29730"}}}
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="417 E Black St Office Suites">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e1b2e">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230e1b2e'/%3E%3Crect x='9' y='12' width='6' height='6' fill='%230085ba'/%3E%3Crect x='17' y='12' width='6' height='6' fill='%230085ba'/%3E%3Crect x='9' y='20' width='6' height='6' fill='%230085ba'/%3E%3Crect x='17' y='20' width='6' height='6' fill='%230085ba'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<header class="nav">
  <div class="wrap nav-in">
    <a href="/" class="brand"><img src="/img/logo.png" alt="Next Home Property Advisors" width="200" height="40"></a>
    <a class="btn btn-primary btn-sm" href="#tour">Book a tour</a>
  </div>
</header>
<div class="offer-bar" data-offer><strong>First month free</strong> on a 12-month lease signed by October 20. <a href="#tour">Claim it →</a></div>
{hero_html}
<main>
{main_html}
<section class="band" id="included">
  <div class="wrap">
    <h2>Every suite includes</h2>
    <p class="lede">One flat monthly bill. No meters, no parking deck, no shared bathroom down the hall.</p>
    <ul class="included">{included}</ul>
  </div>
</section>

<section class="wrap split" id="floorplan">
  <div>
    <h2>Floor plan</h2>
    <p class="lede">Six private suites in a renovated 1930 single-story building in East Town, a short walk from downtown Rock Hill. Offices 1, 2 and 6 are available now.</p>
    <dl class="facts">
      <div><dt>Address</dt><dd>417 E Black St, Rock Hill, SC 29730</dd></div>
      <div><dt>Building</dt><dd>1,500 SF, one story, 6 private suites</dd></div>
      <div><dt>Lease</dt><dd>Up to 12 months · utilities &amp; Wi-Fi included</dd></div>
      <div><dt>Parking</dt><dd>14 dedicated spaces</dd></div>
      <div><dt>Deposit</dt><dd>One month's rent · $0 application fee</dd></div>
    </dl>
    <a class="map-link" href="https://maps.google.com/?q=417+E+Black+St,+Rock+Hill,+SC+29730" target="_blank" rel="noopener">{ic('pin')} Open in Google Maps</a>
  </div>
  <a class="fp" href="/img/floorplan.jpg" target="_blank" rel="noopener"><img src="/img/floorplan.jpg" alt="Floor plan showing Offices 1 through 6, conference room and bathrooms" loading="lazy" width="1100" height="1473"></a>
</section>

<section class="tour" id="tour">
  <div class="wrap tour-in">
    <div class="tour-copy">
      <h2>Book a tour</h2>
      <p>Tell us which office and when you'd like to see it. We reply within 15 minutes during business hours, usually by text.</p>
      <ul class="offer-list" data-offer>
        <li>First month free on a 12-month lease signed by Oct 20</li>
        <li>Move in within 7 days of signing</li>
        <li>$0 application fee, decision within 24 hours</li>
      </ul>
      <div class="contact-btns">
        <a class="btn btn-light" data-tel>{ic('phone')} Call</a>
        <a class="btn btn-light" data-sms>{ic('msg')} Text</a>
      </div>
    </div>
    <form class="form" id="tour-form" novalidate>
      <label>Name<input name="name" autocomplete="name" required></label>
      <div class="row">
        <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
        <label>Email<input name="email" type="email" autocomplete="email"></label>
      </div>
      <label>Which office?
        <select name="suite"><option>Not sure yet, show me all three</option>{opts}</select>
      </label>
      <div class="row">
        <label>Business / profession<input name="business" placeholder="e.g. counselor, CPA"></label>
        <label>Ideal move-in<input name="move_in" placeholder="e.g. Nov 1"></label>
      </div>
      <label>Anything else?<textarea name="notes" rows="3"></textarea></label>
      <input type="text" name="company_site" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-primary btn-block" type="submit">Request a tour</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
</main>
<footer class="foot">
  <div class="wrap">
    <img src="/img/logo.png" alt="Next Home Property Advisors" width="180" height="36" class="foot-logo">
    <p>Listed by Next Home Property Advisors · Myisha Hoyle, Broker-in-Charge · SC Lic. #141872 · NC Lic. #344276</p>
    <p class="fine">Rents, availability and offer terms subject to change. First-month-free offer applies to 12-month leases signed by October 20, 2026.</p>
  </div>
</footer>
<div class="sticky-cta"><a class="btn btn-light" data-tel>{ic('phone')} Call</a><a class="btn btn-light" data-sms>{ic('msg')} Text</a><a class="btn btn-primary" href="#tour">Tour</a></div>
<script src="/config.js"></script>
<script src="/app.js"></script>
</body>
</html>'''

# ---------- home ----------
home_hero = f'''<section class="hero" style="--hero:url('/img/exterior.jpg')">
  <div class="wrap hero-in">
    <p class="eyebrow">417 E Black St · Rock Hill, SC</p>
    <h1>3 private offices with your own bathroom &amp; entrance</h1>
    <p class="hero-sub">From <strong>$595/mo all-in</strong>. Utilities, Wi-Fi and parking included. Near downtown Rock Hill.</p>
    <div class="hero-btns"><a class="btn btn-primary" href="#suites">See the offices</a><a class="btn btn-light" href="#tour">Book a tour</a></div>
  </div>
</section>'''
home_main = f'''<section class="wrap" id="suites">
  <h2>Available now</h2>
  <p class="lede">Each suite is fully private: its own door to the outside, its own bathroom and its own thermostat. Below the price of downtown executive suites, with free parking.</p>
  <div class="suites">{''.join(suite_card(k, s) for k, s in SUITES.items())}</div>
</section>'''
open(OUT + 'index.html', 'w').write(page('index',
    '3 Private Offices with Own Bathroom & Entrance · From $595/mo · Rock Hill',
    'Private office suites at 417 E Black St, Rock Hill SC. Own entrance and bathroom, utilities, Wi-Fi and parking included. From $595/mo. First month free if signed by Oct 20.',
    'og-home.jpg', home_hero, home_main))

# ---------- per-suite ----------
for k, s in SUITES.items():
    others = ''.join(suite_card(ok, os_) for ok, os_ in SUITES.items() if ok != k)
    feats = ''.join(f'<li>{f}</li>' for f in s['feats'])
    hero = f'''<section class="suite-hero wrap">
  <a href="/" class="back">← All available offices</a>
  <div class="sh-grid">
    <img src="/img/{k}.jpg" alt="{s['n']} interior" width="640" height="480">
    <div>
      <p class="eyebrow dark">417 E Black St · Rock Hill, SC</p>
      <h1>{s['n']} <span class="sf">{s['sf']} SF</span></h1>
      <p class="price big">${s['rent']}<span>/mo all-in</span></p>
      <p>{s['blurb']}</p>
      <ul class="feats">{feats}<li>Own entrance, bathroom and thermostat</li><li>Utilities, Wi-Fi and parking included</li></ul>
      <div class="hero-btns"><a class="btn btn-primary" href="#tour">Book a tour of {s['n']}</a><button class="btn btn-ghost" data-share>Share</button></div>
    </div>
  </div>
</section>'''
    main = f'''<section class="wrap"><h2>Also available</h2><div class="suites two">{others}</div></section>'''
    open(OUT + k + '.html', 'w').write(page(k,
        f"{s['n']} · {s['sf']} SF Private Office · ${s['rent']}/mo All-In · Rock Hill",
        f"{s['blurb']} Own entrance and bathroom, utilities, Wi-Fi and parking included. First month free if signed by Oct 20.",
        f'og-{k}.jpg', hero, main, preselect=s['n']))
print('ok')
