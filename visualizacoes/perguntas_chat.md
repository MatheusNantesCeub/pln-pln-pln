# Perguntas ao chat RAG local

Collection `artigos_ia` · LLM e embeddings rodando localmente no Ollama · gabaritos extraídos dos resumos do arXiv.

## 1. Qual HOTA o ARC-SORT alcança no teste do SportsMOT e a quantos quadros por segundo ele roda?

**Gabarito:** 81,82 HOTA no SportsMOT; cerca de 50 FPS em uma RTX 3060 de notebook (artigo 2610.22306).

**Resposta do chat:**

> O ARC-SORT alcança um HOTA de 81,82 no teste do SportsMOT e roda a aproximadamente 50 quadros por segundo em uma GPU RTX 3060 de laptop, conforme mencionado na [Fonte: ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models].

*Processado por `local` em 3.6s.* Trechos recuperados:

- ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models — `2610.22306.pdf` · similaridade 0.713 · tópico *Visão Computacional 3D*
- ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models — `2610.22306.pdf` · similaridade 0.674 · tópico *Tabelas de Resultados*
- ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models — `2610.22306.pdf` · similaridade 0.672 · tópico *Tabelas de Resultados*
- ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models — `2610.22306.pdf` · similaridade 0.670 · tópico *Tabelas de Resultados*
- ARC-SORT: Adaptive, Robust, Compensated Multi-Object Tracking with Interacting Multiple Models — `2610.22306.pdf` · similaridade 0.667 · tópico *Tabelas de Resultados*

## 2. No RAG-RST, quanto o F1 de nuclearidade e de relação melhora em relação ao LLM sem exemplos recuperados?

**Gabarito:** Nuclearidade de 0,794 para 0,846 F1 e relação de 0,738 para 0,788 F1, sem treinamento (2610.22150).

**Resposta do chat:**

> No RAG-RST, o F1 de nuclearidade e de relação melhora significativamente em comparação a um LLM sem exemplos recuperados. De acordo com o contexto fornecido, um LLM forte alcança um F1 de 0,794 para nuclearidade e 0,738 para relação, apenas com um par de EDU-alvo. No entanto, com o framework RAG-RST, esses valores melhoram para 0,846 para nuclearidade e 0,788 para relação, sem a necessidade de atualizações de parâmetros. Essa melhoria é observada tanto na configuração pré-computada quanto na dinâmica, com o RAG-RST dinâmico tendo performances consistentemente melhores. As informações relevantes podem ser encontradas na seção [Fonte: RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing].

*Processado por `local` em 5.4s.* Trechos recuperados:

- RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing — `2610.22150.pdf` · similaridade 0.703 · tópico *Tabelas de Resultados*
- RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing — `2610.22150.pdf` · similaridade 0.646 · tópico *Tabelas de Resultados*
- RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing — `2610.22150.pdf` · similaridade 0.636 · tópico *Tabelas de Resultados*
- RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing — `2610.22150.pdf` · similaridade 0.621 · tópico *Tabelas de Resultados*
- RAG-RST: Retrieved Exemplars as In-Context Discourse Schema for RST Parsing — `2610.22150.pdf` · similaridade 0.620 · tópico *Tabelas de Resultados*

## 3. Como o artigo sobre RAG privado protege o banco de documentos contra ataques de extração?

**Gabarito:** Aplica a mesma projeção aleatória aos embeddings do datastore e das consultas (2610.22297).

**Resposta do chat:**

> O artigo "Private Retrieval Augmented Generation via Random Projection" propõe uma técnica para proteger o banco de documentos contra ataques de extração usando projeção aleatória. De acordo com o texto, a técnica visa mitigar os riscos associados à proteção de privacidade baseada em diferencial de privacidade (DP), que pode degradar a qualidade do output devido às garantias de pior caso e à complexidade de implementação.
> 
> A proposta é que a projeção aleatória possa ser uma solução mais eficaz, pois preserva as similaridades entre as entradas no espaço de baixa dimensionalidade, adicionando um nível extra de aleatoriedade que dificulta a recuperação do texto original pelos atacantes. De fato, o artigo demonstra que a técnica baseada em projeção aleatória melhora significativamente a utilidade (em mais de 50% em média em diferentes conjuntos de dados) em comparação com os métodos de base, sem comprometer a performance de privacidade empírica.
> 
> Além disso, o artigo observa que URLs são os dados mais fáceis de serem expostos. No entanto, a técnica de projeção aleatória mantém uma boa proteção de privacidade (2,19-2,27% de exposição) mesmo em textos não estruturados, como o caso do conjunto de dados ECHR, que contém narrativas legais com informações pessoais sensíveis. Isso sugere que a mecanismo de preservação de privacidade opera no nível das embeddings, tornando-se agnóstico ao formato ou estrutura do conteúdo sensível.
> 
> Portanto, a técnica de projeção aleatória é apresentada como uma alternativa competitiva e prática para sistemas de RAG privados, oferecendo uma abordagem leve que atinge desempenho superior em comparação com métodos anteriores que utilizam garantias formais de diferencial de privacidade. [Fonte: Private Retrieval Augmented Generation via Random Projection]

*Processado por `local` em 8.8s.* Trechos recuperados:

- Private Retrieval Augmented Generation via Random Projection — `2610.22297.pdf` · similaridade 0.661 · tópico *Agentes e Aprendizado por Reforço*
- Private Retrieval Augmented Generation via Random Projection — `2610.22297.pdf` · similaridade 0.626 · tópico *Agentes e Aprendizado por Reforço*
- Private Retrieval Augmented Generation via Random Projection — `2610.22297.pdf` · similaridade 0.621 · tópico *Agentes e Aprendizado por Reforço*
- Private Retrieval Augmented Generation via Random Projection — `2610.22297.pdf` · similaridade 0.620 · tópico *Agentes e Aprendizado por Reforço*
- Private Retrieval Augmented Generation via Random Projection — `2610.22297.pdf` · similaridade 0.618 · tópico *Agentes e Aprendizado por Reforço*

## 4. Quanto tempo os agentes Gemini 4 Argon levaram para derrotar o Ender Dragon no Minecraft e quantas vezes morreram?

**Gabarito:** 27 horas e 14 minutos, 605 mortes e 2.783 programas escritos (2610.22319).

**Resposta do chat:**

> Os agentes Gemini 4 Argon levaram 27 horas e 14 minutos para derrotar o Ender Dragon no Minecraft, conforme mencionado na [Fonte: A team of Gemini 4 Argon agents beats Minecraft]. Ao longo desse processo, os agentes morreram 605 vezes, como informado na mesma fonte.

*Processado por `local` em 2.7s.* Trechos recuperados:

- A team of Gemini 4 Argon agents beats Minecraft — `2610.22319.pdf` · similaridade 0.781 · tópico *Tabelas de Resultados*
- A team of Gemini 4 Argon agents beats Minecraft — `2610.22319.pdf` · similaridade 0.763 · tópico *Visão Computacional 3D*
- A team of Gemini 4 Argon agents beats Minecraft — `2610.22319.pdf` · similaridade 0.706 · tópico *Tabelas de Resultados*
- A team of Gemini 4 Argon agents beats Minecraft — `2610.22319.pdf` · similaridade 0.701 · tópico *Perguntas, Prompts e Avaliação*
- A team of Gemini 4 Argon agents beats Minecraft — `2610.22319.pdf` · similaridade 0.700 · tópico *Tabelas de Resultados*

## 5. Qual taxa de alcance o PSA-PPO obteve na colheita robótica de alface hidropônica e em que robô foi testado?

**Gabarito:** 94,7% de alcance em 150 alvos, braço UR10e; 86,1% de colheita completa (2610.22337).

**Resposta do chat:**

> O PSA-PPO obteve uma taxa de alcance de 94,7% na colheita robótica de alface hidropônica em um benchmark físico controlado com 150 alvos programados. Este teste foi realizado com um braço robótico UR10e [Fonte: Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce].

*Processado por `local` em 3.1s.* Trechos recuperados:

- Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce — `2610.22337.pdf` · similaridade 0.678 · tópico *Agentes e Aprendizado por Reforço*
- Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce — `2610.22337.pdf` · similaridade 0.667 · tópico *Visão Computacional 3D*
- Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce — `2610.22337.pdf` · similaridade 0.663 · tópico *Agentes e Aprendizado por Reforço*
- Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce — `2610.22337.pdf` · similaridade 0.657 · tópico *Tabelas de Resultados*
- Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce — `2610.22337.pdf` · similaridade 0.616 · tópico *Agentes e Aprendizado por Reforço*

## 6. Quantas consultas com premissas falhas o benchmark PremiseSQL contém?

**Gabarito:** 1.800 consultas falhas em quatro categorias, mais as 1.800 originais (2610.22158).

**Resposta do chat:**

> O benchmark PremiseSQL contém 1,800 consultas com premissas falhas. Isso está mencionado na seção de conclusão do artigo [Fonte: PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems].

*Processado por `local` em 2.3s.* Trechos recuperados:

- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems — `2610.22158.pdf` · similaridade 0.680 · tópico *Perguntas, Prompts e Avaliação*
- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems — `2610.22158.pdf` · similaridade 0.665 · tópico *Perguntas, Prompts e Avaliação*
- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems — `2610.22158.pdf` · similaridade 0.661 · tópico *Perguntas, Prompts e Avaliação*
- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems — `2610.22158.pdf` · similaridade 0.648 · tópico *Perguntas, Prompts e Avaliação*
- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems — `2610.22158.pdf` · similaridade 0.647 · tópico *Perguntas, Prompts e Avaliação*

## 7. Que modelo foi especializado para a variante Masewalkopa do náuatle e qual chrF++ ele obteve?

**Gabarito:** Um checkpoint mT5-large (modelo LoRA-v9c-b), 58,46 chrF++ no dev (2610.22110).

**Resposta do chat:**

> Um modelo especializado para a variante Masewalkopa do nawatl foi desenvolvido a partir de uma verificação de 1,2 bilhão de parâmetros do mT5-large. O modelo especializado, denominado lora_v9c_b, obteve os seguintes resultados de chrF++:
> 
> - 58.46 para o conjunto de desenvolvimento (dev chrF++)
> - 58.20/57.90 para os testes direcionais (directional test chrF++)
> 
> Esses resultados foram obtidos após o processo de especialização, que incluiu a curadoria de 2.665 pares paralelos, a integração de 192 sentenças transcritas por idosos através de backtranslation assimétrico, e a utilização de um analisador de estado finito personalizado. Essas técnicas permitiram uma melhoria significativa em relação ao baseline multivariante, com ganhos superiores a 28 pontos percentuais. [Fonte: Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewwalkopa]

*Processado por `local` em 5.5s.* Trechos recuperados:

- Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewalkopa — `2610.22110.pdf` · similaridade 0.590 · tópico *Tabelas de Resultados*
- Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewalkopa — `2610.22110.pdf` · similaridade 0.578 · tópico *Tabelas de Resultados*
- Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewalkopa — `2610.22110.pdf` · similaridade 0.527 · tópico *Agentes e Aprendizado por Reforço*
- Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewalkopa — `2610.22110.pdf` · similaridade 0.521 · tópico *Agentes e Aprendizado por Reforço*
- Unfragmenting Nawatl NMT: Single-Variant Specialization for Masewalkopa — `2610.22110.pdf` · similaridade 0.516 · tópico *Tabelas de Resultados*

## 8. Qual é a receita tradicional do pão de queijo mineiro?

**Gabarito:** Fora do corpus: o modelo deve dizer que o contexto não traz essa informação.

**Resposta do chat:**

> Não há informações relevantes no contexto fornecido sobre a receita tradicional do pão de queijo mineiro. As fontes fornecidas se referem a experimentos e resultados em processamento de linguagem natural, aprendizado contínuo, busca de diversidade de qualidade e outros tópicos relacionados, sem mencionar receitas de alimentos. [Fonte: ...]

*Processado por `local` em 3.7s.* Trechos recuperados:

- Knowledge That Is Linear Before Fine-Tuning Generalizes After It — `2610.22300.pdf` · similaridade 0.352 · tópico *Tabelas de Resultados*
- Towards Continual Learning: Mitigating Forgetting With Subspace Tuning — `2610.22293.pdf` · similaridade 0.351 · tópico *Tabelas de Resultados*
- EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search — `2610.22290.pdf` · similaridade 0.350 · tópico *Agentes e Aprendizado por Reforço*
- OS-Helix: Unifying GUI Interaction and Code Execution in Native Computer-Using Agents — `2610.22234.pdf` · similaridade 0.348 · tópico *Tabelas de Resultados*
- Explaining the Roles of Experts in Mixture-of-Experts LLMs for Personalization — `2610.22127.pdf` · similaridade 0.347 · tópico *Tabelas de Resultados*
