### Incidência (Vanessa)

- Matriz: é a matriz base $M$, onde **linhas são pessoas** e **colunas são gêneros**; cada célula guarda quantas vezes aquela pessoa se conectou àquele gênero (peso). Isso é uma matriz de incidência/bipartida pessoa–gênero.
- Grafo: bipartido, com dois tipos de nós (pessoas e gêneros) e arestas apenas entre pessoa ↔ gênero, com peso igual ao valor da célula em $M$.
- Métricas: medem “quantas conexões cada vértice tem” na rede pessoa–gênero (grau de pessoas = quantos gêneros curte; grau de gêneros = quantas pessoas curtem aquele gênero).

Em resumo: **mostra a relação direta pessoa–gênero** (quem gosta de quê), sem comparar pessoas entre si nem gêneros entre si.

### Similaridade (Rodrigo)

- Matriz: constrói a **mesma matriz de incidência $M$**, depois calcula $S = M \cdot M^T$.
  - Linhas e colunas de $S$ são pessoas; $S_{ij}$ é a quantidade de gêneros em comum entre pessoa $i$ e pessoa $j$.
  - Zera a diagonal para não contar “pessoa com ela mesma”.
- Grafo: nós = pessoas; arestas entre pessoas que compartilham pelo menos um gênero, com peso = número de gêneros em comum (valor da matriz de similaridade).
- Métricas: agora o grau de um nó indica quantas pessoas aquela pessoa se conecta na rede de similaridade, e o grau ponderado indica **quão forte é a sobreposição de gostos** com o resto (mais gêneros em comum → peso maior).

Em resumo: **compara pessoas entre si**, transformando “quem gosta de quê” em “quem se parece com quem” em termos de gostos.

### Coocorrência (Guilherme)

- Matriz: também usa a mesma incidência $M$, mas calcula $C = M^T \cdot M$.
  - Linhas e colunas de $C$ são gêneros; $C_{ab}$ é o número de pessoas que gostam simultaneamente dos gêneros $a$ e $b$.
  - Zera a diagonal para remover o “gênero com ele mesmo”.
- Grafo: nós = gêneros; arestas entre gêneros que aparecem juntos para pelo menos uma pessoa, com peso = quantas pessoas compartilham aquele par de gêneros (valor de coocorrência).
- Métricas: agora o grau (e grau ponderado) de um gênero indica com quantos outros gêneros ele costuma aparecer junto, e o quão “popular como combinação” ele é (coocorrência forte com muitos outros).

Em resumo: **compara gêneros entre si**, mostrando “quais gêneros andam juntos” nas preferências das pessoas.

### Resumão em uma frase cada

- Incidência: matriz e grafo que ligam diretamente **pessoas → gêneros**, base de tudo.
- Similaridade: usa $M M^T$ para ligar **pessoas ↔ pessoas** via gêneros em comum (rede de afinidade entre pessoas).
- Coocorrência: usa $M^T M$ para ligar **gêneros ↔ gêneros** via pessoas em comum (rede de afinidade entre gêneros).
