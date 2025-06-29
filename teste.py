import numpy as np
from connection import connect, get_state_reward

# --- Carregue a Q-table salva ---
Q = np.loadtxt("resultado.txt", delimiter=",")

actions = ["left", "right", "jump"]
port = 2037

# --- Conecte ao ambiente ---
s = connect(port)
if s == 0:
    exit()

test_episodes = 10
test_wins = 0

print("\nTestando agente treinado com epsilon = 0...")

for test in range(test_episodes):
    estado, _ = get_state_reward(s, "right")
    while estado[-2:] != "00":
        estado, _ = get_state_reward(s, "right")
    estado, _ = get_state_reward(s, "jump")
    state_idx = int(estado, 2)  # ou use sua função state_to_index(estado)
    done = False
    steps = 0

    while not done and steps < 100:
        action_idx = np.argmax(Q[state_idx])  # Sempre a melhor ação
        action_str = actions[action_idx]
        estado, recompensa = get_state_reward(s, action_str)
        state_idx = int(estado, 2)  # ou use sua função state_to_index(estado)
        steps += 1

        if recompensa == -1:  # Vitória
            test_wins += 1
            done = True
        elif recompensa == -14:  # Morte
            done = True

    print(f"Episódio de teste {test+1}: {'Vitória' if recompensa == -1 else 'Fracasso'} em {steps} passos.")

print(f"\nTaxa de sucesso do agente treinado: {test_wins}/{test_episodes} ({(test_wins/test_episodes)*100:.1f}%)")
s.close()