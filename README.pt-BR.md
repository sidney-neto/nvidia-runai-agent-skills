# nvidia-runai-agent-skills

Biblioteca comunitária independente com **22 skills** para administração,
governança, quotas de GPU, diagnóstico e planejamento de upgrades do NVIDIA
Run:ai Self-Hosted. Codex é o cliente principal; o formato Agent Skills permite
reutilização por outros clientes compatíveis. Sem endosso da NVIDIA.

A biblioteca investiga qualquer versão informada, mas executa procedimentos
específicos somente com evidência correspondente. Uma versão desconhecida não
herda automaticamente o perfil mais recente. Código e documentação canônica
estão em inglês; cada skill também inclui um exemplo de uso em português.

## Instalação

```sh
git clone https://github.com/sidney-neto/nvidia-runai-agent-skills.git
cd nvidia-runai-agent-skills
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
make check
```

Abra o Codex na raiz: `.agents/skills` aponta para os diretórios canônicos em
`skills/`. Para instalar uma única skill completa, sem sobrescrever outra:

```sh
python scripts/install_skill.py runai-context-discovery --destination "$HOME/.agents/skills"
python -m pip install -r "$HOME/.agents/skills/runai-context-discovery/requirements.txt"
```

Recarregue a descoberta de skills se necessário. Nenhuma configuração global do
cliente é alterada. Python 3.11+ é necessário; os testes foram preparados para 3.12.

## Primeiro uso, sem cluster

“Use runai-context-discovery para analisar examples/eight-gpu.snapshot.json.”

```sh
python skills/runai-quota-capacity-planning/scripts/quota.py examples/eight-gpu.snapshot.json --format text
python skills/runai-scheduling-diagnostics/scripts/fit.py examples/eight-gpu.snapshot.json
python skills/runai-vllm-serving/scripts/budget.py examples/vllm-budget.json
```

- “Audite as quotas por projeto e departamento sem alterar o cluster.”
- “Explique por que este workload continua Pending.”
- “Detecte a versão deste ambiente e use a documentação correspondente.”
- “Prepare um plano da versão instalada para a versão-alvo informada, preservando workloads e volumes.”
- “Analise este snapshot de uma versão ainda não cadastrada e indique as limitações.”
- “Diagnostique o erro x509 no OIDC após a troca do certificado.”
- “Revise esta configuração do vLLM para contexto de 32K.”

O exemplo sintético tem oito GPUs em dois workers físicos, um control plane
virtual, ingress HAProxy e armazenamento persistente de modelos. Não estabelece
requisito de hardware, alta disponibilidade ou suporte do fornecedor. Versões e
recursos opcionais devem ser preenchidos com evidência do ambiente real.

## Cobertura e limites

Os perfis iniciais verificam a diferença no limite de frações de GPU entre as
baselines Self-Hosted 2.26 e 3.0, além do plano 2.26 → 3.0 em etapas por componente.
Não certificam todos os patches, versões futuras ou caminhos históricos. Consulte
[a matriz](docs/compatibility.md), [o catálogo](docs/catalog.md),
[as fontes](docs/sources.json) e [os resultados de validação](docs/validation.md).

Os helpers offline não usam cluster, credenciais, MCP ou APIs de modelos. O MCP
oficial é opcional. O coletor ao vivo exige alvos e autorização explícitos;
kubectl busca os objetos completos internamente e filtra a saída no cliente.
Instalar uma skill não concede permissão nem habilita escrita. Relatórios precisam
de revisão humana após a redação de dados sensíveis. Não foram executados testes
reais de cluster nem a suíte de comportamento do agente.

Para uma nova versão: localize documentação e interfaces exatas, registre a
proveniência, adicione um perfil limitado com fixtures positivas e negativas e
execute `make check`. Preserve os nomes por objetivo. Veja
[CONTRIBUTING.md](CONTRIBUTING.md) e [as instruções de instalação](docs/installation.md).
