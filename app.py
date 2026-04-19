import streamlit as st
import pandas as pd
import datetime
import base64
import os

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="HOSPITAL OS // COMMAND CENTER",
    layout="wide",
    page_icon="💻",
    initial_sidebar_state="collapsed"
)

# --- FUNKCJA DO POBRANIA LOKALNEGO LOGO (DO STOPKI HTML) ---
def get_image_as_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_b64 = get_image_as_base64("logo.png")

# --- ZAAWANSOWANY CSS (CYBERPUNK / MISSION CONTROL THEME) ---
st.markdown("""
    <style>
    /* Reset i ukrycie domyślnych elementów Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Globalne tło i czcionki */
    .stApp {
        background-color: #0b101a !important;
        color: #a0aec0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        padding-bottom: 120px !important; /* Zwiększony margines na dolną belkę */
    }
    
    /* GÓRNY PASEK (TOP BAR) */
    .top-bar {
        background-color: #060b13;
        border-bottom: 2px solid #1a2332;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: -60px;
        margin-bottom: 30px;
        font-family: monospace;
    }
    .top-bar-title {
        color: #00f0ff;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 2px;
    }
    .top-bar-alert {
        background-color: #3b0a0a;
        color: #ff4d4d;
        border: 1px solid #ff4d4d;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .top-bar-info {
        color: #4a5568;
        font-size: 14px;
        display: flex;
        gap: 20px;
    }
    .top-bar-info span { color: #00f0ff; }

    /* PANELE (KARTY) */
    .cyber-panel {
        background-color: #121824;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    .panel-header {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
    }

    /* WSKAŹNIKI (KPI BARS) */
    .kpi-row {
        margin-bottom: 18px;
    }
    .kpi-labels {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .kpi-bg {
        background-color: #1e293b;
        height: 6px;
        width: 100%;
        border-radius: 3px;
        overflow: hidden;
    }
    .kpi-fill {
        height: 100%;
        background-color: #00f0ff;
        box-shadow: 0 0 10px #00f0ff80;
    }
    .kpi-fill.critical {
        background-color: #ff4d4d;
        box-shadow: 0 0 10px #ff4d4d80;
    }

    /* DZIENNIK ZDARZEŃ */
    .log-entry {
        font-family: monospace;
        font-size: 12px;
        margin-bottom: 15px;
    }
    .log-time { color: #eab308; font-weight: bold; }
    .log-title { color: #f8fafc; font-weight: bold; margin-top: 4px; }
    .log-desc { color: #64748b; font-size: 11px; margin-top: 2px; border-left: 2px solid #334155; padding-left: 8px;}

    /* ŚRODKOWA KOLUMNA - DOKUMENTACJA ZDARZENIA */
    .doc-header {
        display: flex;
        justify-content: space-between;
        background-color: #1e222d;
        padding: 8px 15px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    .doc-tag { background-color: #7f1d1d; color: #fca5a5; padding: 2px 8px; border-radius: 2px; }
    .doc-timer { color: #eab308; font-weight: bold; font-size: 16px; }
    
    .stage-title {
        font-size: 26px;
        font-weight: 900;
        color: #f8fafc;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .stage-dot {
        height: 20px;
        width: 20px;
        background-color: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 15px #ef4444;
    }

    .warning-box {
        background-color: #151a23;
        border: 1px solid #334155;
        border-left: 4px solid #00f0ff;
        padding: 20px;
        border-radius: 4px;
        color: #e2e8f0;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 30px;
    }

    /* PRAWA KOLUMNA - STATUS */
    .status-box {
        text-align: center;
        padding: 40px 20px;
        background-color: #121824;
        border: 1px solid #1e293b;
        border-radius: 6px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .status-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        font-size: 24px;
    }
    .status-icon.done { background-color: #064e3b; color: #34d399; border: 2px solid #059669; }
    .status-icon.wait { background-color: #422006; color: #fbbf24; border: 2px solid #d97706; }
    .status-title { font-size: 18px; font-weight: 900; color: #f8fafc; margin-bottom: 10px; text-transform: uppercase; }
    .status-desc { font-size: 12px; color: #64748b; }
    
    /* RADIO BUTTONS (Ciemny motyw) */
    .stRadio label {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        padding: 12px 16px !important;
        border-radius: 4px !important;
        margin-bottom: 8px !important;
    }
    .stRadio div[role="radiogroup"] > label:hover {
        border-color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.05) !important;
    }

    /* CUSTOM FOOTER LOGO */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: auto;
        background-color: #0b101a;
        border-top: 2px solid #00f0ff;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: flex-end;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.8);
    }
    .footer-logo {
        width: 100%;
        height: auto;
        max-height: 120px; 
        object-fit: cover; 
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Wstrzyknięcie stopki z logo do HTML
if logo_b64:
    st.markdown(f"""
        <div class="custom-footer">
            <img src="data:image/png;base64,{logo_b64}" class="footer-logo" alt="System Logo">
        </div>
    """, unsafe_allow_html=True)

# --- STAN GRY ---
@st.cache_resource
def get_game_state():
    return {
        "round": 0, 
        "teams": {}, 
        "active_scenario": "Wariant C: Zaawansowany Atak APT (5 Rund)" 
    }

state = get_game_state()

# --- PEŁNA BAZA SCENARIUSZY (5 WARIANTÓW) ---
ALL_SCENARIOS = {
    "Wariant A: Ransomware i paraliż HIS (3 Rundy)": {
        1: {"title": "ETAP 1 - PIERWSZE SYMPTOMY", "desc": "Lekarze zgłaszają spowolnienie systemu HIS. Na komputerach pojawiły się czarne ekrany. Tłum pacjentów gęstnieje.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Natychmiastowe odcięcie SOR od sieci głównej (Blackout)": {"pat": 0, "avl": -20, "fin": -5, "comp": +10}, "Zdalny restart i analiza logów": {"pat": -10, "avl": +5, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wdrożenie procedury 'Downtime' (dokumentacja papierowa)": {"pat": +15, "avl": 0, "fin": -5, "comp": +10}, "Wstrzymanie wypisów i przyjęć planowych": {"pat": -15, "avl": 0, "fin": -15, "comp": -5}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Powiadomienie Centrum e-Zdrowia (CeZ)": {"pat": 0, "avl": 0, "fin": 0, "comp": +15}, "Brak eskalacji, oczekiwanie na diagnozę": {"pat": 0, "avl": 0, "fin": 0, "comp": -15}}}}},
        2: {"title": "ETAP 2 - ŻĄDANIE OKUPU", "desc": "Potwierdzono atak Ransomware. Żądanie 50 Bitcoinów. Brak wyników laboratoryjnych i dawek leków.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Twardy reset, odcięcie zasilania, wezwanie CERT Polska": {"pat": -10, "avl": -30, "fin": -10, "comp": +25}, "Próba odzyskiwania danych online z kopii zapasowych": {"pat": -25, "avl": -10, "fin": -20, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Przekierowanie karetek, wypisy stabilnych pacjentów": {"pat": +20, "avl": 0, "fin": -20, "comp": +10}, "Leczenie na ślepo bazując na wywiadzie z pacjentem": {"pat": -40, "avl": 0, "fin": 0, "comp": -30}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Odmowa negocjacji, powołanie sztabu z Policją": {"pat": 0, "avl": 0, "fin": +10, "comp": +20}, "Nawiązanie tajnego kontaktu z hakerami": {"pat": -10, "avl": 0, "fin": -40, "comp": -25}}}}},
        3: {"title": "ETAP 3 - KONTROLA", "desc": "Trwa powolne odtwarzanie środowiska. Przed budynkiem media, a do dyrekcji wkracza kontrola UODO.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Odbudowa sieci od podstaw z mikrosegmentacją": {"pat": +10, "avl": -15, "fin": -20, "comp": +20}, "Szybkie łatanie luk i powrót do starej architektury": {"pat": -20, "avl": +20, "fin": +10, "comp": -25}}}, "Med": {"label": "PION PR:", "options": {"Otwarty komunikat o wycieku danych, start infolinii": {"pat": +10, "avl": 0, "fin": -10, "comp": +25}, "Zasłanianie się tajemnicą śledztwa": {"pat": -10, "avl": 0, "fin": -20, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Pilne szkolenia antyphishingowe dla personelu": {"pat": +15, "avl": -5, "fin": -10, "comp": +15}, "Skupienie winy na dostawcy antywirusa": {"pat": -15, "avl": 0, "fin": 0, "comp": -20}}}}}
    },
    "Wariant B: Atak na urządzenia medyczne IoT (3 Rundy)": {
        1: {"title": "ETAP 1 - UTRATA SYNCHRONIZACJI APARATURY", "desc": "Godzina 03:00. OiTM. Kardiomonitory nagle tracą łączność z centralą. Dwie pompy infuzyjne zaczynają emitować fałszywe alarmy.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Natychmiastowe odcięcie sieci Wi-Fi dla urządzeń IoT": {"pat": +10, "avl": -20, "fin": -5, "comp": +5}, "Zdalny restart centrali (utrzymanie sieci)": {"pat": -15, "avl": +10, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Przejście na manualne monitorowanie (100% obłożenia)": {"pat": +25, "avl": 0, "fin": -10, "comp": +10}, "Zignorowanie anomalii jako usterki sprzętu": {"pat": -40, "avl": 0, "fin": 0, "comp": -30}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Skierowanie dodatkowego personelu na OiTM": {"pat": +20, "avl": 0, "fin": -15, "comp": 0}, "Czekanie na raport z porannej zmiany": {"pat": -20, "avl": 0, "fin": 0, "comp": -10}}}}},
        2: {"title": "ETAP 2 - SZANTAŻ NA ŻYCIU PACJENTÓW", "desc": "Godzina 05:00. Hakerzy grożą zdalną zmianą dawek leków w pompach infuzyjnych, jeśli nie zostanie wpłacony okup w ciągu 2 godzin.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Fizyczne wyciągnięcie kabli zasilających routery (Air-Gap)": {"pat": +20, "avl": -30, "fin": -5, "comp": +15}, "Próba lokalizacji złośliwego oprogramowania w sieci": {"pat": -30, "avl": -5, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Odłączenie pomp i podawanie leków manualnie": {"pat": +25, "avl": -10, "fin": -5, "comp": +10}, "Ewakuacja całego OiTM do innego szpitala": {"pat": -15, "avl": -20, "fin": -30, "comp": +5}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie incydentu do CSIRT GOV w trybie pilnym": {"pat": 0, "avl": 0, "fin": 0, "comp": +30}, "Zatajenie ataku i próba samodzielnej negocjacji": {"pat": -10, "avl": 0, "fin": -30, "comp": -40}}}}},
        3: {"title": "ETAP 3 - DOCHODZENIE PO INCYDENCIE", "desc": "Dzień następny. Sieć zabezpieczona. Wykryto luki w oprogramowaniu starych pomp. NFZ grozi wstrzymaniem finansowania.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wydzielenie hermetycznej sieci VLAN dla IoMT": {"pat": +15, "avl": +10, "fin": -15, "comp": +20}, "Podłączenie sprzętu do ogólnej sieci po zmianie haseł": {"pat": -25, "avl": +20, "fin": +5, "comp": -30}}}, "Med": {"label": "PION PR:", "options": {"Zawieszenie ostrego dyżuru i szczera komunikacja": {"pat": +10, "avl": -15, "fin": -15, "comp": +10}, "Komunikowanie usterek technicznych, kontynuacja przyjęć": {"pat": -15, "avl": +10, "fin": +10, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Rozpoczęcie programu wymiany sprzętu medycznego": {"pat": +25, "avl": +10, "fin": -40, "comp": +20}, "Pozwanie producenta pomp o wadliwe oprogramowanie": {"pat": -5, "avl": 0, "fin": +15, "comp": 0}}}}}
    },
    "Wariant C: Zaawansowany Atak APT (5 Rund)": {
         1: {"title": "ETAP 1 - NIEWINNE ANOMALIA CZY ZWIAD?", "desc": "Piątek, 09:00. Skargi lekarzy na powolne ładowanie zdjęć PACS. System pocztowy odrzuca hasła. Wykryto dziwny ruch wychodzący z serwera LIS.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Izolacja serwera LIS i reset haseł w administracji": {"pat": 0, "avl": -10, "fin": -5, "comp": +10}, "Tryb głębokiego monitorowania, praca bez przerw": {"pat": -5, "avl": +5, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Ręczne opisywanie pilnych zdjęć RTG": {"pat": +10, "avl": 0, "fin": -5, "comp": 0}, "Oczekiwanie na stabilizację PACS": {"pat": -10, "avl": 0, "fin": 0, "comp": 0}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zwołanie wstępnego, niejawnego sztabu kryzysowego": {"pat": +5, "avl": 0, "fin": -5, "comp": +5}, "Uznanie za awarię IT, brak działań zarządczych": {"pat": -10, "avl": 0, "fin": +5, "comp": -5}}}}},
         2: {"title": "ETAP 2 - UDERZENIE I LATERAL MOVEMENT", "desc": "Piątek, 21:00. Czarne ekrany i żądanie 2 mln zł okupu. Hakerzy przejęli system BMS. Klimatyzacja na blokach operacyjnych wariuje.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Odcięcie głównego zasilania serwerowni i sieci (Blackout)": {"pat": -10, "avl": -40, "fin": -15, "comp": +20}, "Próba odzyskania kontroli nad BMS bez wyłączania sieci": {"pat": -30, "avl": -10, "fin": -10, "comp": -15}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Ewakuacja bloków operacyjnych, wentylacja ręczna": {"pat": +25, "avl": 0, "fin": -10, "comp": +10}, "Kontynuowanie operacji w niestabilnym środowisku": {"pat": -40, "avl": 0, "fin": -20, "comp": -30}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie 'Zdarzenia Masowego', przekierowanie karetek": {"pat": +20, "avl": 0, "fin": -25, "comp": +20}, "Zakaz informowania mediów i wojewody": {"pat": -20, "avl": 0, "fin": +10, "comp": -35}}}}},
         3: {"title": "ETAP 3 - SZANTAŻ MEDIALNY", "desc": "Sobota, 10:00. Publikacja fragmentu dokumentacji pacjenta VIP na Twitterze. Przed szpitalem wozy transmisyjne i zaniepokojone rodziny.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wynajęcie firmy Incident Response (wysokie koszty)": {"pat": +10, "avl": +15, "fin": -30, "comp": +20}, "Odtwarzanie siłami lokalnych informatyków": {"pat": -10, "avl": -10, "fin": +15, "comp": -10}}}, "Med": {"label": "PION PR:", "options": {"Wysłanie personelu na rozmowy z rodzinami": {"pat": +15, "avl": 0, "fin": -5, "comp": +10}, "Odmawianie dostępu 'ze względów bezpieczeństwa'": {"pat": -15, "avl": 0, "fin": 0, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Konferencja prasowa: przyznanie się do wycieku RODO": {"pat": +5, "avl": 0, "fin": -15, "comp": +25}, "Zablokowanie wypowiedzi, groźby pozwów": {"pat": -5, "avl": 0, "fin": +5, "comp": -30}}}}},
         4: {"title": "ETAP 4 - PARALIŻ KLINICZNY", "desc": "Niedziela, 14:00. Skrajne wyczerpanie personelu. Podawanie leków z pamięci. Wkraczają kontrolerzy z MZ i UODO.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Przekazanie serwerów organom śledczym (dowody)": {"pat": -15, "avl": -20, "fin": 0, "comp": +30}, "Priorytet przywrócenia bazy leków (odmowa wydania sprzętu)": {"pat": +25, "avl": +20, "fin": -10, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Powołanie Komisji Etycznej (Triage leków ratujących życie)": {"pat": +15, "avl": 0, "fin": 0, "comp": +10}, "Podawanie leków losowo, unikanie odpowiedzialności": {"pat": -30, "avl": 0, "fin": 0, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Pełna współpraca z MZ i udostępnienie dokumentacji": {"pat": 0, "avl": 0, "fin": 0, "comp": +25}, "Wpuszczenie nadzoru tylko z prawnikami": {"pat": 0, "avl": 0, "fin": -20, "comp": -30}}}}},
         5: {"title": "ETAP 5 - POST-MORTEM I ROZLICZENIE", "desc": "Dzień 7. Częściowe odzyskanie danych. Ogromne straty wizerunkowe. Raport końcowy organów nadzoru.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Migracja systemów do Chmury Krajowej (Zero Trust)": {"pat": +10, "avl": +30, "fin": -30, "comp": +20}, "Odbudowa lokalnej serwerowni i zakup 'lepszego antywirusa'": {"pat": -10, "avl": -15, "fin": +15, "comp": -20}}}, "Med": {"label": "SZKOLENIA:", "options": {"Comiesięczne symulacje ataków (Downtime Drills)": {"pat": +20, "avl": 0, "fin": -10, "comp": +15}, "Jednorazowe szkolenie e-learningowe": {"pat": -15, "avl": 0, "fin": +5, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Dyrektor składa dymisję, ułatwiając negocjacje finansowe": {"pat": 0, "avl": 0, "fin": +20, "comp": +10}, "Zwolnienie Głównego Informatyka jako manewr PR": {"pat": 0, "avl": 0, "fin": -10, "comp": -10}}}}}
    },
    "Wariant D: Niewidzialny Zabójca (Zatrucie Danych - 4 Rundy)": {
         1: {"title": "ETAP 1 - PODEJRZANY BŁĄD DANYCH", "desc": "Wtorek, 11:00. Pielęgniarka wstrzymuje transfuzję - system pokazuje złą grupę krwi. Z bazy zniknęła informacja o śmiertelnej alergii pacjenta. Systemy działają płynnie.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Zablokowanie edycji w bazie (Read-Only) i audyt logów": {"pat": +10, "avl": -10, "fin": -5, "comp": +10}, "Restart serwera aplikacyjnego (traktowanie jako błąd)": {"pat": -20, "avl": +5, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wstrzymanie operacji do czasu weryfikacji krwi w laboratorium": {"pat": +25, "avl": 0, "fin": -15, "comp": +10}, "Kontynuowanie zabiegów, nakaz 'podwójnego sprawdzania'": {"pat": -30, "avl": 0, "fin": +5, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Poufne zgłoszenie na Policję (podejrzenie sabotażu)": {"pat": 0, "avl": 0, "fin": 0, "comp": +20}, "Czekanie na wewnętrzne wyjaśnienie sprawy": {"pat": 0, "avl": 0, "fin": +5, "comp": -15}}}}},
         2: {"title": "ETAP 2 - EPIDEMIA NIEUFNOŚCI", "desc": "Wtorek, 16:00. Ktoś modyfikował setki wyników i dawek. Lekarze odmawiają podawania leków. Haker żąda 1 mln zł za listę zmienionych rekordów.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Przywrócenie bazy z backupu (utrata wpisów z ostatnich 48h)": {"pat": +10, "avl": -20, "fin": -10, "comp": +15}, "Próba ręcznego wyśledzenia złośliwych modyfikacji": {"pat": -25, "avl": +10, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Masowe ponowne pobieranie krwi (gigantyczne koszty)": {"pat": +25, "avl": -10, "fin": -25, "comp": +10}, "Poleganie na starych, papierowych wydrukach z biurek": {"pat": -10, "avl": +5, "fin": +5, "comp": -10}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Transparentne powiadomienie MZ i pacjentów": {"pat": +10, "avl": 0, "fin": -25, "comp": +30}, "Zatajenie manipulacji jako 'awarii technicznej'": {"pat": -10, "avl": 0, "fin": +10, "comp": -40}}}}},
         3: {"title": "ETAP 3 - KRET CZY PRZEJĘTE KONTO?", "desc": "Środa, 10:00. Służby informują o użyciu danych logowania ordynatora (brak 2FA, ofiara phishingu). Sprawa wypływa w mediach.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wymuszone natychmiastowe wdrożenie MFA (SMS) dla wszystkich": {"pat": +10, "avl": -15, "fin": -10, "comp": +25}, "Tylko masowy reset haseł na silniejsze": {"pat": -15, "avl": +10, "fin": +5, "comp": -15}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Szkolenie z cyberhigieny dla personelu (opóźnienia na izbie)": {"pat": +15, "avl": -10, "fin": -10, "comp": +15}, "Zostawienie personelu na stanowiskach, instrukcje mailem": {"pat": -10, "avl": +15, "fin": +5, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Ochrona oszukanego ordynatora, nacisk na naprawę procesów": {"pat": 0, "avl": 0, "fin": 0, "comp": +15}, "Zwolnienie ordynatora, zrzucenie winy": {"pat": -5, "avl": 0, "fin": +10, "comp": -15}}}}},
         4: {"title": "ETAP 4 - ROZLICZENIE Z ZAUFANIA", "desc": "Czwartek, 12:00. Kryzys opanowany, dane odtworzone. Szpital stoi przed pozwami zbiorowymi od pacjentów, którym podano złe leki.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wdrożenie systemu DLP i zaawansowanego monitorowania logów": {"pat": +15, "avl": +5, "fin": -25, "comp": +20}, "Brak większych zmian strukturalnych": {"pat": -20, "avl": +10, "fin": +15, "comp": -30}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Darmowe badania kontrolne dla pacjentów ze zmanipulowanej puli": {"pat": +25, "avl": -5, "fin": -30, "comp": +15}, "Oczekiwanie na pozwy, brak działań proaktywnych": {"pat": -10, "avl": +5, "fin": +10, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Powołanie oficera ds. integralności danych klinicznych": {"pat": +10, "avl": 0, "fin": -10, "comp": +15}, "Wydatkowanie budżetu naprawczego na kampanię PR": {"pat": -10, "avl": 0, "fin": -15, "comp": -20}}}}}
    },
    "Wariant E: Przerwany Łańcuch (Atak na Telemedycynę - 4 Rundy)": {
         1: {"title": "ETAP 1 - PARALIŻ ZEWNĘTRZNY", "desc": "Środa, 18:00. Padła zewnętrzna chmura radiologiczna i platforma tele-monitoringu kardiologicznego. Awaria po stronie dostawcy.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Natychmiastowe zerwanie VPN z chmurą dostawcy (Air-Gap)": {"pat": 0, "avl": -20, "fin": -5, "comp": +15}, "Utrzymanie aktywnych połączeń API w oczekiwaniu na naprawę": {"pat": -15, "avl": +5, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wezwanie lokalnych radiologów na nadgodziny do szpitala": {"pat": +20, "avl": +10, "fin": -25, "comp": +5}, "Wstrzymanie opisów planowych, diagnostyka tylko na ratunek": {"pat": -15, "avl": -10, "fin": +10, "comp": -5}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Wdrożenie papierowych procedur dla pacjentów z telemonitoringu": {"pat": +15, "avl": 0, "fin": -10, "comp": +10}, "Uznanie to za awarię techniczną dostawcy, brak aktywacji BCP": {"pat": -20, "avl": 0, "fin": +5, "comp": -15}}}}},
         2: {"title": "ETAP 2 - ZARAZA PO ŁĄCZACH", "desc": "Środa, 22:00. Dostawca padł ofiarą wirusa replikującego się przez API. Wirus puka do waszych serwerów. Wyciekły dane telemetryczne.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Odcięcie całego szpitala od sieci Internet w celu skanowania": {"pat": -10, "avl": -30, "fin": -15, "comp": +25}, "Bieżąca aktualizacja antywirusa i blokowanie IP dostawcy": {"pat": -25, "avl": +15, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wysłanie karetek po pacjentów kardiologicznych wysokiego ryzyka": {"pat": +30, "avl": 0, "fin": -30, "comp": +10}, "Wysłanie SMS-ów do pacjentów z prośbą o zgłaszanie złego stanu": {"pat": -30, "avl": 0, "fin": +10, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie do UODO wycieku, przyjęcie roli administratora danych": {"pat": +10, "avl": 0, "fin": -5, "comp": +30}, "Przerzucanie odpowiedzialności na dostawcę, brak zgłoszeń": {"pat": 0, "avl": 0, "fin": 0, "comp": -35}}}}},
         3: {"title": "ETAP 3 - ODPOWIEDZIALNOŚĆ STRON", "desc": "Czwartek, 08:00. Ostra krytyka w mediach dotycząca cięcia kosztów bezpieczeństwa. Wąskie gardła w radiologii paraliżują placówkę.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wymóg audytów bezpieczeństwa TLPT od nowego dostawcy": {"pat": +10, "avl": -10, "fin": -15, "comp": +25}, "Podpisanie najtańszej umowy bez audytu celem szybkiego powrotu": {"pat": -20, "avl": +25, "fin": +15, "comp": -30}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Osobiste, telefoniczne uspokajanie pacjentów przez lekarzy": {"pat": +25, "avl": -5, "fin": -15, "comp": +15}, "Wydanie ogólnego oświadczenia na stronie www szpitala": {"pat": -15, "avl": 0, "fin": +5, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Pozew sądowy o odszkodowanie i rozwiązanie umowy z dostawcą": {"pat": +5, "avl": 0, "fin": +10, "comp": +15}, "Kontynuacja umowy przy rekompensacie 'darmowego roku'": {"pat": -25, "avl": +10, "fin": +25, "comp": -25}}}}},
         4: {"title": "ETAP 4 - NOWA ARCHITEKTURA", "desc": "Piątek. Konieczność przedstawienia Ministerstwu Zdrowia planu zarządzania ryzykiem. Zdarzenie uwidoczniło uzależnienie od jednej platformy.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Strategia Multi-Cloud (wielu dostawców) z systemem Failover": {"pat": +15, "avl": +20, "fin": -35, "comp": +20}, "Wycofanie się do technologii lokalnej (serwery szpitalne)": {"pat": -10, "avl": -15, "fin": -10, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Fizyczne plany awaryjne (BCP) dla wdrażanej aparatury": {"pat": +20, "avl": 0, "fin": -10, "comp": +20}, "Redukcja aparatury analogowej dla cięcia kosztów": {"pat": -25, "avl": +10, "fin": +20, "comp": -25}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Powołanie Działu Zarządzania Ryzykiem Stron Trzecich (NIS2)": {"pat": +15, "avl": 0, "fin": -15, "comp": +25}, "Weryfikacja bezpieczeństwa vendora wyłącznie przez Dział Zakupów": {"pat": -20, "avl": 0, "fin": +15, "comp": -30}}}}}
    }
}

# --- FUNKCJE POMOCNICZE ---
def calculate_score(team_name):
    pat, avl, fin, comp = 100, 100, 100, 100
    if state["active_scenario"] not in ALL_SCENARIOS: return pat, avl, fin, comp
    active_scenario_data = ALL_SCENARIOS[state["active_scenario"]]
    
    for r in range(1, state["round"] + 1):
        if r in state["teams"][team_name]["decisions"] and r in active_scenario_data:
            for role, choice in state["teams"][team_name]["decisions"][r].items():
                impact = active_scenario_data[r]["questions"][role]["options"][choice]
                pat += impact["pat"]
                avl += impact["avl"]
                fin += impact["fin"]
                comp += impact["comp"]
    return max(0, min(150, pat)), max(0, min(150, avl)), max(0, min(150, fin)), max(0, min(150, comp))

def render_cyber_kpi(label, value, is_critical=False):
    pct = int(min((value/150)*100, 100))
    fill_class = "kpi-fill critical" if (is_critical and value < 50) else "kpi-fill"
    
    return f"""
    <div class="kpi-row">
        <div class="kpi-labels">
            <span>{label}</span>
            <span>{pct}%</span>
        </div>
        <div class="kpi-bg">
            <div class="{fill_class}" style="width: {pct}%;"></div>
        </div>
    </div>
    """

# --- WIDOKI ---
def login_view():
    st.markdown("""
        <div class="top-bar" style="margin-top: 0;">
            <div class="top-bar-title">HOSPITAL OS // COMMAND</div>
            <div class="top-bar-info">AUTORYZACJA WYMAGANA</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='cyber-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>IDENTYFIKACJA SYSTEMU</div>", unsafe_allow_html=True)
        team_name = st.text_input("ID ZESPOŁU (KRYPTONIM):")
        if st.button("LOG_IN", use_container_width=True, type="primary"):
            if team_name:
                if team_name not in state["teams"]:
                    state["teams"][team_name] = {"decisions": {}, "ready": False}
                st.session_state["role"] = "team"
                st.session_state["team_name"] = team_name
                st.rerun()
            else:
                st.error("Odmowa. Wprowadź ID.")
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("⚙️ Dostęp Administracyjny / Kod QR"):
            game_url = st.text_input("Link dla terminali mobilnych (QR):")
            if game_url:
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={game_url}"
                st.image(qr_url)
            
            admin_pass = st.text_input("Klucz ROOT:", type="password")
            if st.button("ZALOGUJ JAKO ADMIN"):
                if admin_pass == "admin":
                    st.session_state["role"] = "admin"
                    st.rerun()

def admin_view():
    st.markdown("""
        <div class="top-bar" style="margin-top: 0;">
            <div class="top-bar-title">HOSPITAL OS // ROOT ACCESS</div>
            <div class="top-bar-info">
                <span onclick="window.location.reload();" style="cursor:pointer;">[ ZAKOŃCZ SESJĘ ]</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if state["round"] == 0:
        selected = st.selectbox("Wybierz scenariusz wektora ataku:", list(ALL_SCENARIOS.keys()), index=list(ALL_SCENARIOS.keys()).index(state["active_scenario"]))
        if selected != state["active_scenario"]:
            state["active_scenario"] = selected
            st.success(f"Aktywowano wektor: {selected}")
            
    col1, col2 = st.columns(2)
    with col1:
        total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])
        st.metric("Aktywna Faza", state["round"])
        if state["round"] <= total_rounds:
            if st.button("URUCHOM NASTĘPNY ETAP ⏩", type="primary"):
                state["round"] += 1
                for t in state["teams"]: state["teams"][t]["ready"] = False
                st.rerun()
        else:
            if st.button("RESETUJ SYSTEM 🔄"):
                state["round"] = 0
                state["teams"] = {}
                st.rerun()
                
    with col2:
        st.write("### Status Połączeń Zespołów")
        if not state["teams"]:
            st.info("Brak aktywnych połączeń.")
        for t, data in state["teams"].items():
            status = "✅ Przesłano logi" if data["ready"] else "⏳ Analiza..."
            st.write(f"- **{t}**: {status}")

    st.write("---")
    if state["teams"]:
        scores = []
        for t in state["teams"]:
            p, a, f, c = calculate_score(t)
            scores.append({"ID Zespołu": t, "Pacjenci": p, "Systemy": a, "Finanse": f, "Zgodność": c})
        st.dataframe(pd.DataFrame(scores), use_container_width=True)

def team_view():
    team = st.session_state.get("team_name")
    
    # Auto-Kick (Naprawa KeyError)
    if not team or team not in state["teams"]:
        st.session_state.pop("role", None)
        st.session_state.pop("team_name", None)
        st.rerun()
        return
        
    total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])
    p, a, f, c = calculate_score(team)
    
    active_inc = f"VAR-{state['active_scenario'][:3].upper()}" if state["round"] > 0 else "OCZEKIWANIE"
    st.markdown(f"""
        <div class="top-bar">
            <div class="top-bar-title">HOSPITAL OS // COMMAND</div>
            <div class="top-bar-alert">🔴 INCYDENT AKTYWNY: {active_inc}</div>
            <div class="top-bar-info">
                ZESPÓŁ: <span>{team.upper()}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1.2, 2.8, 1.2], gap="large")
    
    # --- LEWA KOLUMNA ---
    with col_left:
        st.markdown("<div class='cyber-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>METRYKI SYSTEMOWE</div>", unsafe_allow_html=True)
        st.markdown(render_cyber_kpi("PACJENCI", p, is_critical=True), unsafe_allow_html=True)
        st.markdown(render_cyber_kpi("SYSTEMY", a), unsafe_allow_html=True)
        st.markdown(render_cyber_kpi("FINANSE", f), unsafe_allow_html=True)
        st.markdown(render_cyber_kpi("ZGODNOŚĆ", c), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='cyber-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-header'>DZIENNIK ZDARZEŃ SESJI</div>", unsafe_allow_html=True)
        
        if state["round"] == 0:
            st.markdown("<div class='log-entry'><span class='log-time'>[T-00:00]</span><div class='log-title'>SYSTEM W TRYBIE NASŁUCHU</div><div class='log-desc'>Brak zidentyfikowanych anomalii.</div></div>", unsafe_allow_html=True)
        elif state["round"] > total_rounds:
             st.markdown(f"<div class='log-entry'><span class='log-time'>[T-{total_rounds*15:02d}:00]</span><div class='log-title' style='color:#34d399;'>OPERACJA ZAKOŃCZONA</div></div>", unsafe_allow_html=True)
        else:
            for i in range(1, state["round"]):
                st.markdown(f"<div class='log-entry'><span class='log-time'>[T-{(i-1)*15:02d}:00]</span><div class='log-title'>ETAP_{i}: ZAKOŃCZONO</div><div class='log-desc'>Analiza skutków wdrożona w systemie.</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='log-entry'><span class='log-time'>[T-{(state['round']-1)*15:02d}:00]</span><div class='log-title' style='color:#00f0ff;'>ETAP_{state['round']}: OCZEKIWANIE NA DECYZJE</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ŚRODKOWA KOLUMNA ---
    with col_center:
        if state["round"] == 0:
            st.markdown("""
                <div class='doc-header'><span class='doc-tag'>SYSTEM STANDBY</span><span class='doc-timer'>00:00</span></div>
                <div class='stage-title'><div class='stage-dot' style='background-color:#34d399; box-shadow: 0 0 15px #34d399;'></div>OCZEKIWANIE NA INCYDENT</div>
                <div class='warning-box' style='border-left-color: #34d399;'>Sieć monitorowana. Proszę czekać na instrukcje z Dowództwa.</div>
            """, unsafe_allow_html=True)
            if st.button("📡 POBIERZ NOWE DANE", use_container_width=True): st.rerun()
            
        elif 1 <= state["round"] <= total_rounds:
            r = state["round"]
            scenario = ALL_SCENARIOS[state["active_scenario"]][r]
            
            st.markdown(f"""
                <div class='doc-header'><span class='doc-tag'>DOKUMENTACJA ZDARZENIA ID: 0x{r}</span><span class='doc-timer'>⚠️ WYMAGANA AKCJA</span></div>
                <div class='stage-title'><div class='stage-dot'></div>{scenario['title']}</div>
                <div class='warning-box'>{scenario['desc']}</div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='panel-header'>⚙️ ANALIZA DORADCY (WYBIERZ ROZKAZY)</div>", unsafe_allow_html=True)
            
            if not state["teams"][team]["ready"]:
                with st.form(f"form_r{r}"):
                    choices = {}
                    for role, q_data in scenario["questions"].items():
                        st.markdown(f"<span style='color: #94a3b8; font-size: 14px; font-weight: bold;'>{q_data['label']}</span>", unsafe_allow_html=True)
                        choices[role] = st.radio(f"Wybór {role}", list(q_data["options"].keys()), label_visibility="collapsed")
                        st.write("<br>", unsafe_allow_html=True)
                    
                    if st.form_submit_button("WPROWADŹ ROZKAZY DO SYSTEMU 📝", type="primary"):
                        if r not in state["teams"][team]["decisions"]: state["teams"][team]["decisions"][r] = {}
                        state["teams"][team]["decisions"][r] = choices
                        state["teams"][team]["ready"] = True
                        st.rerun()
            else:
                st.markdown("<div class='warning-box' style='border-left-color:#34d399; color:#34d399;'>Rozkazy wdrożone. Czekaj na synchronizację sieci.</div>", unsafe_allow_html=True)
                if st.button("📡 SPRAWDŹ STATUS SIECI", use_container_width=True): st.rerun()

        elif state["round"] > total_rounds:
            st.markdown("""
                <div class='doc-header'><span class='doc-tag'>AUDYT KOŃCOWY</span><span class='doc-timer'>ZAKOŃCZONO</span></div>
                <div class='stage-title'><div class='stage-dot' style='background-color:#00f0ff; box-shadow: 0 0 15px #00f0ff;'></div>PODSUMOWANIE OPERACJI</div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='panel-header'>🏆 GLOBALNY RANKING JEDNOSTEK</div>", unsafe_allow_html=True)
            ranking_data = []
            for t_name in state["teams"]:
                tp, ta, tf, tc = calculate_score(t_name)
                total_score = tp + ta + tf + tc
                ranking_data.append({"KRYPTONIM": t_name, "SCORE": total_score, "PACJENCI": tp, "SYSTEMY": ta, "FINANSE": tf, "ZGODNOŚĆ": tc})
                
            df_ranking = pd.DataFrame(ranking_data)
            if not df_ranking.empty:
                df_ranking = df_ranking.sort_values(by=["SCORE", "PACJENCI"], ascending=[False, False]).reset_index(drop=True)
                df_ranking.index = df_ranking.index + 1 
                st.dataframe(df_ranking, use_container_width=True)

            st.markdown(f"<div class='panel-header' style='margin-top: 30px;'>📋 STATUS LOKALNY: {team.upper()}</div>", unsafe_allow_html=True)
            if p < 50:
                st.markdown("<div class='warning-box' style='border-left-color:#ef4444; color:#ef4444;'>Wyrok Prokuratora: ZAGROŻENIE ŻYCIA PACJENTÓW. Oczekuj aktu oskarżenia. (Poniżej 50 pkt)</div>", unsafe_allow_html=True)
            elif c < 50:
                st.markdown("<div class='warning-box' style='border-left-color:#ef4444; color:#ef4444;'>Wyrok Regulatora: KATASTROFA PRAWNA. Nałożono maksymalne kary finansowe (RODO/NIS2).</div>", unsafe_allow_html=True)
            elif p >= 80 and c >= 80:
                st.markdown("<div class='warning-box' style='border-left-color:#34d399; color:#34d399;'>Wyrok: MISTRZOWSKIE ZARZĄDZANIE KRYZYSEM. Infrastruktura i pacjenci zabezpieczeni.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='warning-box' style='border-left-color:#fbbf24; color:#fbbf24;'>Wyrok: SZPITAL PRZETRWAŁ Z DUŻYMI STRATAMI. Decyzje operacyjne wymagały kompromisów.</div>", unsafe_allow_html=True)

    # --- PRAWA KOLUMNA ---
    with col_right:
        if state["round"] == 0:
            st.markdown("""
                <div class='status-box'>
                    <div class='status-icon wait'>📡</div>
                    <div class='status-title'>NASŁUCH</div>
                    <div class='status-desc'>Połączenie z serwerem głównym stabilne.</div>
                </div>
            """, unsafe_allow_html=True)
        elif 1 <= state["round"] <= total_rounds:
            if state["teams"][team]["ready"]:
                st.markdown("""
                    <div class='status-box'>
                        <div class='status-icon done'>✓</div>
                        <div class='status-title'>TRANSMISJA ZAKOŃCZONA</div>
                        <div class='status-desc'>Logi decyzji przesłane do Głównej Sieci. Oczekuj na weryfikację.</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='status-box'>
                        <div class='status-icon wait'>!</div>
                        <div class='status-title'>WYMAGANA AKCJA</div>
                        <div class='status-desc'>Wprowadź rozkazy i zatwierdź transmisję.</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='status-box'>
                    <div class='status-icon done'>🏁</div>
                    <div class='status-title'>RAPORT WYGENEROWANY</div>
                    <div class='status-desc'>Sesja zamknięta.</div>
                </div>
            """, unsafe_allow_html=True)

# --- ROUTER ---
if "role" not in st.session_state:
    login_view()
elif st.session_state["role"] == "admin":
    admin_view()
elif st.session_state["role"] == "team":
    team_view()
