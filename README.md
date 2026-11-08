# Nyhetsankaret

Hubben för det dagliga nyhetsintaget. En daglig nyhetssammanfattning inom teknik, hållbarhet, inrikes- och utrikespolitik.
Varje nyhet bygger på minst tre oberoende källor där det går och får en källkritisk bedömning.
Rapporterna sammanställs varje morgon av Claude och publiceras här via GitHub Pages.

## Struktur

- `index.html` – själva sidan (ingen byggprocess, inga beroenden)
- `reports/ÅÅÅÅ-MM-DD.json` – en rapport per dag
- `reports/index.json` – lista över alla dagar, nyast först
- `scripts/add_report.py` – kontrollerar en ny rapport och uppdaterar listan

## Lägga till en rapport

```
python3 scripts/add_report.py rapport.json
git add reports && git commit -m "Rapport ÅÅÅÅ-MM-DD" && git push
```

## Som app i mobilen

Öppna sidan i Safari (iPhone) eller Chrome (Android) och välj **Lägg till på hemskärmen**.
