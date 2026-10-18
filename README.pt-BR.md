# nvidia-runai-agent-skills

**22 skills portáveis** para administração de NVIDIA Run:ai Self-Hosted, quotas de
GPU, governança e diagnóstico com Kubernetes, GPU Operator, NVIDIA NIM e vLLM.
Inspeção e planejamento são o padrão. Projeto comunitário independente, sem
endosso da NVIDIA; não instala servidor nem opera um cluster automaticamente.

[English](README.md) · [Catálogo](docs/catalog.md) ·
[Instalação e clientes](docs/installation.md) · [Compatibilidade](docs/compatibility.md)

## Instalar uma skill

No projeto em que pretende usá-la, com Node/npm disponível:

```sh
npx skills@1.7.2 add sidney-neto/nvidia-runai-agent-skills \
  --skill runai-context-discovery --agent codex --copy
```

Confira skills existentes com o mesmo nome antes de instalar. Substitua `codex`
por `claude-code`, `openclaw`, `hermes-agent`, `gemini-cli`, `github-copilot`,
`cursor` ou `opencode`, conforme o cliente. A instalação das instruções não exige
o ambiente Python de desenvolvimento.

O [guia de instalação](docs/installation.md) explica escopo por projeto/usuário,
instalação sem npm, comandos nativos de OpenClaw/Hermes, sandboxes NemoClaw já
existentes, atualização e remoção. Para Grok Bot, há uma adaptação manual com
limitações explícitas; a importação deste pacote GitHub não foi verificada.
Copiar arquivos com sucesso não comprova execução pelo agente.

Para usar no próprio repositório com Codex, clone-o e abra sua raiz no cliente.
Os links em `.agents/skills` apontam para as pastas canônicas em `skills/`.
Cada skill também pode ser instalada separadamente com referências, schemas,
scripts e avisos legais, sem depender de arquivos externos à sua pasta.

## Primeiro uso

Selecione `$runai-context-discovery` no Codex CLI/IDE ou
`/runai-context-discovery` no Claude Code e peça:

> Analise offline o arquivo assets/example.snapshot.json incluído nesta skill.
> Preserve versões desconhecidas e indique as evidências ausentes. Não acesse o cluster.

Outros exemplos práticos, fornecendo arquivos sanitizados e alvos explícitos:

- **Quotas:** “Use runai-quota-capacity-planning. Audite as quotas por projeto e departamento sem alterar o cluster.”
- **Agendamento:** “Use runai-scheduling-diagnostics. Explique por que este workload continua Pending.”
- **TLS/OIDC:** “Use runai-tls-oidc. Diagnostique o erro x509 no OIDC após a troca do certificado.”
- **Upgrade:** “Use runai-upgrade-readiness. Prepare um plano da versão instalada para a versão-alvo informada, preservando workloads e volumes.”
- **vLLM:** “Use runai-vllm-serving. Revise esta configuração do vLLM para contexto de 32K.”
- **Versão desconhecida:** “Analise este snapshot de uma versão ainda não cadastrada e indique as limitações.”

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
