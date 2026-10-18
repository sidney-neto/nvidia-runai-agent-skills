# NVIDIA Run:ai Agent Skills

[![Offline validation](https://github.com/sidney-neto/nvidia-runai-agent-skills/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/sidney-neto/nvidia-runai-agent-skills/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Helpers: Python 3.11+](https://img.shields.io/badge/helpers-Python%203.11%2B-3776AB.svg)](CONTRIBUTING.md#development-setup)
[![Format: Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-76B900.svg)](https://agentskills.io/specification)

**22 skills focadas · Análise de evidências offline · Procedimentos por versão**

Administração de NVIDIA Run:ai Self-Hosted, quotas de GPU, governança e diagnóstico
com Kubernetes, GPU Operator, NVIDIA NIM e vLLM. Inspecione o ambiente e prepare
mudanças revisáveis a partir de snapshots sanitizados. Projeto comunitário
independente, sem endosso da NVIDIA.

[English](README.md) · [Catálogo](docs/catalog.md) ·
[Instalação](docs/installation.md) · [Compatibilidade](docs/compatibility.md) ·
[Contribuir](CONTRIBUTING.md)

## Início rápido

No projeto em que pretende usá-la, com Node/npm disponível:

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent codex --copy
```

Confira skills existentes com o mesmo nome antes de instalar. O comando copia
instruções e recursos; o ambiente Python é necessário apenas para helpers e testes.
Use o identificador abaixo com `--agent` ou siga o guia nativo do cliente.

| Cliente | Forma de instalação |
|---|---|
| Codex | `--agent codex` |
| Claude Code | `--agent claude-code` |
| OpenClaw · Hermes Agent | `--agent openclaw` / `--agent hermes-agent`; instaladores nativos também documentados |
| Gemini CLI · GitHub Copilot · Cursor · OpenCode | `--agent gemini-cli` / `github-copilot` / `cursor` / `opencode` |
| NVIDIA NemoClaw | Instalação no runtime escolhido de um sandbox existente |
| Grok Bot | Adaptação manual com arquivos fornecidos; importação do pacote não verificada |

O [guia de instalação](docs/installation.md) explica escopo por projeto/usuário,
instalação sem npm, comandos nativos, atualização e remoção. A cópia dos arquivos
foi testada para os oito destinos da CLI; a execução pelos agentes não foi testada.
NemoClaw e Grok Bot têm limitações próprias documentadas.

Para usar no próprio repositório com Codex, clone-o e abra sua raiz no cliente.
Os links em `.agents/skills` apontam para as pastas canônicas em `skills/`.
Cada skill também pode ser instalada separadamente com referências, schemas,
scripts e avisos legais, sem depender de arquivos externos à sua pasta.

## Primeiro uso

Selecione `$runai-context-discovery` no Codex CLI/IDE ou
`/runai-context-discovery` no Claude Code e peça:

> Analise offline o arquivo assets/example.snapshot.json incluído nesta skill.
> Preserve versões desconhecidas e indique as evidências ausentes. Não acesse o cluster.

## Escolha o fluxo

| O que pedir | Skill indicada |
|---|---|
| Detecte as versões e indique as evidências ausentes. | [Descoberta de contexto](skills/runai-context-discovery/SKILL.md) |
| Explique a degradação dos nós ou da conexão com o cluster. | [Saúde do cluster](skills/runai-cluster-health/SKILL.md) |
| Audite as quotas por projeto e departamento sem alterar o cluster. | [Quotas e capacidade](skills/runai-quota-capacity-planning/SKILL.md) |
| Explique por que este workload continua Pending. | [Diagnóstico de agendamento](skills/runai-scheduling-diagnostics/SKILL.md) |
| Diagnostique o erro x509 no OIDC após a troca do certificado. | [TLS e OIDC](skills/runai-tls-oidc/SKILL.md) |
| Prepare um plano para a versão-alvo, preservando workloads e volumes. | [Preparação para upgrade](skills/runai-upgrade-readiness/SKILL.md) |
| Revise esta configuração do vLLM para contexto de 32K. | [Serving com vLLM](skills/runai-vllm-serving/SKILL.md) |

[Veja as 22 skills →](docs/catalog.md), incluindo RBAC, políticas, compartilhamento
de GPU, NIM, workloads distribuídos, armazenamento, rede e recuperação.
Forneça arquivos sanitizados e alvos explícitos. Para uma versão ainda não
cadastrada, peça análise offline e indicação das limitações.

Os [helpers opcionais](docs/installation.md#offline-helpers-and-first-use) usam
Python; o validador de snapshots também exige a dependência jsonschema empacotada.
Instale dependências antes de trabalhar offline. O [snapshot sintético de oito GPUs](examples/eight-gpu.snapshot.json)
e o [relatório de exemplo](examples/executive-report.md) não exigem credenciais,
GPU ou MCP. O exemplo tem um único control plane, sem presumir alta disponibilidade.

## Escopo e evidências

Qualquer versão informada pode ser investigada. Versões desconhecidas continuam
permitindo análise offline e nunca herdam automaticamente o perfil mais recente.
Os perfis iniciais cobrem diferenças de frações entre Self-Hosted 2.26/3.0 e um
plano documentado 2.26 → 3.0 em etapas por componente; não certificam todos os
patches nem limitam a arquitetura a essas versões. Consulte a
[matriz de evidências](docs/compatibility.md).

MCP é opcional. Operações reais exigem interfaces verificadas, alvos explícitos e
autorização correspondente. A instalação não habilita conexões, credenciais ou
escritas. Guarde snapshots e relatórios privados em `.local/`, ignorado pelo Git;
a sanitização automática é heurística e exige revisão antes de compartilhar.

Para adicionar cobertura, revise as fontes da versão exata, acrescente um
perfil/referência delimitado e fixtures positivas/negativas e execute `make check`.
Preserve os nomes orientados ao objetivo das skills.

## Contribuir

O [guia de contribuição](CONTRIBUTING.md) contém o ambiente opcional de
desenvolvimento e a validação com `make check`. Os testes são sintéticos e offline
após instalar dependências. Avaliações de comportamento dos agentes e integrações
reais não foram executadas. A atualização das fontes é separada e usa rede.

[Segurança](SECURITY.md) · [Fontes](docs/sources.json) ·
[Procedência](docs/upstream-provenance.md) · [Licença](LICENSE) ·
[Atribuição](THIRD_PARTY_NOTICES.md)
