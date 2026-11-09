# Tópicos encontrados nos chunks

Collection `artigos_ia`: **8808 chunks** de **100 PDFs**, tratados como um único corpus. O K-Means agrupou os embeddings (bge-m3, 1024 dimensões) em **5 tópicos**.
Nenhuma informação de arquivo ou categoria do arXiv entra no agrupamento.

Os nomes foram sugeridos pelo LLM local a partir dos termos e trechos de cada grupo e depois revisados à mão (coluna *Sugestão do LLM*).

| # | Tópico | Sugestão do LLM | Chunks | PDFs com trechos | PDFs onde é dominante | Termos característicos |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | **Tabelas de Resultados** | Resultados e Tabelas | 2230 | 97 | 22 | table, gpt-, mean, claude, flash, base, accuracy, sft |
| 1 | **Agentes e Aprendizado por Reforço** | Aprendizado por Reforço | 1871 | 94 | 25 | policy, agent, learning, agents, work, agentic, tasks, reinforcement learning |
| 2 | **Visão Computacional 3D** | Visão 3D | 1727 | 68 | 23 | camera, frame, geometry, image, frames, scene, video, cameras |
| 3 | **Perguntas, Prompts e Avaliação** | Prompt e Avaliação | 1660 | 74 | 18 | sql, answer, evidence, question, label, json, conversation, patient |
| 4 | **Provas e Teoremas** | Prova e Teorema | 1320 | 88 | 12 | probability, lemma, inequality, equation, define, proof, theorem, bound |

## Detalhes

### 0. Tabelas de Resultados

Contém dados numéricos e tabelas de resultados de experimentos.

Artigos com mais trechos no tópico:

- MJev-Spatial: System One Spatial Intelligence via Native Attention Matching (79 chunks)
- EMO: A Closed-Loop Test-Time Computation Framework via Alternating Context Optimization and Logits Steering (63 chunks)
- Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine (61 chunks)
- BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks (50 chunks)
- 3DCodeVerse: Exploring 3D Worlds as Code (50 chunks)

### 1. Agentes e Aprendizado por Reforço

Contém trechos focados em algoritmos e técnicas de aprendizado por reforço em agentes de IA.

Artigos com mais trechos no tópico:

- OS-Helix: Unifying GUI Interaction and Code Execution in Native Computer-Using Agents (70 chunks)
- Improving Environment-Agnostic Coding Agents: The Role of Scaffolding (55 chunks)
- Mosaic: Multi-Session Agentic Reinforcement Learning (50 chunks)
- Training Reasoning Models to Generate Diverse Scientific Ideas (49 chunks)
- Mem4Act: Learning Effective Latent Memory for Long-Horizon Robotic Manipulation (48 chunks)

### 2. Visão Computacional 3D

Contém trechos relacionados à geração e modelagem de objetos em 3D.

Artigos com mais trechos no tópico:

- SUPRA-TEX: 3D Generation with Super-Aligned Texture (108 chunks)
- GeoState: Learning View-Decoupled Geometry States for 3D World Modeling (90 chunks)
- CF-Splat: Closed-Form Triangle Splatting with Mesh Priors (86 chunks)
- 3DCodeVerse: Exploring 3D Worlds as Code (82 chunks)
- Perceive, Predict, and Plan: a Unified World Action Model for Egocentric Dexterous Manipulation (77 chunks)

### 3. Perguntas, Prompts e Avaliação

Inclui prompts de avaliação e métodos de teste para modelos de linguagem.

Artigos com mais trechos no tópico:

- MindEval2: Clinically Grounded Patients and Rubrics for Evaluating Language Models in Mental Health Support (140 chunks)
- CLUE: Uncovering Social Context for Pragmatic Understanding (123 chunks)
- PremiseSQL: Evaluating Premise Critique and Abstention in Text-to-SQL Systems (110 chunks)
- Training Reasoning Models to Generate Diverse Scientific Ideas (98 chunks)
- AI Consilium: a Benchmark of LLM Clinical Multidisciplinary Second Opinions (97 chunks)

### 4. Provas e Teoremas

Contém provas matemáticas e enunciados de teoremas relacionados a aprendizado de máquina e otimização.

Artigos com mais trechos no tópico:

- Learning Rational Strategies for Temporal Objectives in Multi-Agent Systems (70 chunks)
- Explore Once, Evaluate Many: Multiple Policy Evaluation for Stochastic Linear Bandits (57 chunks)
- Query-Efficient Rejection Sampling for Parallel Masked Diffusion (54 chunks)
- Generalization Guarantees of Randomized Block Coordinate Descent for Nonconvex Learning (50 chunks)
- Baselines and Score Centering in Policy Gradient Estimation (46 chunks)
