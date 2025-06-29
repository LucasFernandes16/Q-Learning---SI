from connection import connect, get_state_reward
import numpy as np
import time

# --- Hiperparâmetros Ajustados ---
alpha = 0.1
gamma = 0.95 
epocas = 5000

# --- Estratégia de Exploração (Mantendo o decaimento lento) ---
epsilon_inicial = 0.7
epsilon_final = 0.1
taxa_decaimento = 0.9997

# --- Configuração Inicial ---
Q = np.zeros((96, 3))
actions = ["left", "right", "jump"]
port = 2037

def state_to_index(estado_binario):
        estado_int = int(estado_binario, 2)
        estado_formatado = format(estado_int, '07b')
        plataforma = int(estado_formatado[:5], 2)
        direcao = int(estado_formatado[5:], 2)
        return plataforma * 4 + direcao


def choose_action(state_idx, epsilon):
    """Escolhe uma ação usando a política epsilon-greedy."""
    if np.random.rand() < epsilon:
        return np.random.randint(3)
    else:
        return np.argmax(Q[state_idx])

# --- Conexão e Treinamento ---
s = connect(port)
if s == 0:
    exit()

visited_states = set()
epsilon = epsilon_inicial
total_wins = 0 # Novo: Contador de vitórias

for episode in range(epocas):

    estado, _ = get_state_reward(s, "right")  # Inicializa o estado
    while estado[-2:] != "00":  # "00" = Norte
        estado, _ = get_state_reward(s, "right")
    estado, _ = get_state_reward(s, "jump")
    state_idx = state_to_index(estado)
    
    done = False
    total_reward = 0
    steps = 0

    action_idx = choose_action(state_idx, epsilon)

    while not done:
        prev_state_idx = state_idx
        prev_action_idx = action_idx
        
        action_str = actions[prev_action_idx]
        estado, recompensa = get_state_reward(s, action_str)
        recompensa_original = recompensa  # Salva o valor original
        state_idx = state_to_index(estado)
        visited_states.add(state_idx)

        action_idx = choose_action(state_idx, epsilon)
        
        # --- REWARD SHAPING: Custo de vida menor ---
        # Penalidade para desencorajar caminhos longos.
        custo_de_vida = -0.5  # ou mais negativo

        estado_formatado = format(int(estado, 2), '07b')
        plataforma = int(estado_formatado[:5], 2)

        # Penalidade extra por voltar à plataforma inicial (plataforma 0)
        if plataforma == 0 and steps > 1:  # penalize só se não for o primeiro passo
            print("Voltou à plataforma inicial, penalizando...")
            recompensa -= 500  # penalidade bem forte
        # Ajuste da recompensa
        if recompensa == -1:
            recompensa += 100  # valor extra para vitória

        recompensa_ajustada = recompensa + custo_de_vida
        # -------------------------------------------
        
        Q[prev_state_idx, prev_action_idx] = Q[prev_state_idx, prev_action_idx] + alpha * (recompensa_ajustada + gamma * np.max(Q[state_idx]) - Q[prev_state_idx, prev_action_idx])

        total_reward += recompensa
 
        if recompensa_original == -1 or recompensa_original == -14:
            done = True
            if recompensa_original == -1:
                total_wins += 1

    # --- Aqui é o final do episódio ---
    epsilon = max(epsilon_final, epsilon * taxa_decaimento)

    if (episode + 1) % 100 == 0:
        win_rate = (total_wins / 10) * 100
        print(f"Épocas {episode-9}-{episode+1} | Taxa de vitória: {win_rate:.1f}% | Epsilon: {epsilon:.4f} | Estados visitados: {len(visited_states)}")
        total_wins = 0  # Reseta o contador de vitórias para o próximo bloco

# --- Finalização ---
print("\nTreinamento concluído!")
print(f"Total de estados únicos visitados: {len(visited_states)} de 96.")
print("Q-table salva em 'resultado.txt'")
np.savetxt("resultado.txt", Q, fmt="%.6f", delimiter=", ")
s.close()