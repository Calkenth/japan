# Japonia 2026

Plan wyjazdu do Japonii, 1–15 listopada 2026: mapa trasy, plan dzień po dniu, noclegi, rozliczenie kosztów i sprawy do załatwienia przed wyjazdem. Treść pochodzi z arkusza „JAPAN!”.

Strona po włączeniu GitHub Pages: https://calkenth.github.io/japan/

## Co jest w repozytorium

- `index.html` – cała strona w jednym pliku: style, dane i kod. Działa też otwarta prosto z dysku albo wysłana jako plik.
- `tools/map-data/generate.py` – generator linii brzegowej i jezior do mapy, z danych Natural Earth 1:10m.

## Jak zmieniać treść

Dane są w obiekcie `DATA` na początku głównego skryptu w `index.html`:

- `days` – plan dzień po dniu: godziny, opisy i miejsca, które mapa pokazuje po kliknięciu dnia,
- `hotels` – noclegi z godzinami zameldowania i wymeldowania,
- `money` – pozycje rozliczenia; sumy, podział na osoby i kwota przelewu liczą się same,
- `esim` i `insurance` – oferty z zakładki „Przed wyjazdem”; `eur` to kurs euro do przeliczeń,
- `places` i `views` – punkty na mapie i widoki z przycisków nad mapą.

Przebieg tras na mapie jest w tablicy `ROUTES` tuż pod danymi.

## Mapa

Linia brzegowa jest osadzona w `window.__MAP__` w pierwszym skrypcie. Trzeba ją przeliczyć tylko wtedy, gdy zmienia się zasięg mapy:

```
pip install shapely
python3 tools/map-data/generate.py > map.json
```

Wynik wklej w miejsce obiektu po `window.__MAP__ =`.

## GitHub Pages

Settings → Pages → Source: „Deploy from a branch”, gałąź `main`, katalog `/ (root)`.
