import streamlit as st
import pandas as pd
import datetime
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="HOSPITAL OS // COMMAND CENTER",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

# --- PROFESSIONAL POLISH CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
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
    }

    /* Global Overrides */
    .stApp {
        background-color: var(--bg-color) !important;
        color: var(--text-primary);
        font-family: var(--font-sans);
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Layout Containers */
    .command-header {
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
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-title {
        font-family: var(--font-mono);
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 0.1em;
        color: var(--accent-cyan);
        text-transform: uppercase;
    }

    .status-badge {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid var(--accent-red);
        color: var(--accent-red);
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* Professional Panels */
    .panel {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 16px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .panel-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: block;
    }

    /* KPI Display */
    .kpi-container {
        margin-bottom: 14px;
    }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        margin-bottom: 6px;
        font-weight: 500;
    }

    .kpi-value {
        font-family: var(--font-mono);
        color: var(--text-primary);
    }

    .progress-bar-bg {
        background: var(--bg-color);
        height: 4px;
        border-radius: 2px;
        overflow: hidden;
    }

    .progress-bar-fill {
        height: 100%;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        background: var(--accent-cyan);
        box-shadow: 0 0 8px rgba(6, 182, 212, 0.4);
    }

    /* Situational Room */
    .scenario-header {
        background: linear-gradient(135deg, var(--panel-bg) 0%, var(--bg-color) 100%);
        border-left: 4px solid var(--accent-red);
        border-radius: 0 6px 6px 0;
        padding: 20px;
        margin-bottom: 20px;
    }

    .scenario-id {
        font-family: var(--font-mono);
        color: var(--accent-cyan);
        font-size: 0.75rem;
        margin-bottom: 4px;
    }

    .scenario-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text-primary);
    }

    .scenario-desc {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-top: 12px;
        font-size: 0.95rem;
    }

    /* Forms and Buttons */
    .stButton > button {
        background: var(--accent-cyan) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 4px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 14px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.3) !important;
        transform: none !important;
    }

    .stRadio label {
        background: #2d3748 !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        border-radius: 4px !important;
        font-size: 0.85rem !important;
        margin-bottom: 8px !important;
    }

    .stRadio div[role="radiogroup"] > label:hover {
        border-color: var(--accent-cyan) !important;
        background: rgba(6, 182, 212, 0.05) !important;
    }

    /* Terminal Logs */
    .log-item {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        padding: 4px 0 4px 8px;
        border-left: 2px solid var(--border-color);
        margin-bottom: 8px;
    }
    .log-ts { color: var(--accent-yellow); }
    .log-act { color: var(--accent-cyan); font-weight: 600; margin-left: 4px; }
    .log-msg { color: var(--text-secondary); display: block; margin-top: 2px; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg-color); }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 2px; }
    </style>
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
                "Dir": {"label": "SZTAB KRYZYSOWY", "options": {"Transparentne przyznanie się do naruszenia": {"pat": +5, "avl": 0, "fin": -15, "comp": +25}, "Agresywna kampania prawna i zaprzeczanie": {"pat": -5, "avl": 0, "fin": +5, "comp": -30}}}
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
    # Critical state color - use CSS variable for consistency
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
                <div class="brand-title">HOSPITAL OS // COMMAND</div>
            </div>
            <div class="status-badge" style="background: rgba(245, 158, 11, 0.1); color: var(--accent-yellow); border-color: rgba(245, 158, 11, 0.3);">WAITING FOR AUTH</div>
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
                <div class="brand-title">HOSPITAL OS // COMMAND // ROOT</div>
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
        st.markdown("<div class='panel-label'>KONTROLA FAZ</div>", unsafe_allow_html=True)
        
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
        else:
            if st.button("🔄 ZAMKNIJ I RESETUJ", use_container_width=True):
                state["round"] = 0
                state["teams"] = {}
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
                <div class="brand-title">HOSPITAL OS // COMMAND</div>
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
                st.markdown("""
                    <div class='panel' style='background: rgba(16, 185, 129, 0.05); border-color: rgba(16, 185, 129, 0.2);'>
                        <h4 style='color: #10b981;'>✓ TRANSMISJA PRZYJĘTA</h4>
                        <p style='color: #94a3b8; font-size: 0.9rem;'>Analiza strategiczna w toku. Twoje rozkazy zostały zakolejkowane w systemie centralnym.</p>
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
