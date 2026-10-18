# ChatGPT Workspace Agents

[English](chatgpt-workspace-agents.md) · [Todos os clientes](installation.md)

Workspace Agents combinam instruções gerais, ferramentas selecionadas e skills
reutilizáveis. As instruções do agente definem seu papel; cada skill fornece um
procedimento específico e seus recursos. Instalar uma skill não concede acesso à
infraestrutura. **Os pacotes são validados localmente; upload, descoberta e execução
no ChatGPT ainda não foram testados.**

## Obter e construir pacotes

Quando houver uma [release publicada](https://github.com/sidney-neto/nvidia-runai-agent-skills/releases),
baixe o ZIP da skill desejada, `manifest.json` e `SHA256SUMS`. Compare o hash do
arquivo com sua linha em `SHA256SUMS`:

```sh
shasum -a 256 nvidia-runai-runai-context-discovery.zip
```

O checksum detecta alterações; também revise a origem e o conteúdo. Se ainda não
houver release com pacotes, construa localmente. Não envie o ZIP do repositório
inteiro nem o artefato de Actions que reúne várias skills.

Baixar e ler instruções não exige Python. Para construir e validar, prepare o
[ambiente de contribuição](../CONTRIBUTING.md#development-setup) e execute:

```sh
python scripts/package_chatgpt_skills.py --list
python scripts/package_chatgpt_skills.py --skill runai-context-discovery --output dist/selected
python scripts/package_chatgpt_skills.py --all --validate-only --json
make package-chatgpt
make validate-chatgpt
```

Cada `dist/chatgpt/<nome>/skill.zip` contém uma pasta com a skill, referências,
scripts, schemas e avisos legais necessários. `agents/openai.yaml` é gerado na
exportação. As pastas canônicas em `skills/` não são modificadas. A descoberta é
dinâmica e não depende de uma quantidade fixa de skills ou versões do Run:ai.

Em `dist/chatgpt/release/`, os mesmos ZIPs recebem nomes únicos para download,
acompanhados de manifesto e checksums. Use outro `--output` para uma compilação
alterada: arquivos diferentes existentes não são sobrescritos. `dist/` permanece
ignorado pelo Git. Exportar não instala dependências nem executa helpers; apenas
lê arquivos locais e metadados Git.

## Instalar e configurar o agente

No workspace elegível, abra **Plugins → Skills → Create → Upload from your
computer** e selecione um ZIP individual. Confira a análise de segurança. A
disponibilidade e as permissões de upload dependem do workspace.
[Orientação oficial sobre Skills](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

Em Agents, crie ou edite **NVIDIA Run:ai Infrastructure Expert**. No Agent Builder,
use o controle de adicionar skills, geralmente **Add skill**, para selecionar uma
skill disponível ou enviar seu arquivo. Teste em **Preview**; para salvar mudanças
em um agente ativo, use **Update**. Rótulos podem variar. A documentação confirma
essas capacidades, mas não todas as regras de validação do ZIP.
[Guia oficial de Workspace Agents](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business).

Adicione apenas os workflows necessários, começando por descoberta:

- `runai-context-discovery`, `runai-cluster-health`
- `runai-scheduling-diagnostics`, `runai-quota-capacity-planning`
- `runai-tls-oidc`, `nvidia-gpu-operator`
- `runai-vllm-serving`, `runai-upgrade-readiness`

O [modelo de instruções](../examples/chatgpt-agent-instructions.md) é opcional.
Importar separadamente mantém identidade, revisão, associação e atualização
independentes para cada skill.

## Exemplos de uso

Forneça evidências sanitizadas e alvos explícitos. Para testar seleção automática:

- “Analise offline o assets/example.snapshot.json da skill instalada. Detecte as versões e indique as lacunas.”
- “Audite as quotas por projeto e departamento sem alterar o cluster.”
- “Explique por que este workload continua Pending, usando este snapshot.”
- “Diagnostique o erro x509 no OIDC após a troca do certificado.”
- “Prepare um plano da versão instalada para a versão-alvo informada, preservando workloads e volumes.”
- “Revise esta configuração do vLLM para contexto de 32K e a memória disponível.”

Quando investigar problemas de seleção, mencione explicitamente a skill. Versões
desconhecidas permitem análise independente de versão; não herdam o perfil mais
recente.

Helpers opcionais precisam de Python 3.11+ e execução de código permitida. O
validador de snapshots também exige `jsonschema==4.25.1`. Não presuma instalação
automática no ChatGPT. Sem execução, use o runbook e declare que validação de
schema ou cálculos determinísticos não foram executados. É possível executar
localmente e fornecer resultados sanitizados: [configuração dos helpers](installation.md#offline-helpers-and-first-use).

O coletor exige ainda kubectl compatível e escopo autorizado. A instalação não
conecta Kubernetes, Run:ai, SSH ou MCP. Ferramentas, rede e permissões são
configuradas separadamente; não habilite acesso real apenas para testar o pacote.

## Compatibilidade e validação

O perfil **chatgpt-conservative-v1**, revisado em **2026-10-18**, está detalhado na
[matriz técnica](chatgpt-workspace-agents.md#compatibility-profile-chatgpt-conservative-v1).
Ele distingue ChatGPT Skills, Workspace Agents, Codex, Skills hospedadas na API e
o padrão Agent Skills. O limite documentado da API não é tratado como limite da
interface ChatGPT.

Limites locais: ZIP de até **25.000.000 bytes**, **250 arquivos**, **10.000.000 bytes
por arquivo** e **50.000.000 bytes descompactados no total**. São decisões
conservadoras do repositório. A aceitação desses pacotes no ChatGPT permanece
pendente de teste manual. Metadados OpenAI são documentados para clientes locais;
seu uso na interface web de Workspace Agents não foi confirmado.

O validador rejeita caminhos perigosos, symlinks, arquivos especiais, duplicatas,
entrypoints extras, referências ausentes, dependências não declaradas e indicadores
conhecidos de dados sensíveis. Não executa código nem extrai ZIPs não confiáveis.
Detectar segredos é heurístico; caminhos e imports dinâmicos exigem revisão.

```sh
make check
make check-chatgpt
python scripts/validate_chatgpt_skill.py dist/chatgpt/runai-context-discovery/skill.zip --json
python scripts/validate_chatgpt_skill.py --release dist/chatgpt/release --json
```

Falhas retornam código diferente de zero. O validador também aceita uma pasta já
extraída. Os testes verificam todos os pacotes e executam helpers representativos
com fixtures sintéticas fora do checkout. Isso não comprova comportamento do agente.

## Atualizar e resolver problemas

Revise o diff e o checksum da nova release, guarde o ZIP anterior e teste em um
rascunho privado. Use os controles de edição/substituição disponíveis no workspace;
o contrato exato de atualização de ZIP no mesmo registro não foi confirmado.
Quando necessário, envie a nova skill separadamente e substitua a associação
após Preview. Confirme a revisão ativa antes de retirar a anterior. Remover uma
skill do agente não revoga credenciais de ferramentas.

- Upload ausente: confira disponibilidade e permissão no workspace.
- ZIP rejeitado: confira hash, estrutura e erro exato da interface.
- Needs Review/Blocked: siga a revisão do workspace; não contorne o bloqueio.
- Helper indisponível: confira execução e dependências ou use análise pelas instruções.
- Skill não selecionada: confira associação, descrição e invocação explícita.

Checklist manual, **ainda não executado**:

1. Importar descoberta; registrar SHA, data, workspace e resultado da análise.
2. Associar a um rascunho privado e testar o snapshot sintético em Preview.
3. Verificar versões independentes, lacunas explícitas e ausência de chamadas reais.
4. Testar seleção implícita de outra skill e um pedido sem relação com infraestrutura.
5. Registrar se houve execução real do helper ou apenas análise das instruções.
6. Testar substituição/remoção antes de publicar mudanças para outros usuários.

## Distribuição para mantenedores

O workflow gera artefatos em PRs, pushes para main e execução manual. Tags
`vMAJOR.MINOR.PATCH`, com sufixo de pré-release opcional, geram uma **release em
rascunho**, após validação. Somente esse job possui escrita. A publicação exige
ação explícita do mantenedor; commits comuns não publicam releases e nenhum
workflow envia arquivos para contas ChatGPT. ZIPs usam ordem, permissões e datas
fixas; manifesto e checksums identificam revisão, versão e limitações.
