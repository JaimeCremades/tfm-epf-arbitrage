import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Carga del dataset ─────────────────────────────────────────────────────────
df = pd.read_csv('dataset_final_clean.csv')
df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
df['date'] = df['datetime'].dt.date

# ── Extracción del día representativo (21 octubre 2023) ───────────────────────
dia = pd.to_datetime('2023-10-21').date()
day = df[df['date'] == dia].sort_values('hour').reset_index(drop=True)

horas        = day['hour'].tolist()
precio       = day['price_spain'].tolist()
demanda_real = (day['Real'] / 1000).tolist()  # MW -> GW

# ── Simulación de la estrategia de arbitraje ─────────────────────────────────
UMBRAL_CARGA    = day['price_spain'].quantile(0.25)
UMBRAL_DESCARGA = day['price_spain'].quantile(0.75)
POTENCIA        = (day['Real'].max() - day['Real'].min()) * 0.15 / 1000

demanda_arbitraje = demanda_real.copy()
for i, p in enumerate(precio):
    if p <= UMBRAL_CARGA:
        demanda_arbitraje[i] += POTENCIA
    elif p >= UMBRAL_DESCARGA:
        demanda_arbitraje[i] -= POTENCIA

# ── Figura ────────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(13, 6))
ax2 = ax1.twinx()

# Zonas de carga y descarga
for i, p in enumerate(precio):
    if p <= UMBRAL_CARGA:
        ax1.axvspan(i - 0.5, i + 0.5, color='#B5D4F4', alpha=0.5, zorder=0)
    elif p >= UMBRAL_DESCARGA:
        ax1.axvspan(i - 0.5, i + 0.5, color='#9FE1CB', alpha=0.5, zorder=0)

# Curvas
l1, = ax2.plot(horas, precio, color='#378ADD', linewidth=2.5,
               label='Precio eléctrico (€/MWh)', zorder=3)
l2, = ax1.plot(horas, demanda_real, color='#888780', linewidth=2,
               linestyle='--', label='Demanda sin gestión (GW)', zorder=2)
l3, = ax1.plot(horas, demanda_arbitraje, color='#1D9E75', linewidth=2.5,
               label='Demanda con arbitraje (GW)', zorder=2)

# Ejes
ax1.set_xlabel('Hora del día', fontsize=12)
ax1.set_ylabel('Demanda (GW)', fontsize=12, color='#444441')
ax2.set_ylabel('Precio eléctrico (€/MWh)', fontsize=12, color='#378ADD')
ax1.tick_params(axis='y', labelcolor='#444441')
ax2.tick_params(axis='y', labelcolor='#378ADD')
ax1.set_xticks(horas)
ax1.set_xticklabels([f'{h}h' for h in horas], fontsize=9)

# Anotaciones dinámicas
hora_pico  = precio.index(max(precio))
hora_valle = precio.index(min(precio))

ax2.annotate('Pico de precio\n(descarga batería)',
             xy=(hora_pico, max(precio)),
             xytext=(hora_pico - 3.5, max(precio) * 0.88),
             arrowprops=dict(arrowstyle='->', color='#1D9E75', lw=1.5),
             fontsize=9, color='#1D9E75')

ax2.annotate('Valle de precio\n(carga batería)',
             xy=(hora_valle, min(precio)),
             xytext=(hora_valle + 1.5, min(precio) + max(precio) * 0.2),
             arrowprops=dict(arrowstyle='->', color='#378ADD', lw=1.5),
             fontsize=9, color='#378ADD')

# Leyenda
patch_carga    = mpatches.Patch(color='#B5D4F4', alpha=0.8,
                                label=f'Carga batería (precio ≤ {UMBRAL_CARGA:.0f} €/MWh)')
patch_descarga = mpatches.Patch(color='#9FE1CB', alpha=0.8,
                                label=f'Descarga batería (precio ≥ {UMBRAL_DESCARGA:.0f} €/MWh)')
ax1.legend(handles=[l1, l2, l3, patch_carga, patch_descarga],
           loc='upper left', fontsize=9, framealpha=0.9)

# Título y pie
ax1.set_title('Peak shaving y peak shifting mediante arbitraje energético\n'
              f'Mercado eléctrico español — 21 de Octubre de 2023',
              fontsize=13, pad=12)


plt.tight_layout()
plt.savefig('grafico_peak_shaving.png', dpi=200, bbox_inches='tight')
plt.show()
print("Gráfico guardado como grafico_peak_shaving.png")
