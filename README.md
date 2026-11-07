# 🛡️ FreeAV

Zdarma open-source antivirus s hezkým webovým rozhraním (mobil i PC). Skenuje pomocí [ClamAV](https://www.clamav.net/), nalezený virus **dá do karantény nebo rovnou smaže**.

## Instalace

1. Nainstaluj **Python 3.8+** a **ClamAV**:
   - Linux: `sudo apt install clamav` (pak `sudo freshclam`)
   - macOS: `brew install clamav`
   - Windows: stáhni instalátor z clamav.net a přidej složku ClamAV do `PATH`
2. Stáhni databázi virů: `freshclam`
3. Spusť:
   ```
   python app.py
   ```
4. Otevři **http://127.0.0.1:8765** v prohlížeči.

Žádné další knihovny nejsou potřeba.

## Funkce

- Skenování složky nebo souboru
- Karanténa (bezpečné) nebo okamžité smazání
- Aktualizace virové databáze jedním tlačítkem
- Responzivní design, funguje na telefonu i počítači

## Bezpečnost a omezení

- Server poslouchá jen na `127.0.0.1` a odmítá požadavky z cizích webů.
- Žádný antivirus nechytí všechno. FreeAV je jen tak dobrý jako databáze ClamAV, nenahrazuje rozum při stahování souborů.
- Pozor na falešné poplachy: při smazání zkontroluj, co se maže. Doporučeno nejdřív karanténa.

## Licence

MIT
