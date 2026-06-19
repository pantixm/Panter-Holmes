#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐾 PANTHER HOLMES OSINT v5.0 — TERMUX EDITION
Tek kullanıcı adı → Telefon + Instagram + Facebook + Email + 50+ Site + Dijital Ayak İzi
Termux + Colorama + Full CLI
"""

import os
import sys
import re
import json
import time
import hashlib
import random
import socket
import dns.resolver
from datetime import datetime
from urllib.parse import quote_plus

# Renklendirme
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# HTTP istekleri
try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

# DNS
try:
    import dns.resolver
except ImportError:
    os.system("pip install dnspython")
    import dns.resolver

# ====================== RENK SABİTLERİ ======================
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
BR = Fore.LIGHTRED_EX
BG = Fore.LIGHTGREEN_EX
BY = Fore.LIGHTYELLOW_EX
BB = Fore.LIGHTBLUE_EX
BM = Fore.LIGHTMAGENTA_EX
BC = Fore.LIGHTCYAN_EX
ST = Style.BRIGHT
RS = Style.RESET_ALL

# ====================== BAŞLIK ======================
BASLIK = f"""
{BR}{ST}╔══════════════════════════════════════════════════════╗
║     {BC}🐾 PANTHER HOLMES OSINT v5.0{BR}                    ║
║     {BY}Telegram Username → HER ŞEY{BR}                      ║
║     {BG}Termux Edition | CLI Mode{BR}                         ║
╚══════════════════════════════════════════════════════╝{RS}

{BM}{ST}🔍 Bir kullanıcı adından:{RS}
{BC}📡 Telegram | 📸 Instagram | 📘 Facebook | 📧 Email{RS}
{BC}📞 Telefon | 🌐 50+ Site | 🐙 GitHub | 🔍 Dijital Ayak İzi{RS}
"""

MENU = f"""
{BR}{ST}{'═'*50}{RS}
{BM}{ST}          🐾 PANTHER HOLMES — ANA MENÜ{RS}
{BR}{ST}{'═'*50}{RS}

{BC}{ST}[1]{RS} {BG}🕵️ Username'den HER ŞEYİ Bul{RS}
{BC}{ST}[2]{RS} {BG}📞 Telefon'dan HER ŞEYİ Bul{RS}
{BC}{ST}[3]{RS} {BG}📧 Email'den HER ŞEYİ Bul{RS}
{BC}{ST}[4]{RS} {BG}🌐 Domain / IP Analizi{RS}
{BC}{ST}[5]{RS} {BG}📊 Toplu Rapor (Tümü){RS}
{BC}{ST}[0]{RS} {BR}🚪 Çıkış{RS}

{BR}{ST}{'═'*50}{RS}
"""

# ====================== HEADER ======================
AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) Mobile/15E148",
]
def h(): return {"User-Agent": random.choice(AGENTS), "Accept-Language": "en-US,en;q=0.5,tr;q=0.3"}

# ====================== 1. TELEGRAM BİLGİSİ ======================
def telegram_kullanici_bilgi(username):
    print(f"    {BC}📡{RS} Telegram profili alınıyor...")
    sonuc = {"username": username, "profil": None, "foto": None, "bio": None, "ad": None, "kanal": False}
    
    url = f"https://t.me/{username}"
    try:
        r = requests.get(url, headers=h(), timeout=10)
        if r.status_code == 200:
            sonuc["profil"] = url
            bio_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', r.text)
            if bio_m: sonuc["bio"] = bio_m.group(1)
            name_m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', r.text)
            if name_m: sonuc["ad"] = name_m.group(1)
            img_m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', r.text)
            if img_m: sonuc["foto"] = img_m.group(1)
    except: pass
    
    try:
        r2 = requests.get(f"https://t.me/s/{username}", headers=h(), timeout=10)
        sonuc["kanal"] = r2.status_code == 200
    except: pass
    
    return sonuc

# ====================== 2. INSTAGRAM ======================
def instagram_bilgi(username):
    print(f"    {BC}📸{RS} Instagram taranıyor...")
    sonuc = {"var": False, "url": f"https://www.instagram.com/{username}/", "isim": None, "bio": None,
             "takipci": None, "takip": None, "post": None, "foto": None,
             "email": None, "telefon": None, "dogrulanmis": False, "ozel": False}
    
    try:
        r = requests.get(sonuc["url"], headers=h(), timeout=10)
        if r.status_code == 200:
            sonuc["var"] = True
            shared_m = re.search(r'window\._sharedData\s*=\s*({.*?});', r.text, re.DOTALL)
            if shared_m:
                try:
                    data = json.loads(shared_m.group(1))
                    u = data.get("entry_data", {}).get("ProfilePage", [{}])[0].get("graphql", {}).get("user", {})
                    if u:
                        sonuc["isim"] = u.get("full_name")
                        sonuc["bio"] = u.get("biography")
                        sonuc["takipci"] = u.get("edge_followed_by", {}).get("count")
                        sonuc["takip"] = u.get("edge_follow", {}).get("count")
                        sonuc["post"] = u.get("edge_owner_to_timeline_media", {}).get("count")
                        sonuc["foto"] = u.get("profile_pic_url_hd")
                        sonuc["dogrulanmis"] = u.get("is_verified", False)
                        sonuc["ozel"] = u.get("is_private", False)
                        if u.get("biography"):
                            bio_txt = u["biography"]
                            em = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', bio_txt)
                            if em: sonuc["email"] = em[0]
                            tm = re.findall(r'(\+?\d{10,15})', bio_txt)
                            if tm: sonuc["telefon"] = tm[0]
                except: pass
    except: pass
    
    return sonuc

# ====================== 3. FACEBOOK ======================
def facebook_bilgi(username):
    print(f"    {BC}📘{RS} Facebook taranıyor...")
    sonuc = {"var": False, "url": f"https://www.facebook.com/{username}", "isim": None}
    try:
        r = requests.get(sonuc["url"], headers=h(), timeout=10, allow_redirects=True)
        if r.status_code == 200 and "facebook.com" in r.url:
            sonuc["var"] = True
            nm = re.search(r'<title>(.*?)</title>', r.text)
            if nm: sonuc["isim"] = nm.group(1).replace(" | Facebook", "").strip()
    except: pass
    return sonuc

# ====================== 4. EMAIL BUL ======================
def email_bul(username):
    print(f"    {BC}📧{RS} Email adresleri taranıyor...")
    emailler = set()
    domainler = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com", 
                 "protonmail.com", "yandex.com", "mail.ru", "live.com", "msn.com"]
    for d in domainler:
        emailler.add(f"{username}@{d}")
    
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=h(), timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("email"): emailler.add(data["email"])
    except: pass
    
    try:
        r = requests.get(f"https://api.github.com/users/{username}/events/public", headers=h(), timeout=10)
        if r.status_code == 200:
            for ev in r.json():
                if ev.get("type") == "PushEvent":
                    for c in ev.get("payload", {}).get("commits", []):
                        if c.get("author", {}).get("email"):
                            emailler.add(c["author"]["email"])
    except: pass
    
    return list(emailler)[:20]

# ====================== 5. KAYITLI SİTELER ======================
def kayitli_siteler(username, progress=True):
    if progress:
        print(f"    {BC}🌐{RS} 50+ platform taranıyor...")
    
    siteler = {
        "Instagram":    f"https://www.instagram.com/{username}/",
        "Facebook":     f"https://www.facebook.com/{username}",
        "X (Twitter)":  f"https://x.com/{username}",
        "TikTok":       f"https://www.tiktok.com/@{username}",
        "YouTube":      f"https://www.youtube.com/@{username}",
        "Telegram":     f"https://t.me/{username}",
        "Threads":      f"https://www.threads.net/@{username}",
        "Twitch":       f"https://www.twitch.tv/{username}",
        "GitHub":       f"https://github.com/{username}",
        "Reddit":       f"https://www.reddit.com/user/{username}",
        "LinkedIn":     f"https://www.linkedin.com/in/{username}",
        "Pinterest":    f"https://www.pinterest.com/{username}/",
        "Snapchat":     f"https://www.snapchat.com/add/{username}",
        "Medium":       f"https://medium.com/@{username}",
        "SoundCloud":   f"https://soundcloud.com/{username}",
        "VK":           f"https://vk.com/{username}",
        "Steam":        f"https://steamcommunity.com/id/{username}",
        "Chess.com":    f"https://www.chess.com/member/{username}",
        "Spotify":      f"https://open.spotify.com/user/{username}",
        "Patreon":      f"https://www.patreon.com/{username}",
        "Keybase":      f"https://keybase.io/{username}",
        "Mastodon":     f"https://mastodon.social/@{username}",
        "DEV.to":       f"https://dev.to/{username}",
        "Dribbble":     f"https://dribbble.com/{username}",
        "Flickr":       f"https://www.flickr.com/people/{username}/",
        "Replit":       f"https://replit.com/@{username}",
        "Behance":      f"https://www.behance.net/{username}",
        "CodePen":      f"https://codepen.io/{username}",
        "BitBucket":    f"https://bitbucket.org/{username}/",
        "GitLab":       f"https://gitlab.com/{username}",
        "About.me":     f"https://about.me/{username}",
        "Imgur":        f"https://imgur.com/user/{username}",
        "WordPress":    f"https://{username}.wordpress.com",
        "Gravatar":     f"https://gravatar.com/{username}",
        "Last.fm":      f"https://www.last.fm/user/{username}",
        "MixCloud":     f"https://www.mixcloud.com/{username}/",
        "MyAnimeList":  f"https://myanimelist.net/profile/{username}",
        "Fiverr":       f"https://www.fiverr.com/{username}",
        "AngelList":    f"https://angel.co/u/{username}",
        "ProductHunt":  f"https://www.producthunt.com/@{username}",
        "HackerNews":   f"https://news.ycombinator.com/user?id={username}",
        "Roblox":       f"https://www.roblox.com/user.aspx?username={username}",
        "Wattpad":      f"https://www.wattpad.com/user/{username}",
        "Myspace":      f"https://myspace.com/{username}",
        "Vimeo":        f"https://vimeo.com/{username}",
        "VSCO":         f"https://vsco.co/{username}",
        "Canva":        f"https://www.canva.com/{username}",
    }
    
    bulunan = {}
    toplam = len(siteler)
    
    for idx, (site, url) in enumerate(siteler.items(), 1):
        try:
            r = requests.get(url, headers=h(), timeout=8, allow_redirects=True)
            if r.status_code == 200 and (username.lower() in r.url.lower() or len(r.text) > 500):
                bulunan[site] = url
        except: pass
        # Progress
        if progress and idx % 10 == 0:
            print(f"\r    {BC}🌐{RS} Taranıyor: {idx}/{toplam} | Bulunan: {len(bulunan)}", end="", flush=True)
        time.sleep(0.15)
    
    if progress:
        print(f"\r    {BC}🌐{RS} Tarama tamam: {toplam}/{toplam} | Bulunan: {len(bulunan)}   ")
    
    return bulunan

# ====================== 6. TELEFON BUL ======================
def telefon_ara(username):
    print(f"    {BC}📞{RS} Telefon numarası aranıyor...")
    telefonlar = set()
    
    # Instagram bio
    insta = instagram_bilgi(username)
    if insta.get("telefon"): telefonlar.add(insta["telefon"])
    
    # Google dork
    try:
        r = requests.get(f"https://www.google.com/search?q=%22{username}%22+%22telefon%22+OR+%22phone%22+OR+%2205", headers=h(), timeout=10)
        for t in re.findall(r'(\+?\d{10,15})', r.text):
            if len(t) >= 10 and len(t) <= 15: telefonlar.add(t)
    except: pass
    
    return list(telefonlar)[:10]

# ====================== 7. GITHUB BİLGİ ======================
def github_bilgi(username):
    print(f"    {BC}🐙{RS} GitHub profili alınıyor...")
    sonuc = {}
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=h(), timeout=10)
        if r.status_code == 200:
            d = r.json()
            sonuc["ad"] = d.get("name")
            sonuc["bio"] = d.get("bio")
            sonuc["konum"] = d.get("location")
            sonuc["sirket"] = d.get("company")
            sonuc["web"] = d.get("blog")
            sonuc["repo"] = d.get("public_repos")
            sonuc["takipci"] = d.get("followers")
            sonuc["takip"] = d.get("following")
            sonuc["tarih"] = d.get("created_at")
    except: pass
    return sonuc

# ====================== 8. GOOGLE DORK ======================
def google_dork(username):
    dorks = [
        f'"%40{username}" site:instagram.com "telefon" OR "phone" OR "whatsapp" OR "05"',
        f'"@{username}" site:tiktok.com',
        f'"{username}" "email" OR "@gmail" OR "@hotmail" OR "@yahoo"',
        f'"{username}" "05" OR "+90" OR "telefon"',
        f'intitle:"{username}" intext:"@gmail.com" OR "@hotmail.com"',
        f'site:github.com "{username}" password OR token OR api_key OR secret',
        f'site:pastebin.com "{username}"',
        f'"{username}" filetype:pdf OR filetype:docx OR filetype:xlsx',
        f'"{username}" site:linkedin.com/in',
        f'"{username}" "hack" OR "breach" OR "leak" OR "dump"',
    ]
    return dorks

# ====================== ANA OSINT FONKSİYONU ======================
def herseyi_bul(username):
    """Kullanıcı adından tüm bilgileri bul"""
    
    os.system("clear")
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"{BM}{ST}     🐾 PANTHER HOLMES — TAM İSTİHBARAT RAPORU{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"    {BC}🎯{RS} Hedef: {BY}{ST}@{username}{RS}")
    print(f"    {BC}🕐{RS} Zaman: {BY}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    
    # === AŞAMA 1: TELEGRAM ===
    print(f"\n{BM}{ST}📡 1. TELEGRAM BİLGİSİ{RS}")
    print(f"{BR}{'─'*60}{RS}")
    tg = telegram_kullanici_bilgi(username)
    if tg["profil"]:
        print(f"    {BG}✅{RS} Profil: {BC}https://t.me/{username}{RS}")
        if tg["ad"]: print(f"    {BC}👤{RS} İsim: {BY}{tg['ad']}{RS}")
        if tg["bio"]: 
            bio_short = tg['bio'][:120] + "..." if len(tg['bio']) > 120 else tg['bio']
            print(f"    {BC}📝{RS} Bio: {Y}{bio_short}{RS}")
        if tg["foto"]: print(f"    {BC}🖼️{RS} Fotoğraf: {C}{tg['foto']}{RS}")
        print(f"    {BC}📢{RS} Kanal: {BG}✅ Var{RS}" if tg["kanal"] else f"    {BC}📢{RS} Kanal: {BR}❌ Yok{RS}")
    else:
        print(f"    {BR}❌ Telegram profili bulunamadı.{RS}")
    
    # === AŞAMA 2: INSTAGRAM ===
    print(f"\n{BM}{ST}📸 2. INSTAGRAM BİLGİSİ{RS}")
    print(f"{BR}{'─'*60}{RS}")
    insta = instagram_bilgi(username)
    if insta["var"]:
        print(f"    {BG}✅{RS} Profil: {BC}https://www.instagram.com/{username}/{RS}")
        if insta["isim"]: print(f"    {BC}👤{RS} İsim: {BY}{insta['isim']}{RS}")
        if insta["bio"]: print(f"    {BC}📝{RS} Bio: {Y}{insta['bio'][:150]}{RS}")
        if insta["takipci"] is not None: print(f"    {BC}👥{RS} Takipçi: {BY}{insta['takipci']:,}{RS}")
        if insta["takip"] is not None: print(f"    {BC}👣{RS} Takip: {BY}{insta['takip']:,}{RS}")
        if insta["post"] is not None: print(f"    {BC}📸{RS} Post: {BY}{insta['post']:,}{RS}")
        if insta["dogrulanmis"]: print(f"    {BG}✅{RS} Mavi Tik: {BG}{ST}EVET{RS}")
        if insta["ozel"]: print(f"    {BR}🔒{RS} Gizli Hesap: {BR}{ST}EVET{RS}")
        if insta["email"]: print(f"    {BG}⭐{RS} {BR}{ST}Email (Bio'da): {BY}{insta['email']}{RS}")
        if insta["telefon"]: print(f"    {BG}⭐{RS} {BR}{ST}Telefon (Bio'da): {BY}{insta['telefon']}{RS}")
        if insta["foto"]: print(f"    {BC}🖼️{RS} Profil: {C}{insta['foto']}{RS}")
    else:
        print(f"    {BR}❌ Instagram hesabı bulunamadı.{RS}")
    
    # === AŞAMA 3: FACEBOOK ===
    print(f"\n{BM}{ST}📘 3. FACEBOOK BİLGİSİ{RS}")
    print(f"{BR}{'─'*60}{RS}")
    fb = facebook_bilgi(username)
    if fb["var"]:
        print(f"    {BG}✅{RS} Profil: {BC}https://www.facebook.com/{username}{RS}")
        if fb["isim"]: print(f"    {BC}👤{RS} İsim: {BY}{fb['isim']}{RS}")
    else:
        print(f"    {BR}❌ Facebook hesabı bulunamadı.{RS}")
        print(f"    {BC}🔍{RS} Alternatif: {C}https://www.facebook.com/search/top/?q={username}{RS}")
    
    # === AŞAMA 4: EMAIL ===
    print(f"\n{BM}{ST}📧 4. BULUNAN EMAİL ADRESLERİ{RS}")
    print(f"{BR}{'─'*60}{RS}")
    emailler = email_bul(username)
    if emailler:
        print(f"    {BG}✅{RS} {BY}{len(emailler)}{RS} aday email bulundu:")
        for e in emailler[:8]:
            print(f"    {BC}•{RS} {Y}{e}{RS}")
        if len(emailler) > 8:
            print(f"    {BC}•{RS} ... ve {len(emailler)-8} tane daha")
        print(f"    {BC}🔍{RS} Kontrol: {C}https://haveibeenpwned.com/{RS}")
    else:
        print(f"    {BR}❌ Email bulunamadı.{RS}")
    
    # === AŞAMA 5: KAYITLI SİTELER ===
    print(f"\n{BM}{ST}🌐 5. KAYITLI SİTELER / PLATFORMLAR{RS}")
    print(f"{BR}{'─'*60}{RS}")
    siteler = kayitli_siteler(username)
    if siteler:
        print(f"    {BG}✅{RS} {BY}{len(siteler)}{RS} platformda bulundu:")
        for site, url in sorted(siteler.items()):
            print(f"    {BC}•{RS} {BG}{site:15}{RS} → {C}{url}{RS}")
        print(f"\n    {BC}📊{RS} İstatistik:")
        print(f"    {BC}  •{RS} Taranan: {BY}50{RS} platform")
        print(f"    {BC}  •{RS} Bulunan: {BG}{len(siteler)}{RS} profil")
        print(f"    {BC}  •{RS} Başarı: {BG}%{int((len(siteler)/50)*100)}{RS}")
    else:
        print(f"    {BR}❌ Hiçbir platformda bulunamadı.{RS}")
    
    # === AŞAMA 6: TELEFON ===
    print(f"\n{BM}{ST}📞 6. BULUNAN TELEFON NUMARALARI{RS}")
    print(f"{BR}{'─'*60}{RS}")
    telefonlar = telefon_ara(username)
    if telefonlar:
        print(f"    {BG}✅{RS} {BY}{len(telefonlar)}{RS} aday telefon:")
        for t in telefonlar:
            t_clean = t.replace("+", "").replace(" ", "").replace("-", "")
            print(f"    {BC}•{RS} {BR}{t}{RS}")
            print(f"      {BC}📱{RS} WhatsApp: {C}https://wa.me/{t_clean}{RS}")
            print(f"      {BC}✈️{RS} Telegram: {C}https://t.me/{t_clean}{RS}")
            print(f"      {BC}🔐{RS} Signal:   {C}https://signal.me/#p/{t_clean}{RS}")
    else:
        print(f"    {BR}❌ Telefon numarası bulunamadı.{RS}")
    
    # === AŞAMA 7: GITHUB ===
    print(f"\n{BM}{ST}🐙 7. GITHUB BİLGİSİ{RS}")
    print(f"{BR}{'─'*60}{RS}")
    gh = github_bilgi(username)
    if gh:
        print(f"    {BG}✅{RS} Profil: {BC}https://github.com/{username}{RS}")
        if gh.get("ad"): print(f"    {BC}👤{RS} İsim: {BY}{gh['ad']}{RS}")
        if gh.get("bio"): print(f"    {BC}📝{RS} Bio: {Y}{gh['bio'][:100]}{RS}")
        if gh.get("konum"): print(f"    {BC}📍{RS} Konum: {BY}{gh['konum']}{RS}")
        if gh.get("sirket"): print(f"    {BC}🏢{RS} Şirket: {BY}{gh['sirket']}{RS}")
        if gh.get("web"): print(f"    {BC}🌐{RS} Web: {C}{gh['web']}{RS}")
        if gh.get("repo"): print(f"    {BC}📦{RS} Repo: {BY}{gh['repo']}{RS}")
        if gh.get("takipci"): print(f"    {BC}👥{RS} Takipçi: {BY}{gh['takipci']:,}{RS}")
    else:
        print(f"    {BR}❌ GitHub profili bulunamadı.{RS}")
    
    # === AŞAMA 8: GOOGLE DORK ===
    print(f"\n{BM}{ST}🔍 8. ÖZEL GOOGLE DORKLAR{RS}")
    print(f"{BR}{'─'*60}{RS}")
    dorks = google_dork(username)
    for i, dork in enumerate(dorks, 1):
        print(f"    {BC}{i}.{RS} {Y}{dork[:80]}...{RS}")
        encoded = quote_plus(dork)
        print(f"       {C}🔗 https://www.google.com/search?q={encoded[:70]}...{RS}")
    
    # === AŞAMA 9: DİĞER ===
    print(f"\n{BM}{ST}🔗 9. EK BAĞLANTILAR{RS}")
    print(f"{BR}{'─'*60}{RS}")
    email_hash = hashlib.md5(f"{username}@gmail.com".lower().encode()).hexdigest()
    print(f"    {BC}📌{RS} Gravatar: {C}https://www.gravatar.com/{email_hash}{RS}")
    print(f"    {BC}📌{RS} Dehashed: {C}https://dehashed.com/search?query={username}{RS}")
    print(f"    {BC}📌{RS} HIBP:     {C}https://haveibeenpwned.com/account/{username}%40gmail.com{RS}")
    print(f"    {BC}📌{RS} Instagram Checker: {C}https://www.instagram.com/{username}/{RS}")
    
    # === RAPOR SONU ===
    print(f"\n{BR}{ST}{'═'*60}{RS}")
    print(f"{BG}{ST}     ✅ RAPOR TAMAMLANDI — {len(siteler)} site, {len(emailler)} email, {len(telefonlar)} telefon{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    
    # Dosyaya kaydet
    kaydet(username, {
        "telegram": tg,
        "instagram": insta,
        "facebook": fb,
        "emailler": emailler,
        "siteler": siteler,
        "telefonlar": telefonlar,
        "github": gh,
        "zaman": datetime.now().isoformat()
    })

# ====================== DOSYAYA KAYDET ======================
def kaydet(username, data):
    try:
        # JSON kaydet
        dosya_adi = f"panther_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n    {BG}💾{RS} Rapor kaydedildi: {C}{dosya_adi}{RS}")
        
        # TXT özet
        txt_adi = f"panther_{username}_ozet.txt"
        with open(txt_adi, "w", encoding="utf-8") as f:
            f.write(f"PANTHER HOLMES OSINT RAPORU - @{username}\n")
            f.write(f"Tarih: {data['zaman']}\n")
            f.write(f"{'='*60}\n")
            f.write(f"\nSiteler ({len(data['siteler'])}):\n")
            for site, url in sorted(data['siteler'].items()):
                f.write(f"  {site}: {url}\n")
            f.write(f"\nEmailler ({len(data['emailler'])}):\n")
            for e in data['emailler']:
                f.write(f"  {e}\n")
            f.write(f"\nTelefonlar ({len(data['telefonlar'])}):\n")
            for t in data['telefonlar']:
                f.write(f"  {t}\n")
        print(f"    {BG}📄{RS} Özet kaydedildi: {C}{txt_adi}{RS}")
    except Exception as e:
        print(f"    {BR}❌{RS} Kayıt hatası: {e}")

# ====================== TELEFON OSINT ======================
def telefon_osint(telefon):
    os.system("clear")
    numara = re.sub(r'[\s\-\(\)]', '', telefon)
    if not numara.startswith('+'):
        if numara.startswith('90'): numara = '+' + numara
        elif numara.startswith('0'): numara = '+90' + numara[1:]
        else: numara = '+90' + numara
    
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"{BM}{ST}     📞 TELEFON TAM RAPORU{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"    {BC}🎯{RS} Orijinal: {BY}{telefon}{RS}")
    print(f"    {BC}🔢{RS} Normalize: {BY}{numara}{RS}")
    print(f"{BR}{ST}{'─'*60}{RS}")
    
    t = numara.replace('+', '').replace(' ', '')
    
    print(f"\n{BM}{ST}🔍 GOOGLE DORKLAR:{RS}")
    dorks = [
        f'https://www.google.com/search?q=%22{numara}%22',
        f'https://www.google.com/search?q=%22{numara}%22+site:instagram.com',
        f'https://www.google.com/search?q=%22{numara}%22+site:facebook.com',
        f'https://www.google.com/search?q=%22{numara}%22+site:twitter.com',
        f'https://www.google.com/search?q=%22{numara}%22+site:linkedin.com',
        f'https://www.google.com/search?q=%22{numara}%22+site:tiktok.com',
        f'https://www.google.com/search?q=%22{numara}%22+%22whatsapp%22',
    ]
    for i, d in enumerate(dorks, 1):
        print(f"    {BC}{i}.{RS} {C}{d[:90]}...{RS}")
    
    print(f"\n{BM}{ST}📱 MESSENGER:{RS}")
    print(f"    {BC}•{RS} WhatsApp: {C}https://wa.me/{t}{RS}")
    print(f"    {BC}•{RS} Telegram: {C}https://t.me/{t}{RS}")
    print(f"    {BC}•{RS} Signal:   {C}https://signal.me/#p/{t}{RS}")
    
    print(f"\n{BM}{ST}🌐 OSINT ARAÇLARI:{RS}")
    print(f"    {BC}•{RS} Truecaller: {C}https://www.truecaller.com/search/tr/{t}{RS}")
    print(f"    {BC}•{RS} Numverify:  {C}https://numverify.com/{RS}")
    print(f"    {BC}•{RS} SpyDialer:  {C}https://spydialer.com/{RS}")
    
    print(f"\n{BR}{ST}{'═'*60}{RS}")
    input(f"\n    {BY}Devam etmek için ENTER'a bas...{RS}")

# ====================== EMAIL OSINT ======================
def email_osint(email):
    os.system("clear")
    
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"{BM}{ST}     📧 EMAIL TAM RAPORU{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"    {BC}🎯{RS} Hedef: {BY}{email}{RS}")
    print(f"{BR}{ST}{'─'*60}{RS}")
    
    if '@' in email:
        local, domain = email.split('@')
        print(f"\n    {BC}📊{RS} Local: {Y}{local}{RS}")
        print(f"    {BC}📊{RS} Domain: {Y}{domain}{RS}")
        
        # MX sorgula
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            print(f"\n    {BC}📡{RS} MX Sunucuları:")
            for mx in answers[:5]:
                print(f"      {BC}•{RS} {C}{mx.exchange}{RS}")
        except:
            print(f"\n    {BR}❌{RS} MX: Sorgulanamadı")
    
    print(f"\n{BM}{ST}🔍 ARAMA LİNKLERİ:{RS}")
    encoded = email.replace('@', '%40')
    print(f"    {BC}•{RS} HIBP:     {C}https://haveibeenpwned.com/account/{encoded}{RS}")
    print(f"    {BC}•{RS} Dehashed: {C}https://dehashed.com/search?query={encoded}{RS}")
    print(f"    {BC}•{RS} Hunter:   {C}https://hunter.io/email-verifier/{email}{RS}")
    print(f"    {BC}•{RS} EmailRep: {C}https://emailrep.io/{email}{RS}")
    print(f"    {BC}•{RS} Google:   {C}https://www.google.com/search?q=%22{email}%22{RS}")
    print(f"    {BC}•{RS} GitHub:   {C}https://github.com/search?q=%22{email}%22&type=code{RS}")
    print(f"    {BC}•{RS} Pastebin: {C}https://pastebin.com/search?q={email}{RS}")
    
    print(f"\n{BM}{ST}🛡️ CLI ARAÇLARI:{RS}")
    print(f"    {BC}•{RS} {Y}holehe {email}{RS}")
    print(f"    {BC}•{RS} {Y}theHarvester -d {domain if '@' in email else email} -b all{RS}")
    print(f"    {BC}•{RS} {Y}social-analyzer --username {local if '@' in email else email}{RS}")
    
    print(f"\n{BR}{ST}{'═'*60}{RS}")
    input(f"\n    {BY}Devam etmek için ENTER'a bas...{RS}")

# ====================== DOMAIN/IP ANALİZİ ======================
def domain_analiz(hedef):
    os.system("clear")
    
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"{BM}{ST}     🌐 DOMAIN / IP ANALİZİ{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"    {BC}🎯{RS} Hedef: {BY}{hedef}{RS}")
    print(f"{BR}{ST}{'─'*60}{RS}")
    
    # DNS çözümleme
    try:
        ip = socket.gethostbyname(hedef)
        print(f"\n    {BG}✅{RS} A Kaydı (IP): {BY}{ip}{RS}")
        
        # Ters DNS
        try:
            hostname = socket.gethostbyaddr(ip)
            print(f"    {BC}🔁{RS} Ters DNS: {C}{hostname[0]}{RS}")
        except: pass
        
        # WHOIS (port 43)
        print(f"\n    {BC}📋{RS} WHOIS için: {Y}whois {hedef}{RS}")
        
        # Alt alan keşfi
        print(f"\n    {BC}🔎{RS} Alt Alan Keşfi:")
        print(f"      {Y}sublist3r -d {hedef}{RS}")
        print(f"      {Y}ffuf -w subdomains.txt -u https://{hedef} -H \"Host: FUZZ.{hedef}\"{RS}")
        
        # Teknoloji
        print(f"\n    {BC}🛠️{RS} Teknoloji Keşfi:")
        print(f"      {Y}whatweb {hedef}{RS}")
        print(f"      {Y}wappalyzer (tarayıcı eklentisi){RS}")
        
    except socket.gaierror:
        print(f"\n    {BR}❌{RS} DNS çözümlemesi başarısız!")
    
    print(f"\n{BR}{ST}{'═'*60}{RS}")
    input(f"\n    {BY}Devam etmek için ENTER'a bas...{RS}")

# ====================== TOPLU RAPOR ======================
def toplu_rapor():
    os.system("clear")
    
    print(f"{BR}{ST}{'═'*60}{RS}")
    print(f"{BM}{ST}     📊 TOPLU RAPOR — TÜM MODÜLLER{RS}")
    print(f"{BR}{ST}{'═'*60}{RS}")
    
    print(f"\n    {BC}1.{RS} {BG}Username OSINT{RS}    → Telefon + Instagram + Facebook + Email + 50 site")
    print(f"    {BC}2.{RS} {BG}Telefon OSINT{RS}    → Google dork + WhatsApp/Telegram/Signal + Truecaller")
    print(f"    {BC}3.{RS} {BG}Email OSINT{RS}      → HIBP + Dehashed + GitHub + Pastebin + MX sorgu")
    print(f"    {BC}4.{RS} {BG}Domain/IP Analizi{RS} → DNS + WHOIS + Alt alan + Teknoloji")
    print(f"    {BC}5.{RS} {BG}Tümü (Sıralı){RS}    → Yukarıdaki modüllerin hepsini çalıştır")
    
    secim = input(f"\n    {BY}Seçim [1-5]: {RS}").strip()
    
    if secim == "1":
        hedef = input(f"\n    {BY}Kullanıcı adı: {RS}").strip().replace("@", "")
        if hedef: herseyi_bul(hedef)
    elif secim == "2":
        hedef = input(f"\n    {BY}Telefon: {RS}").strip()
        if hedef: telefon_osint(hedef)
    elif secim == "3":
        hedef = input(f"\n    {BY}Email: {RS}").strip()
        if hedef: email_osint(hedef)
    elif secim == "4":
        hedef = input(f"\n    {BY}Domain/IP: {RS}").strip()
        if hedef: domain_analiz(hedef)
    elif secim == "5":
        print(f"\n    {BR}⚠️  Tüm modüller sırayla çalışacak.{RS}\n")
        hedef = input(f"    {BY}Hedef (username/telefon/email/domain): {RS}").strip()
        if hedef:
            if '@' in hedef:
                email_osint(hedef)
            elif re.match(r'^\+?\d[\d\s\-\(\)]{7,20}$', hedef):
                telefon_osint(hedef)
            elif '.' in hedef and not hedef.startswith('@'):
                domain_analiz(hedef)
            else:
                herseyi_bul(hedef.replace("@", ""))

# ====================== ANA DÖNGÜ ======================
def main():
    while True:
        os.system("clear")
        print(BASLIK)
        print(MENU)
        
        secim = input(f"    {BY}Seçiminiz [0-5]: {RS}").strip()
        
        if secim == "1":
            hedef = input(f"\n    {BY}🎯 Telegram kullanıcı adı: {RS}").strip().replace("@", "").replace(" ", "")
            if hedef and len(hedef) >= 2:
                herseyi_bul(hedef)
            else:
                print(f"\n    {BR}❌ Geçersiz kullanıcı adı!{RS}")
                time.sleep(2)
        
        elif secim == "2":
            hedef = input(f"\n    {BY}📞 Telefon numarası: {RS}").strip()
            if hedef:
                telefon_osint(hedef)
        
        elif secim == "3":
            hedef = input(f"\n    {BY}📧 Email adresi: {RS}").strip().lower()
            if hedef:
                email_osint(hedef)
        
        elif secim == "4":
            hedef = input(f"\n    {BY}🌐 Domain veya IP: {RS}").strip().lower()
            if hedef:
                domain_analiz(hedef)
        
        elif secim == "5":
            toplu_rapor()
        
        elif secim == "0":
            os.system("clear")
            print(f"\n{BR}{ST}🐾 Panther Holmes OSINT kapatılıyor...{RS}")
            print(f"{BC}Görüşmek üzere Dedektif! 🕵️{RS}\n")
            sys.exit(0)
        
        else:
            print(f"\n    {BR}❌ Geçersiz seçim!{RS}")
            time.sleep(1)

# ====================== BAŞLAT ======================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("clear")
        print(f"\n{BR}🐾 Panther Holmes OSINT kapatıldı.{RS}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{BR}❌ HATA: {e}{RS}")
        time.sleep(3)
        main()

