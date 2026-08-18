# Futmondo Dashboard · Rates 2026–2027

Incluye dos apps Streamlit separadas:

- `private_app.py`: dashboard económico privado.
- `public_app.py`: dashboard público de puntos y estadísticas.

## Datos iniciales
- Snapshot económico: 18/08/2026
- 11 participantes
- Todos los equipos están todavía en 0 puntos.
- El índice de liquidez es relativo y se basa en el gasto neto visible reconstruido de las capturas del 9–18/08/2026.

## Ejecutar en local
```bash
pip install -r requirements.txt
streamlit run private_app.py
```

Para el público:
```bash
streamlit run public_app.py
```

## Publicar online
Sube esta carpeta a un repositorio y despliega `public_app.py` y `private_app.py` como dos apps separadas en Streamlit Community Cloud.

## Actualización
Cuando haya nuevas capturas:
- `data/team_economy.csv`: nuevos snapshots económicos.
- `data/scores.csv`: añadir una fila por equipo y jornada.
