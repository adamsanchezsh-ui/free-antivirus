# 🛡️ FreeAV

Zdarma open-source antivirus s hezkým webovým rozhraním (mobil i PC). Skenuje pomocí [ClamAV](https://www.clamav.net/), nalezený virus **dá do karantény nebo rovnou smaže** a řekne, **z jaké stránky byl soubor stažen** (pokud to systém zaznamenal).

## ⬇️ Stáhnout

**[Stáhnout ZIP](https://github.com/adamsanchezsh-ui/free-antivirus/archive/refs/heads/main.zip)** a rozbalit.

## Spuštění

1. Nainstaluj **Python 3.8+** a **ClamAV**:
   - Windows: Python z python.org (zaškrtni *Add to PATH*) a ClamAV z clamav.net (přidej do `PATH`)
   - Linux: `sudo apt install clamav`
   - macOS: `brew install clamav`
2. Spusť launcher:
   - **Windows:** dvojklik na `start.bat`
   - **Linux/macOS:** `sh start.sh`
3. Otevře se prohlížeč na `http://127.0.0.1:8765`.

Ručně: `freshclam` a pak `python app.py`. Žádné další knihovny nejsou potřeba.

## Funkce

- Skenování složky nebo souboru
- Karanténa (bezpečné) nebo okamžité smazání
- Zobrazení původu souboru (stránka, odkud byl stažen)
- Aktualizace virové databáze jedním tlačítkem
- Responzivní design pro telefon i počítač

## Bezpečnost a omezení

- Server poslouchá jen na `127.0.0.1` a odmítá požadavky z cizích webů.
- Žádný antivirus nechytí všechno. FreeAV je jen tak dobrý jako databáze ClamAV.
- Původ souboru jde zjistit jen tehdy, když ho systém při stahování zaznamenal. Nezjistí odesílatele e-mailu ani útočníka.
- Pozor na falešné poplachy: doporučeno nejdřív karanténa, smazání je nevratné.
- Aplikace běží na počítači. Na telefonu se jen zobrazí její rozhraní (např. v síti), samostatně tam neskénuje.

## Licence

MIT
