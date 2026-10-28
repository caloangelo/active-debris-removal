import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parametri
h = 8000  # altezza di scala in metri (8 km)
E = 3/2   # valore di E
C = 0.002  # costante balistica (valore stimato)

D = 0.001  # costante incognita (valore iniziale)
H0 = 800000  # altezza iniziale in metri (800 km)

# Funzione che rappresenta l'EDO
def ode_system(t, H):
    if H < 0:  # per evitare valori negativi
        return 0
    dHdt = -C * (H**0.5) * np.exp(H/h) - D * (H**(3/2) + E * H**0.5)
    return dHdt

# Intervallo di tempo per la simulazione
t_span = (0, 25*365*24*60*60)  # tempo in secondi (fino a 30.000 secondi, circa 8 ore)
t_eval = np.linspace(t_span[0], t_span[1], 1)  # punti di valutazione

# Risoluzione dell'EDO
sol = solve_ivp(ode_system, t_span, [H0], t_eval=t_eval)

# Estrazione dei risultati
t_values = sol.t
H_values = sol.y[0]


# Visualizzazione dei risultati
# plt.figure(figsize=(12, 6))
# plt.plot(t_values / 3600, H_values / 1000, label=f'C = {C}, D = {D}', color='b')  # tempo in ore, H in km
# plt.title('Evoluzione dell\'altitudine H nel tempo')
# plt.xlabel('Tempo (ore)')
# plt.ylabel('Altitudine H (km)')
# plt.axhline(0, color='red', linestyle='--', label='H = 0 (Rientro)')
# plt.legend()
# plt.grid()
# plt.ylim(0, 800)  # Limiti per l'asse Y
# plt.xlim(0, 8)  # Limiti per l'asse X
# plt.show()
