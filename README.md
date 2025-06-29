# Qlearning
 ## Dificuldades:
  Durante a execução do problema me deparei com as seguintes dificuldades:
    - Dificuldade na interação com o Ambiente
    - Escolha dos Hiperparâmetros
    - Repetição redundante de ações no estado Inicial("Boneco pulava pra fora na primeira plataforma")
  ## O Que fiz
    Para resolver os Hiperparâmetros escolhi adotar um epsilon não fixo, que decai ao longo do código para que o agente explore o máximo possível nas primeiras épocas e no final apenas refine o aprendizado

    Para resolver o problema do estado inicial utilizei uma verificação no começo de cada época para alinha o agente na direção correta(norte = "00") e só depois executar o jump

    fiz ajustes de penalidade para quando o boneco quisesse retornar para a plataforma inicial e adicionei uma recompensa maior para quando chegasse no objetivo,além disso limitei o número de passos para 100