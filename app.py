import streamlit as st
import pandas as pd
import datetime
import time
import base64
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="CyberGra Decyzyjna - Atak na Szpital // COMMAND CENTER",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

# --- HELPER FUNKCJA DO ZDJĘCIA LOKALNEGO W HTML ---
def get_image_as_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Pobierz base64 logotypu, aby użyć go w CSS (jeśli plik logo.png nie istnieje, zignoruje to bez błędu)
logo_b64 = get_image_as_base64("LOGO.png")

# --- PROFESSIONAL POLISH CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {{
        --bg-color: #0f172a;
        --panel-bg: #1e293b;
        --border-color: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --accent-cyan: #06b6d4;
        --accent-red: #ef4444;
        --accent-green: #22c55e;
        --accent-yellow: #f59e0b;
        --font-sans: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }}

    /* Global Overrides */
    .stApp {{
        background-color: var(--bg-color) !important;
        color: var(--text-primary);
        font-family: var(--font-sans);
        /* Dodajemy margines na dole, aby treść nie chowała się pod stopką z logo */
        padding-bottom: 80px; 
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}

    /* Layout Containers */
    .command-header {{
        height: 64px;
        background: rgba(15, 23, 42, 0.8);
        border-bottom: 1px solid var(--border-color);
        padding: 0 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: -75px;
        margin-bottom: 24px;
        position: sticky;
        top: 0;
        z-index: 1000;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand-title {{
        font-family: var(--font-mono);
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 0.1em;
        color: var(--accent-cyan);
        text-transform: uppercase;
    }}

    .status-badge {{
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid var(--accent-red);
        color: var(--accent-red);
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }}

    /* Professional Panels */
    .panel {{
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 16px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}

    .panel-label {{
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: block;
    }}

    /* KPI Display */
    .kpi-container {{
        margin-bottom: 14px;
    }}

    .kpi-header {{
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        margin-bottom: 6px;
        font-weight: 500;
    }}

    .kpi-value {{
        font-family: var(--font-mono);
        color: var(--text-primary);
    }}

    .progress-bar-bg {{
        background: var(--bg-color);
        height: 4px;
        border-radius: 2px;
        overflow: hidden;
    }}

    .progress-bar-fill {{
        height: 100%;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        background: var(--accent-cyan);
        box-shadow: 0 0 8px rgba(6, 182, 212, 0.4);
    }}

    /* Situational Room */
    .scenario-header {{
        background: linear-gradient(135deg, var(--panel-bg) 0%, var(--bg-color) 100%);
        border-left: 4px solid var(--accent-red);
        border-radius: 0 6px 6px 0;
        padding: 20px;
        margin-bottom: 20px;
    }}

    .scenario-id {{
        font-family: var(--font-mono);
        color: var(--accent-cyan);
        font-size: 0.75rem;
        margin-bottom: 4px;
    }}

    .scenario-title {{
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text-primary);
    }}

    .scenario-desc {{
        color: var(--text-secondary);
        line-height: 1.6;
        margin-top: 12px;
        font-size: 0.95rem;
    }}

    /* Forms and Buttons */
    .stButton > button {{
        background: var(--accent-cyan) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 4px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 14px !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        opacity: 0.9 !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.3) !important;
        transform: none !important;
    }}

    .stRadio label {{
        background: #2d3748 !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        border-radius: 4px !important;
        font-size: 0.85rem !important;
        margin-bottom: 8px !important;
    }}

    .stRadio div[role="radiogroup"] > label:hover {{
        border-color: var(--accent-cyan) !important;
        background: rgba(6, 182, 212, 0.05) !important;
    }}

    /* Terminal Logs */
    .log-item {{
        font-family: var(--font-mono);
        font-size: 0.7rem;
        padding: 4px 0 4px 8px;
        border-left: 2px solid var(--border-color);
        margin-bottom: 8px;
    }}
    .log-ts {{ color: var(--accent-yellow); }}
    .log-act {{ color: var(--accent-cyan); font-weight: 600; margin-left: 4px; }}
    .log-msg {{ color: var(--text-secondary); display: block; margin-top: 2px; }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg-color); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 2px; }}
    
    /* --- LOGO FOOTER CSS --- */
    .custom-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: rgba(15, 23, 42, 0.95);
        border-top: 1px solid var(--border-color);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    }}
    .footer-logo {{
        height: 40px; /* Maksymalna wysokość logo na pasku */
        max-width: 90%;
        object-fit: contain;
        opacity: 0.85; /* Delikatne wtopienie w tło */
        transition: opacity 0.3s;
    }}
    .footer-logo:hover {{
        opacity: 1;
    }}
    </style>
""", unsafe_allow_html=True)

# WSTRZYKNIĘCIE STOPKI Z LOGO NA KAŻDĄ STRONĘ
if logo_b64:
    st.markdown(f"""
        <div class="custom-footer">
            <img src="data:image/png;base64,{logo_b64}" class="footer-logo" alt="System Logo">
        </div>
    """, unsafe_allow_html=True)
else:
    # Fallback tekstowy jeśli plik logo.png nie zostanie odnaleziony
    st.markdown("""
        <div class="custom-footer">
            <span style="font-family: var(--font-mono); color: var(--text-secondary); font-size: 12px; letter-spacing: 2px;">
                SYSTEM // SECURE CONNECTION ESTABLISHED
            </span>
        </div>
    """, unsafe_allow_html=True)


# --- GAME ENGINE STATE ---
@st.cache_resource
def get_engine():
    return {
        "round": 0,
        "teams": {},
        "active_scenario_key": "Wariant C: Zaawansowany Atak APT (5 Rund)",
        "logs": []
    }

state = get_engine()

# --- SCENARIOS DATABASE ---
SCENARIOS = {
    "Wariant A: Ransomware (Klasyczny)": {
         1: {
            "title": "FAZA 1: PIERWSZE SZYFROWANIE",
            "desc": "Stacje robocze w rejestracji nagle tracą dostęp do plików. Na ekranach pojawia się informacja o zaszyfrowaniu danych. Atakujący żądają 500 000 PLN w Bitcoin.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Natychmiastowe odłączenie zainfekowanych stacji": {"pat": 0, "avl": -10, "fin": 0, "comp": +5}, "Próba lokalizacji złośliwego procesu": {"pat": -5, "avl": 0, "fin": 0, "comp": -5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Kontynuacja pracy na papierze": {"pat": +10, "avl": -5, "fin": -5, "comp": 0}, "Czekanie na przywrócenie systemów": {"pat": -15, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Zawiadomienie Policji i CERT": {"pat": 0, "avl": 0, "fin": 0, "comp": +20}, "Brak zgłoszenia (ochrona wizerunku)": {"pat": 0, "avl": 0, "fin": 0, "comp": -25}}}
            }
         },
         2: {
            "title": "FAZA 2: ROZPRZESTRZENIANIE",
            "desc": "Wirus przeskoczył do sieci laboratorium. Wyniki badań nie trafiają do lekarzy. Na SORze rośnie kolejka, pacjenci stają się agresywni.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Blokada całej sieci wewnętrznej": {"pat": -5, "avl": -30, "fin": -10, "comp": +10}, "Selektywne wyłączanie serwerów": {"pat": -10, "avl": -10, "fin": -5, "comp": -10}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Przekierowanie pacjentów do innych szpitali": {"pat": +20, "avl": 0, "fin": -20, "comp": +10}, "Próba pracy w chaosie": {"pat": -30, "avl": 0, "fin": 0, "comp": -20}}},
                "Dir": {"label": "ZARZĄD", "options": {"Oficjalny komunikat o awarii": {"pat": +10, "avl": 0, "fin": 0, "comp": +15}, "Ukrywanie skali problemu": {"pat": -20, "avl": 0, "fin": 0, "comp": -30}}}
            }
         },
         3: {
            "title": "FAZA 3: NEGOCJACJE",
            "desc": "Hakerzy grożą publikacją danych pacjentów, jeśli okup nie zostanie wpłacony w ciągu 12h. Media zaczynają dopytywać o wyciek.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Podjęcie prób deszyfracji narzędziami darmowymi": {"pat": -5, "avl": -5, "fin": 0, "comp": -10}, "Przywracanie z backupów (powolne)": {"pat": +5, "avl": +10, "fin": -5, "comp": +10}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Weryfikacja danych pacjentów z papieru": {"pat": +15, "avl": 0, "fin": -5, "comp": 0}, "Zaniechanie weryfikacji tożsamości": {"pat": -40, "avl": 0, "fin": 0, "comp": -20}}},
                "Dir": {"label": "ZARZĄD", "options": {"Wynajęcie negocjatora": {"pat": 0, "avl": 0, "fin": -15, "comp": +5}, "Ignorowanie hakerów": {"pat": 0, "avl": 0, "fin": 0, "comp": -10}}}
            }
         },
         4: {
            "title": "FAZA 4: ATAK NA BACKUPY",
            "desc": "Okazuje się, że backupy również zostały częściowo uszkodzone. Szpital staje przed wizją utraty historii leczenia tysięcy ludzi.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Próba odzyskania danych z dysków fizycznych": {"pat": 0, "avl": +5, "fin": -10, "comp": +5}, "Zaakceptowanie utraty części danych": {"pat": -25, "avl": -20, "fin": +10, "comp": -30}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Wywiady lekarskie z każdym pacjentem": {"pat": +20, "avl": 0, "fin": -10, "comp": 0}, "Leczenie na podstawie szczątkowych danych": {"pat": -50, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Zgłoszenie naruszenia do UODO": {"pat": 0, "avl": 0, "fin": 0, "comp": +40}, "Zatajenie utraty danych": {"pat": 0, "avl": 0, "fin": 0, "comp": -50}}}
            }
         },
         5: {
            "title": "FAZA 5: ODBUDOWA",
            "desc": "Systemy wracają. Rozpoczyna się wielkie sprzątanie i audyt poincydentalny.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Wdrożenie polityki offline backup": {"pat": 0, "avl": +20, "fin": -10, "comp": +15}, "Instalacja nowszej wersji antywirusa": {"pat": 0, "avl": -10, "fin": +5, "comp": -15}}},
                "Med": {"label": "EDUKACJA", "options": {"Szkolenie personelu z phishingu": {"pat": +10, "avl": 0, "fin": -5, "comp": +10}, "Brak dodatkowych szkoleń": {"pat": -10, "avl": 0, "fin": 0, "comp": -10}}},
                "Dir": {"label": "ZARZĄD", "options": {"Stworzenie realnej procedury DRP": {"pat": +5, "avl": +5, "fin": -15, "comp": +20}, "Ograniczenie budżetu IT na poczet strat": {"pat": -15, "avl": -20, "fin": +10, "comp": -10}}}
            }
         }
    },
    "Wariant B: Insider Threat (Błąd Ludzki/Zemsta)": {
         1: {
            "title": "FAZA 1: DZIWNE UPRAWNIENIA",
            "desc": "Zwolniony wczoraj informatyk nadal loguje się do systemu. Zmienia hasła administratorów domeny. Szpital traci kontrolę nad kontami personelu.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Fizyczne odłączenie serwera AD": {"pat": 0, "avl": -30, "fin": 0, "comp": +10}, "Próba blokady konta z poziomu zapasowego": {"pat": -15, "avl": 0, "fin": 0, "comp": -10}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Działanie bez dostępu do kont (hasła papierowe)": {"pat": +5, "avl": -10, "fin": 0, "comp": 0}, "Logowanie na konta 'ogólne'": {"pat": -10, "avl": 0, "fin": 0, "comp": -25}}},
                "Dir": {"label": "ZARZĄD", "options": {"Zawiadomienie prokuratury": {"pat": 0, "avl": 0, "fin": 0, "comp": +20}, "Próba polubownego kontaktu": {"pat": 0, "avl": 0, "fin": 0, "comp": -10}}}
            }
         },
         2: {
            "title": "FAZA 2: SABOTAŻ BAZY LEKÓW",
            "desc": "W bazie aptecznej zmieniono dawkowanie leków krytycznych. Lekarze zauważają błędy w ostatniej chwili. Systemy wydają błędne instrukcje.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Blokada zapisu do bazy i weryfikacja sum kontrolnych": {"pat": +20, "avl": -10, "fin": -5, "comp": +10}, "Restart serwera bazy danych": {"pat": -10, "avl": -20, "fin": 0, "comp": -5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Podwójna weryfikacja dawki przez dwóch lekarzy": {"pat": +30, "avl": -5, "fin": -5, "comp": 0}, "Zaufanie systemowi (brak czasu)": {"pat": -50, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Wstrzymanie planowych zabiegów": {"pat": +20, "avl": -20, "fin": -30, "comp": +10}, "Utrzymanie pełnej operacyjności": {"pat": -40, "avl": 0, "fin": +10, "comp": -20}}}
            }
         },
         3: {
            "title": "FAZA 3: WYCIEK DO KONKURENCJI/MEDIÓW",
            "desc": "Lista płac i premie zarządu trafiają do lokalnej gazety. Atmosfera w szpitalu staje się toksyczna. Personel zaczyna strajkować.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Audyt wszystkich wydruków i maili": {"pat": 0, "avl": 0, "fin": -5, "comp": +10}, "Blokada dostępu do internetu": {"pat": 0, "avl": -10, "fin": 0, "comp": -10}}},
                "Med": {"label": "ATMOSFERA", "options": {"Otwarte spotkanie z dyrekcją": {"pat": +5, "avl": 0, "fin": -5, "comp": +5}, "Ignorowanie protestów": {"pat": -10, "avl": 0, "fin": 0, "comp": -10}}},
                "Dir": {"label": "ZARZĄD", "options": {"Upublicznienie zarobków (pełna transparentność)": {"pat": 0, "avl": 0, "fin": -10, "comp": +25}, "Grozba zwolnień dyscyplinarnych": {"pat": 0, "avl": 0, "fin": 0, "comp": -30}}}
            }
         },
         4: {
            "title": "FAZA 4: USUNIĘCIE KLUCZOWYCH KONFIGURACJI",
            "desc": "Znikają ustawienia aparatury RTG i TK. Sprzęt medyczny jest sprawny, ale nie można go uruchomić z powodu braku oprogramowania sterującego.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Ściągnięcie serwisu producenta": {"pat": +10, "avl": +20, "fin": -25, "comp": +5}, "Próba wgrania starych ustawień": {"pat": -10, "avl": -10, "fin": 0, "comp": -5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Transport pacjentów na badania do innych miast": {"pat": +20, "avl": 0, "fin": -20, "comp": 0}, "Rezygnacja z badań obrazowych": {"pat": -40, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Fundusz awaryjny na naprawy": {"pat": 0, "avl": 0, "fin": -40, "comp": +5}, "Czekanie na darmowe wsparcie": {"pat": -10, "avl": -10, "fin": +10, "comp": -10}}}
            }
         },
         5: {
            "title": "FAZA 5: POST-MORTEM",
            "desc": "Sprawca zostaje ujęty. Pozostaje trauma i zniszczona reputacja.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Wdrożenie procedury 'off-boarding'": {"pat": 0, "avl": 0, "fin": -5, "comp": +30}, "Większa wiara w 'lojalność'": {"pat": 0, "avl": 0, "fin": 0, "comp": -40}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Psycholog dla personelu": {"pat": +15, "avl": 0, "fin": -5, "comp": 0}, "Brak działań wspierających": {"pat": -15, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Nowa polityka bezpieczeństwa personalnego": {"pat": 0, "avl": 0, "fin": -10, "comp": +20}, "Zwolnienie wszystkich z działu IT": {"pat": -20, "avl": -30, "fin": -10, "comp": -10}}}
            }
         }
    },
    "Wariant C: Zaawansowany Atak APT (5 Rund)": {
         1: {
            "title": "FAZA 1: ANOMALIA / REKONESANS",
            "desc": "Systemy PACS wykazują znaczne opóźnienia w transmisji danych obrazowych. Jednocześnie administratorzy zgłaszają serię nieudanych prób logowania na konta personelu administracyjnego. Ruch wychodzący z serwera LIS osiąga niespotykane piki.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Izolacja serwera LIS i wymuszony reset haseł": {"pat": 0, "avl": -10, "fin": -5, "comp": +10}, "Monitorowanie pasywne i analiza logów": {"pat": -5, "avl": +5, "fin": 0, "comp": -10}}},
                "Med": {"label": "PRODUKCJA MEDYCZNA", "options": {"Przejście na dokumentację analogową dla RTG": {"pat": +10, "avl": 0, "fin": -5, "comp": 0}, "Utrzymanie pracy w środowisku PACS mimo błędów": {"pat": -10, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Aktywacja niejawnego zespołu reagowania": {"pat": +5, "avl": 0, "fin": -5, "comp": +5}, "Klasyfikacja zdarzenia jako rutynowa awaria IT": {"pat": -10, "avl": 0, "fin": +5, "comp": -5}}}
            }
         },
         2: {
            "title": "FAZA 2: EKSFILTRACJA I PARALIŻ",
            "desc": "Atakujący ujawniają obecność. Systemy BMS (automatyka budynkowa) zostają przejęte. Klimatyzacja w salach operacyjnych zostaje zablokowana na maksymalnej temperaturze. Żądanie okupu: 2 000 000 PLN.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Strategiczny blackout sieci (Full Lockdown)": {"pat": -10, "avl": -40, "fin": -15, "comp": +20}, "Surgaliczna próba izolacji BMS (praca ciągła)": {"pat": -30, "avl": -10, "fin": -10, "comp": -15}}},
                "Med": {"label": "PRODUKCJA MEDYCZNA", "options": {"Ewakuacja bloków operacyjnych": {"pat": +25, "avl": 0, "fin": -10, "comp": +10}, "Kontynuacja zabiegów w trybie awaryjnym": {"pat": -40, "avl": 0, "fin": -20, "comp": -30}}},
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Ogłoszenie stanu zdarzenia masowego": {"pat": +20, "avl": 0, "fin": -25, "comp": +20}, "Cisza medialna i blokada informacji": {"pat": -20, "avl": 0, "fin": +10, "comp": -35}}}
            }
         },
         3: {
            "title": "FAZA 3: WOJNA INFORMACYJNA",
            "desc": "Wyciek danych pacjentów VIP. Media społecznościowe zalewa fala zrzutów ekranu z danymi wrażliwymi. Zdezorientowane rodziny pacjentów blokują wejście do szpitala.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Kontraktacja zewnętrznych ekspertów Incident Response": {"pat": +10, "avl": +15, "fin": -30, "comp": +20}, "Odzyskiwanie zasobów siłami wewnętrznymi": {"pat": -10, "avl": -10, "fin": +15, "comp": -10}}},
                "Med": {"label": "KOMUNIKACJA PR", "options": {"Otwarty dialog i wsparcie psychologiczne rodzin": {"pat": +15, "avl": 0, "fin": -5, "comp": +10}, "Blokada informacyjna (względy bezpieczeństwa)": {"pat": -15, "avl": 0, "fin": 0, "comp": -20}}},
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Transparentne przyznanie się do naruszenia": {"pat": +5, "avl": 0, "fin": -15, "comp": +25}, "Agresy kampania prawna i zaprzeczanie": {"pat": -5, "avl": 0, "fin": +5, "comp": -30}}}
            }
         },
         4: {
            "title": "FAZA 4: IMPAS OPERACYJNY",
            "desc": "Wyczerpanie personelu sięga zenitu. Podawanie leków odbywa się bez wsparcia systemowego. Rozpoczynają się kontrole z organów nadzorczych (UODO, MZ).",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Przekazaie infrastruktury do analizy śledczej": {"pat": -15, "avl": -20, "fin": 0, "comp": +30}, "Priorytetyzacja przywracania bazy leków": {"pat": +25, "avl": +20, "fin": -10, "comp": -20}}},
                "Med": {"label": "PRODUKCJA MEDYCZNA", "options": {"Powołanie Komisji Triage’u Etycznego": {"pat": +15, "avl": 0, "fin": 0, "comp": +10}, "Utrzymanie standardowej procedury (ryzyko błędów)": {"pat": -30, "avl": 0, "fin": 0, "comp": -20}}},
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Pełna współpraca z nadzorem państwowym": {"pat": 0, "avl": 0, "fin": 0, "comp": +25}, "Blokada dostępu do dokumentacji (linia obrony)": {"pat": 0, "avl": 0, "fin": -20, "comp": -30}}}
            }
         },
         5: {
            "title": "FAZA 5: POST-MORTEM",
            "desc": "Opanowanie wektora ataku. Rozpoczyna się szacowanie strat długofalowych i planowanie nowej architektury bezpieczeństwa.",
            "questions": {
                "IT": {"label": "STRATEGIA IT", "options": {"Migracja do chmury i model Zero Trust": {"pat": +10, "avl": +30, "fin": -30, "comp": +20}, "Odbudowa starych systemów z nowym EDR": {"pat": -10, "avl": -15, "fin": +15, "comp": -20}}},
                "Med": {"label": "EDUKACJA", "options": {"Cykliczne wiertła bezpieczeństwa (Red Teaming)": {"pat": +20, "avl": 0, "fin": -10, "comp": +15}, "Jednorazowy audyt zewnętrzny": {"pat": -15, "avl": 0, "fin": +5, "comp": -15}}},
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Restrukturyzacja zarządu i nowe partnerstwa": {"pat": 0, "avl": 0, "fin": +20, "comp": +10}, "Wyznaczenie kozłów ofiarnych w dziale IT": {"pat": 0, "avl": 0, "fin": -10, "comp": -10}}}
            }
         }
    },
    "Wariant D: IoT & Supply Chain Sabotage": {
         1: {
            "title": "FAZA 1: AWARIA POMP INFUZYJNYCH",
            "desc": "Pielęgniarki zgłaszają, że pompy infuzyjne na oddziale intensywnej terapii restartują się bez powodu. Niektóre zmieniają szybkość podawania leków.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Fizyczna izolacja sieci medycznej od Wi-Fi": {"pat": +5, "avl": -20, "fin": 0, "comp": +10}, "Próba wgrywania patcha w trakcie pracy": {"pat": -10, "avl": 0, "fin": 0, "comp": -5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Działanie w stałym nadzorze przy łóżku": {"pat": +20, "avl": 0, "fin": -5, "comp": 0}, "Zaufanie alarmom dźwiękowym (które mogą nie działać)": {"pat": -40, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Pilny kontakt z producentem sprzętu": {"pat": 0, "avl": 0, "fin": 0, "comp": +10}, "Skargi do serwisu sprzątającego (podejrzenie zalania)": {"pat": -5, "avl": 0, "fin": 0, "comp": -10}}}
            }
         },
         2: {
            "title": "FAZA 2: MANIPULACJA WINDAMI",
            "desc": "Windy w całym szpitalu stają. Pacjenci jadący na pilne operacje zostają uwięzieni. Ktoś zdalnie przejął sterowanie automatyką Hitachi/Otis.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Reset sterowników technicznych (ryzyko spadku)": {"pat": -5, "avl": -5, "fin": -10, "comp": -5}, "Awaryjne otwieranie manualne przez straż": {"pat": +15, "avl": 0, "fin": -5, "comp": +5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Uruchomienie transportu schodami (ryzykowne)": {"pat": +5, "avl": 0, "fin": -5, "comp": 0}, "Czekanie na przywrócenie sterowania": {"pat": -25, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Poinformowanie straży pożarnej": {"pat": +10, "avl": 0, "fin": 0, "comp": +15}, "Ukrywanie awarii przed pacjentami": {"pat": -10, "avl": 0, "fin": 0, "comp": -20}}}
            }
         },
         3: {
            "title": "FAZA 3: SKUŻONE LOGISTYKI LEKÓW",
            "desc": "System zamówień leków wysłał puste zamówienia do dostawcy. Zaczyna brakować tlenu i podstawowych antybiotyków.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Manualna weryfikacja wszystkich wyjść sieciowych API": {"pat": 0, "avl": 0, "fin": -5, "comp": +10}, "Podejrzenie błędu po stronie hurtowni": {"pat": 0, "avl": 0, "fin": 0, "comp": -10}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Ręczne inwentaryzacje na oddziałach": {"pat": +10, "avl": 0, "fin": -5, "comp": 0}, "Leczenie tym co zostało (bez planu)": {"pat": -30, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Pożyczanie leków od sąsiednich jednostek": {"pat": +20, "avl": 0, "fin": -15, "comp": +5}, "Czekanie na terminowe dostawy": {"pat": -20, "avl": 0, "fin": 0, "comp": 0}}}
            }
         },
         4: {
            "title": "FAZA 4: SABOTAŻ KOMÓR KRWI",
            "desc": "Termostaty w chłodziarkach z krwią zostały przestawione na +25 stopni. Krew jest do wyrzucenia. Planowane operacje muszą zostać odwołane.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Montaż niezależnych czujników fizycznych": {"pat": +10, "avl": 0, "fin": -10, "comp": +5}, "Wiara w logi systemowe (które kłamią)": {"pat": -30, "avl": 0, "fin": 0, "comp": -15}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Całkowite wstrzymanie operacji krwiopochodnych": {"pat": +10, "avl": -30, "fin": -10, "comp": +10}, "Próba użycia krwi bez weryfikacji temperatury": {"pat": -100, "avl": 0, "fin": 0, "comp": -50}}},
                "Dir": {"label": "ZARZĄD", "options": {"Pilna prośba do RCKiK o nowe zasoby": {"pat": +20, "avl": 0, "fin": -10, "comp": +5}, "Zatajenie błędu termostatów": {"pat": -50, "avl": 0, "fin": 0, "comp": -40}}}
            }
         },
         5: {
            "title": "FAZA 5: POST-MORTEM",
            "desc": "IoT okazało się piętą achillesową. Wymagana całkowita zmiana architektury IoT.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Fizyczna separacja sieci medycznej od innych": {"pat": 0, "avl": +25, "fin": -20, "comp": +15}, "Zakup droższego Firewalla": {"pat": 0, "avl": -10, "fin": -5, "comp": -5}}},
                "Med": {"label": "EDUKACJA", "options": {"Szkolenie techniczne personelu z obsługi wind/pomp": {"pat": +10, "avl": 0, "fin": -5, "comp": 0}, "Brak zmian": {"pat": -10, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Pozew przeciwko producentowi sprzętu IoT": {"pat": 0, "avl": 0, "fin": +15, "comp": +10}, "Brak działań prawnych": {"pat": 0, "avl": 0, "fin": -10, "comp": -10}}}
            }
         }
    },
    "Wariant E: Phishing Masowy i Socjotechnika": {
         1: {
            "title": "FAZA 1: MAILE OD 'DYREKCJI'",
            "desc": "Cały personel otrzymuje maile z 'nowym regulaminem premii'. Załącznik zawiera złośliwe oprogramowanie typu Stealer. 60% pielęgniarek otwiera plik.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Blokada kont mailowych wszystkich użytkowników": {"pat": 0, "avl": -20, "fin": 0, "comp": +10}, "Próba usuwania maili z serwera (Ex Post)": {"pat": -5, "avl": 0, "fin": 0, "comp": -10}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Ostrzeżenie personelu na grupach prywatnych": {"pat": +10, "avl": 0, "fin": 0, "comp": 0}, "Czekanie na oficjalny komunikat": {"pat": -15, "avl": 0, "fin": 0, "comp": 0}}},
                "Dir": {"label": "ZARZĄD", "options": {"Poinformowanie, że to nie był mail od dyrekcji": {"pat": +5, "avl": 0, "fin": 0, "comp": +5}, "Milczenie (wstyd z powodu kradzieży tożsamości)": {"pat": -10, "avl": 0, "fin": 0, "comp": -15}}}
            }
         },
         2: {
            "title": "FAZA 2: KRADZIEŻ TOŻSAMOŚCI ŚWIADCZĄCYCH",
            "desc": "Hakerzy logują się na portale rozliczeniowe z NFZ. Próbują przekierować płatności za procedury medyczne na swoje konta.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Zmiana haseł do wszystkich systemów zewnętrznych": {"pat": 0, "avl": -5, "fin": 0, "comp": +15}, "Ignorowanie (systemy NFZ są 'bezpieczne')": {"pat": 0, "avl": 0, "fin": -50, "comp": -20}}},
                "Med": {"label": "BIURO", "options": {"Manualna weryfikacja faktur": {"pat": 0, "avl": 0, "fin": +10, "comp": +10}, "Automatyczne przesyłanie danych": {"pat": 0, "avl": 0, "fin": -30, "comp": -10}}},
                "Dir": {"label": "ZARZĄD", "options": {"Kontakt z bankiem i NFZ": {"pat": 0, "avl": 0, "fin": +20, "comp": +10}, "Ukrywanie incydentu przed NFZ": {"pat": 0, "avl": 0, "fin": -20, "comp": -40}}}
            }
         },
         3: {
            "title": "FAZA 3: TELEFON OD 'INFORMATYKA'",
            "desc": "Pacjenci zaczynają dzwonić z pytaniem, dlaczego dostali SMSy z instrukcją logowania do portalu pacjenta w celu wpłaty za leki. Ktoś personifikuje dział wsparcia.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Wyłączenie portalu pacjenta": {"pat": 0, "avl": -15, "fin": 0, "comp": +5}, "Monitorowanie nieudanych prób logowań": {"pat": -5, "avl": 0, "fin": 0, "comp": -10}}},
                "Med": {"label": "OBŁSUGA PACJENTA", "options": {"SMS o treści OSTRZEŻENIE do pacjentów": {"pat": +15, "avl": 0, "fin": 0, "comp": +15}, "Brak powiadomienia (koszty SMS masowego)": {"pat": -30, "avl": 0, "fin": 0, "comp": -20}}},
                "Dir": {"label": "ZARZĄD", "options": {"Zgłoszenie masowej socjotechniki do mediów": {"pat": +5, "avl": 0, "fin": 0, "comp": +10}, "Blokowanie infolinii": {"pat": -10, "avl": -10, "fin": 0, "comp": -10}}}
            }
         },
         4: {
            "title": "FAZA 4: SFAŁSZOWANE DYREKTYWY MEDYCZNE",
            "desc": "W systemie pojawiają się sfałszowane notatki o przeniesieniu pacjentów na inne oddziały. Sanepid dostaje fejkowe zgłoszenie o zarazie w szpitalu.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Audyt logów edycji dokumentacji": {"pat": 0, "avl": 0, "fin": -5, "comp": +20}, "Restart systemu": {"pat": -5, "avl": -5, "fin": 0, "comp": -5}}},
                "Med": {"label": "PION MEDYCZNY", "options": {"Potwierdzanie telefoniczne każdej notatki": {"pat": +10, "avl": -20, "fin": -5, "comp": +5}, "Realizacja notatek (chaos logistyczny)": {"pat": -40, "avl": 0, "fin": 0, "comp": -10}}},
                "Dir": {"label": "ZARZĄD", "options": {"Zaproszenie Sanepidu na fizyczną wizję lokalną": {"pat": 0, "avl": 0, "fin": -5, "comp": +20}, "Zaprzeczanie przez telefon": {"pat": 0, "avl": 0, "fin": 0, "comp": -10}}}
            }
         },
         5: {
            "title": "FAZA 5: POST-MORTEM",
            "desc": "Ludzie okazali się najsłabszym ogniwem. Pora na systemy techniczne ograniczające błędy.",
            "questions": {
                "IT": {"label": "OPERACJE IT", "options": {"Wdrożenie MFA (Multi Factor Authentication)": {"pat": 0, "avl": 0, "fin": -10, "comp": +40}, "Zabranie ludziom dostępu do maila": {"pat": 0, "avl": -40, "fin": 0, "comp": -10}}},
                "Med": {"label": "EDUKACJA", "options": {"Cykliczne testowe phishingi dla personelu": {"pat": +15, "avl": 0, "fin": -5, "comp": +10}, "Jedna prezentacja na zebraniu": {"pat": -10, "avl": 0, "fin": 0, "comp": -5}}},
                "Dir": {"label": "ZARZĄD", "options": {"Nagroda dla pielęgniarki, która zgłosiła maila": {"pat": +10, "avl": 0, "fin": -5, "comp": +5}, "Ukaranie finansowe tych co kliknęli": {"pat": -20, "avl": 0, "fin": +10, "comp": -30}}}
            }
         }
    }
}

# --- VERDICT ENGINE ---
def get_verdict(p, a, f, c):
    total = p + a + f + c
    if p < 50:
        return "❌ KATASTROFA MEDYCZNA: Twoje decyzje doprowadziły do tragicznych błędów lekarskich i utraty życia pacjentów. Szpital zostaje zamknięty przez prokuraturę.", "ERROR_RED"
    if c < 40:
        return "⚖️ WYROK SĄDOWY: Całkowite zlekceważenie procedur prawnych i RODO skutkuje rekordowymi karami finansowymi, których szpital nie przeżyje. Zarząd trafia do aresztu.", "ERROR_RED"
    if a < 40:
        return "🔌 PARALIŻ CYFROWY: Systemy szpitala zostały trwale uszkodzone. Placówka nie potrafi wrócić do pracy przez miesiące. Pacjenci masowo uciekają do konkurencji.", "WARNING_YELLOW"
    if f < 40:
        return "💸 BANKRUCTWO: Szpital opanował atak, ale koszty incident response i kar zjadły cały budżet. Brak środków na pensje i leki zmusza do licytacji komorniczej.", "WARNING_YELLOW"
    
    if total > 500:
        return "🏆 MISTRZOSTWO REAGOWANIA: Wykazałeś się zimną krwią i doskonałym balansem między etyką a technologią. Szpital stał się wzorcem cyberbezpieczeństwa w regionie.", "SUCCESS_GREEN"
    if total > 400:
        return "✅ SKUTECZNA DEFENSYWA: Atak został odparty przy minimalnych stratach. Placówka funkcjonuje, a wyciągnięte wnioski pozwolą na uniknięcie błędów w przyszłości.", "SUCCESS_GREEN"
    
    return "🟧 PRZETRWANIE: Szpital przetrwał, ale blizny pozostaną na lata. Zaufanie pacjentów zostało nadszarpnięte, a budżet jest mocno naciągnięty.", "NEUTRAL_BLUE"

# --- HELPERS ---
def calculate_team_metrics(team_name):
    p, a, f, c = 100, 100, 100, 100
    team_data = state["teams"].get(team_name, {})
    scenario_data = SCENARIOS[state["active_scenario_key"]]
    
    for r_num in range(1, state["round"] + 1):
        r_decisions = team_data.get("decisions", {}).get(r_num, {})
        if r_num in scenario_data:
            for role, choice in r_decisions.items():
                if choice in scenario_data[r_num]["questions"][role]["options"]:
                    impact = scenario_data[r_num]["questions"][role]["options"][choice]
                    p += impact["pat"]
                    a += impact["avl"]
                    f += impact["fin"]
                    c += impact["comp"]
    
    return [max(0, min(150, m)) for m in [p, a, f, c]]

def render_kpi(label, value, color="var(--accent-cyan)"):
    pct = int((value/150)*100)
    current_color = "var(--accent-red)" if value < 50 else color
    
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-header">
                <span>{label}</span>
                <span class="kpi-value">{pct}%</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {pct}%; background: {current_color}; box-shadow: 0 0 8px {current_color}44;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- VIEWS ---

def login_view():
    st.markdown("""
        <div class="command-header">
            <div class="brand">
                <div class="brand-title">CyberGra Decyzyjna - Atak na Szpital // COMMAND</div>
            </div>
            <div class="status-badge" style="background: rgba(245, 158, 11, 0.1); color: var(--accent-yellow); border-color: rgba(245, 158, 11, 0.3);">Czekam na autoryzację</div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        with st.container():
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-label'>TERMINAL LOGIN</div>", unsafe_allow_html=True)
            team_id = st.text_input("KRYPTONIM JEDNOSTKI:", placeholder="np. ALPHA-1")
            
            if st.button("AUTORYZUJ DOSTĘP", use_container_width=True):
                if team_id:
                    if team_id not in state["teams"]:
                        state["teams"][team_id] = {"decisions": {}, "ready": False}
                    st.session_state["team_name"] = team_id
                    st.session_state["role"] = "team"
                    st.rerun()
                else:
                    st.warning("Podaj identyfikator zespołu.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔐 TRYB ADMINISTRATORA"):
                pwd = st.text_input("ROOT KEY:", type="password")
                if st.button("LOG AS ADMIN"):
                    if pwd == "admin":
                        st.session_state["role"] = "admin"
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

def admin_view():
    st.markdown("""
        <div class="command-header">
            <div class="brand">
                <div class="brand-title">CyberGra Decyzyjna - Atak na Szpital // COMMAND // ROOT</div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div class="status-badge" style="background: rgba(34, 197, 94, 0.1); color: var(--accent-green); border-color: rgba(34, 197, 94, 0.3);">SYSTEM READY</div>
                <div style="cursor:pointer; font-size: 0.8rem; color: var(--text-secondary);" onclick="window.location.reload();">[ EXIT SESSION ]</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>KONTROLA FAZ GRY</div>", unsafe_allow_html=True)
        
        if state["round"] == 0:
            scenario_choice = st.selectbox("Wybierz scenariusz:", list(SCENARIOS.keys()))
            state["active_scenario_key"] = scenario_choice
            
        st.write(f"### Obecna faza: **{state['round']}**")
        
        rounds_total = len(SCENARIOS[state["active_scenario_key"]])
        if state["round"] < rounds_total:
            if st.button("⏩ AKTYWUJ NASTĘPNĄ FAZĘ", use_container_width=True):
                state["round"] += 1
                for t in state["teams"]: state["teams"][t]["ready"] = False
                st.rerun()
        elif state["round"] == rounds_total:
            if st.button("📊 GENERUJ RAPORTY KOŃCOWE", use_container_width=True):
                state["round"] += 1
                st.rerun()
        else:
            if st.button("🔄 ZAKOŃCZ SESJĘ I RESETUJ", use_container_width=True):
                state["round"] = 0
                state["teams"] = {}
                state["logs"] = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>MONITOR TRANSMISJI ZESPOŁÓW</div>", unsafe_allow_html=True)
        if not state["teams"]:
            st.info("Brak aktywnych połączeń.")
        else:
            for t_name, t_data in state["teams"].items():
                status_color = "#10b981" if t_data["ready"] else "#facc15"
                status_text = "READY" if t_data["ready"] else "COMPUTING..."
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; margin-bottom: 0.5rem; align-items: center;">
                        <span style="font-weight: 700; color: #f8fafc;">{t_name}</span>
                        <span style="color: {status_color}; font-size: 0.75rem; font-weight: 800;">{status_text}</span>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📲 GENERATOR TERMINALI (QR)"):
            game_url = st.text_input("Link dla terminali mobilnych:", placeholder="https://...")
            if game_url:
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={game_url}"
                st.image(qr_url, caption="Zeskanuj, aby połączyć jednostkę")
    if state["teams"]:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>RANKING GLOBALNY JEDNOSTEK</div>", unsafe_allow_html=True)
        scores = []
        for t in state["teams"]:
            p, a, f, c = calculate_team_metrics(t)
            scores.append({"JEDNOSTKA": t, "SUMA": p+a+f+c, "PACJENCI": p, "SYSTEMY": a, "FINANSE": f, "ZGODNOŚĆ": c})
        st.dataframe(pd.DataFrame(scores).sort_values(by="SUMA", ascending=False), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def team_view():
    team_name = st.session_state.get("team_name")
    if not team_name:
        st.session_state["role"] = None
        st.rerun()
        return

    # METRICS
    p, a, f, c = calculate_team_metrics(team_name)

    # HEADER
    st.markdown(f"""
        <div class="command-header">
            <div class="brand">
                <div class="brand-title">CyberGra Decyzyjna - Atak na Szpital // COMMAND</div>
                <div style="font-family: var(--font-mono); font-size: 0.85rem; color: var(--text-secondary); margin-left: 20px;">
                    SESSION_ID: <span style="color: var(--accent-cyan)">{team_name.upper()}</span>
                </div>
            </div>
            <div class="status-badge">Critical Incident: APT-VAR-C</div>
        </div>
    """, unsafe_allow_html=True)

    # MAIN CONTENT 3-COLUMN
    left, center, right = st.columns([1, 2.2, 0.9], gap="medium")

    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>SYSTEM METRICS</div>", unsafe_allow_html=True)
        render_kpi("DOBROSTAN PACJENTÓW", p, "#f43f5e")
        render_kpi("DOSTĘPNOŚĆ SYSTEMÓW", a, "#06b6d4")
        render_kpi("REZERWY FINANSOWE", f, "#10b981")
        render_kpi("ZGODNOŚĆ PRAWNA", c, "#facc15")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>COMMUNICATION LOG</div>", unsafe_allow_html=True)
        now = datetime.datetime.now().strftime("%H:%M:%S")
        if state["round"] == 0:
            st.markdown(f"<div class='log-item'><span class='log-ts'>[{now}]</span> <span class='log-act'>SYS</span>: <span class='log-msg'>Awaiting scenario trigger...</span></div>", unsafe_allow_html=True)
        else:
            for r_idx in range(1, state["round"]+1):
                st.markdown(f"<div class='log-item'><span class='log-ts'>[T-{r_idx:02d}]</span> <span class='log-act'>PHASE_{r_idx}</span>: <span class='log-msg'>Report sync complete.</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='log-item'><span class='log-ts'>[{now}]</span> <span class='log-act'>UPT</span>: <span class='log-msg'>Receiving situational update.</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with center:
        if state["round"] == 0:
            st.markdown("""
                <div class='panel' style='text-align: center; padding: 5rem 2rem;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>📡</div>
                    <h2 style='color: #f8fafc;'>NASŁUCH PASYWNY</h2>
                    <p style='color: #64748b;'>Sieć szpitalna działa w trybie nominalnym. <br>Brak aktywnych wektorów ataku. Oczekuj na sygnał z Dowództwa.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("SYNCHRONIZUJ TERMINAL 🔄", use_container_width=True): st.rerun()
            
        elif state["round"] <= len(SCENARIOS[state["active_scenario_key"]]):
            r_num = state["round"]
            scenario = SCENARIOS[state["active_scenario_key"]][r_num]
            
            st.markdown(f"""
                <div class='scenario-header'>
                    <div class='scenario-id'>SITUATION_REPORT 0x{r_num:02x}</div>
                    <div class='scenario-title'>{scenario['title']}</div>
                </div>
                <div class='panel' style='margin-bottom: 1.5rem;'>
                    <div class='scenario-desc'>{scenario['desc']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if not state["teams"][team_name]["ready"]:
                st.markdown("<div class='panel-label'>ROZKAZY OPERACYJNE</div>", unsafe_allow_html=True)
                with st.form(f"team_form_{r_num}"):
                    decisions = {}
                    for role, q_data in scenario["questions"].items():
                        st.markdown(f"<div style='margin-bottom: 0.5rem; color: #94a3b8; font-size: 0.8rem; font-weight: 700;'>{q_data['label']}</div>", unsafe_allow_html=True)
                        decisions[role] = st.radio(f"Select_{role}", list(q_data["options"].keys()), label_visibility="collapsed")
                        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                    
                    if st.form_submit_button("WDROŻYJ STRATEGIĘ 💾", use_container_width=True):
                        if "decisions" not in state["teams"][team_name]: state["teams"][team_name]["decisions"] = {}
                        state["teams"][team_name]["decisions"][r_num] = decisions
                        state["teams"][team_name]["ready"] = True
                        st.rerun()
            else:
                st.markdown(f"""
                    <div class='panel' style='background: rgba(6, 182, 212, 0.05); border-color: var(--accent-cyan);'>
                        <h4 style='color: var(--accent-cyan);'>✓ TRANSMISJA PRZYJĘTA</h4>
                        <p style='color: var(--text-secondary); font-size: 0.9rem;'>
                            Twoje rozkazy zostały zakolejkowane. <br>
                            Status: <b>Oczekiwanie na analizę Dowództwa...</b>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("ODŚWIEŻ DANE SIECIOWE", use_container_width=True): st.rerun()
        else:
            st.markdown("<div class='panel' style='text-align: center; border-color: var(--accent-cyan);'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: var(--text-primary); margin-top:0;'>SYMULACJA ZAKOŃCZONA</h2>", unsafe_allow_html=True)
            
            p, a, f, c = calculate_team_metrics(team_name)
            verdict_text, _ = get_verdict(p, a, f, c)
            
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 6px; padding: 20px; margin: 20px 0; text-align: left;">
                    <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-cyan); margin-bottom: 10px;">RAPORT KOŃCOWY: {team_name.upper()}</div>
                    <div style="font-size: 1.1rem; line-height: 1.6; color: var(--text-primary);">{verdict_text}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='panel-label'>RANKING OPERACYJNY</div>", unsafe_allow_html=True)
            lb = []
            for t in state["teams"]:
                mp, ma, mf, mc = calculate_team_metrics(t)
                total = mp + ma + mf + mc
                lb.append({"TEAM": t, "SCORE": total, "PACJENCI": mp, "SYSTEMY": ma, "FINANSE": mf, "ZGODNOŚĆ": mc})
            
            df = pd.DataFrame(lb).sort_values(by="SCORE", ascending=False).reset_index(drop=True)
            df.index += 1
            st.dataframe(df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-label'>TERMINAL STATUS</div>", unsafe_allow_html=True)
        
        status_icon = "🔵" if state["round"] == 0 else ("🟢" if state["teams"][team_name]["ready"] else "🟡")
        status_txt = "STANDBY" if state["round"] == 0 else ("ENCRYPTED" if state["teams"][team_name]["ready"] else "WAITING")
        
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem 0;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{status_icon}</div>
                <div style="font-weight: 800; color: #f8fafc; font-size: 1.25rem;">{status_txt}</div>
                <div style="color: #64748b; font-size:0.8rem; margin-top: 0.5rem;">Connection: Secure AES-256</div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1rem; font-size: 0.7rem; color: #475569;">
                HOST: ais-node-04<br>
                UI_VERSION: 2.0.4-PRO<br>
                LAST_SYNC: {now}
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- ROUTER ---
if "role" not in st.session_state:
    login_view()
elif st.session_state["role"] == "admin":
    admin_view()
elif st.session_state["role"] == "team":
    team_view()
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

# Pobierz plik "logo.png" w tym samym folderze co kod
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
        /* Miejsce na dolną belkę z logo */
        padding-bottom: 120px !important; 
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
        background-color: #060b13;
        border-top: 2px solid #00f0ff;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.5);
    }
    .footer-logo {
        width: 100%;
        height: auto;
        max-height: 100px;
        object-fit: contain; /* lub cover, jeśli chcesz wypełnić krawędzie */
        opacity: 0.90;
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
else:
    st.markdown("""
        <div class="custom-footer" style="height: 60px;">
            <span style="font-family: monospace; color: #64748b; letter-spacing: 2px;">SYSTEM // SECURE CONNECTION ESTABLISHED</span>
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
    
    # Auto-Kick (KeyError Fix)
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
