# Building Agents from Scratch: Find a Place to Live

This one-hour webinar builds an agentic home-finding workflow with plain Python classes and direct Azure OpenAI calls. It uses no LangChain, CrewAI, AutoGen, Semantic Kernel, or agent SDK.

The only non-standard packages are the clients needed to reach Azure Key Vault and Azure OpenAI. Routing, memory, tools, handoffs, and workflow control are ordinary Python.

## What participants build

```text
User request
     |
 RouterAgent
  /  |  \
Housing | Neighborhood
Agent   | Agent
  \     | /
 RecommendationAgent
          |
        Answer
```

Suggested timing:

| Time | Topic |
|---|---|
| 0–10 min | Azure setup check and mental model |
| 10–15 min | Demo 1: one basic LLM call |
| 15–21 min | Demo 2: add context and a persona |
| 21–31 min | Demo 3: build one agent class |
| 31–41 min | Demo 4: add a tool-using agent loop |
| 41–49 min | Demo 5: evaluator-optimizer collaboration |
| 49–56 min | Demo 6: routed agentic workflow |
| 56–60 min | Recap and next experiments |

## Prerequisite: set up Azure

You need Python 3.11+, the Azure CLI, an Azure subscription, and permission to create resources and role assignments. Names must be globally unique where indicated.

Sign in and create the resource group, Azure OpenAI resource, and RBAC-enabled Key Vault:

```bash
az login
az group create --name agents-webinar-rg --location eastus

az cognitiveservices account create \
  --name <unique-openai-resource-name> \
  --resource-group agents-webinar-rg \
  --location eastus \
  --kind OpenAI \
  --sku S0 \
  --custom-domain <unique-openai-resource-name>

az keyvault create \
  --name <unique-vault-name> \
  --resource-group agents-webinar-rg \
  --location eastus \
  --enable-rbac-authorization true
```

In the Microsoft Foundry portal, open the Azure OpenAI resource and deploy `gpt-4.1-mini`. Give the deployment a memorable name such as `webinar-gpt-41-mini`. Model availability and versions vary by region, so using the portal makes capacity problems visible before the live session.

Grant yourself permission to manage secrets. Replace the placeholders with your Azure sign-in and subscription ID:

```bash
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee <your-sign-in-email> \
  --scope /subscriptions/<subscription-id>/resourceGroups/agents-webinar-rg/providers/Microsoft.KeyVault/vaults/<unique-vault-name>
```

In Key Vault, create these three secrets. Using the Azure portal avoids putting the API key into shell history:

| Secret name | Value |
|---|---|
| `aoai-endpoint` | `https://<resource-name>.openai.azure.com` |
| `aoai-key` | Azure OpenAI key 1 or key 2 |
| `aoai-deployment` | Your deployment name, for example `webinar-gpt-41-mini` |

The Key Vault URL is configuration, not a secret. Store it in the local `.env` file:

```text
WEBINAR_KEY_VAULT_URL=https://<unique-vault-name>.vault.azure.net/
```

`AzureLLMClient` loads this setting with the Python standard library. The `.env` file is ignored by Git because it may contain sensitive configuration in other projects.

Install the small dependency set:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`InteractiveBrowserCredential` opens an Azure sign-in page when the Python demo needs to access Key Vault. This makes authentication visible during the webinar and does not depend on an existing Azure CLI session. In production, use a managed identity and grant it the `Key Vault Secrets User` role. The code never logs secret values.

The shared [`AzureLLMClient`](services/azure_llm.py) reads configuration from Key Vault and calls Azure's v1 endpoint. The v1 endpoint avoids pinning the workshop to a dated `api-version`.

The webinar repository is intentionally small:

```text
01_model_call.py
02_persona_call.py
03_single_agent.py
04_agent_loop.py
05_agent_collaboration.py
06_routed_workflow.py
agents/                 # Every class that reasons as an agent
services/               # Azure OpenAI and Key Vault access
tools/                  # Functions agents call to retrieve housing facts
workflows/              # Deterministic orchestration and handoffs
requirements.txt
```

Every script prints its important intermediate steps. The terminal output is part of the lesson: prompts, memory updates, tool calls, observations, routing decisions, and agent handoffs remain visible instead of being hidden behind a framework.

## Demo 1: make a basic LLM call

Run:

```bash
python 01_model_call.py
```

[`01_model_call.py`](01_model_call.py) asks a broad relocation question without giving the model a role or personal context. The answer will probably be broad too.

Pause after the answer and ask the audience:

- Who is the model supposed to be?
- What does it know about the person moving?
- What constraints should guide its answer?
- What kind of answer should it produce?

This is only an LLM call. It has no identity, persistent memory, tool, or action loop.

## Demo 2: add context and a persona

Run:

```bash
python 02_persona_call.py
```

[`02_persona_call.py`](02_persona_call.py) supplies only two kinds of system-prompt information: the relocation advisor's persona and the Austin-area knowledge available to that persona.

The script asks two questions. Riley answers the Austin neighborhood question, then declines an unrelated cooking question. Use the contrast to identify three ideas:

- **Persona:** who Riley is and how Riley communicates;
- **Knowledge:** the Austin neighborhood facts Riley may use;
- **Scope:** Riley answers only questions that belong to the persona.

This is still an LLM call, not yet a full agent: it has no persistent memory, tool, or action loop. However, the system message establishes an identity, domain knowledge, and behavioral boundary. Demo 3 packages those ideas inside a reusable class.

Teaching question: “What could this program do if the answer required live rental data?” The answer is “nothing yet.” That limitation motivates tools.

## Demo 3: turn the model into an agent

Run:

```bash
python 03_single_agent.py
```

[`03_single_agent.py`](03_single_agent.py) introduces `HousingAgent`, implemented as a Python class. The script prints its four components before running it:

- **Persona:** Riley's role, tone, responsibility, and boundaries;
- **Knowledge:** stable housing principles included in the system prompt;
- **Tools:** named Python functions that retrieve current listing facts;
- **Memory:** previous requests retained by the running agent object.

The demo creates two `HousingAgent` instances and sends both the exact same follow-up question. The fresh agent has no earlier context, so its memory policy requires it to ask for the missing household details rather than guess. The existing agent remembers that the user is moving with two children and can make a recommendation. Their answers are printed side by side. For each call, the trace shows **memory read**, **memory write**, and the exact prior history sent to the model. Temperature is set to zero to reduce unrelated variation, making memory the clearest difference. Restarting the script clears that memory; persistent memory would require saving it to a file or database.

The listing tool intentionally uses an in-memory list. This keeps the agent mechanics visible and the demo reliable. Later, that one method can call a real property API without changing the rest of the class.

Key idea: the model supplies judgment; Python owns data access and control flow.

## Demo 4: let the agent choose a tool

Run:

```bash
python 04_agent_loop.py
```

In Demo 3, Python always calls `search_listings()` before asking the model for an answer. [`04_agent_loop.py`](04_agent_loop.py) creates the same `HousingAgent`, then passes it to an external `AgentLoop` runtime. The agent retains the same persona, knowledge, memory, and tool, but now chooses its next action.

The bounded loop is:

```text
Goal -> Decision -> Validated action -> Tool -> Observation -> Decision -> Final answer
```

The agent returns a small JSON decision. The external runtime checks the tool name and arguments before executing anything. Tool results become observations that are sent back to the agent. The loop stops when the agent chooses `finish`, or the runtime stops it after three steps.

Watch the printed trace for four concepts:

- **Decision:** the model selects an allowed next action;
- **Action:** Python validates and executes the selected tool;
- **Observation:** Python gives the tool result back to the model;
- **Loop:** the model decides again using the new information.

Key idea: the agent decides, while a deterministic runtime controls execution. Keeping the loop outside the agent makes that boundary visible.

## Demo 5: improve an answer through agent feedback

Run:

```bash
python 05_agent_collaboration.py
```

[`05_agent_collaboration.py`](05_agent_collaboration.py) demonstrates the evaluator-optimizer pattern:

```text
HousingAgent proposes
        ↓
NeighborhoodAgent evaluates
        ↓
HousingAgent revises
        ↓
User receives an improved answer
```

The first agent produces a recommendation. The second agent acts as a strict evaluator, separating supported claims from unsupported claims and suggesting a correction. Its critique is passed back to the first agent, which uses the feedback and its existing memory to revise the recommendation.

The printed messages include `from`, `to`, `purpose`, and `content`, making the feedback loop explicit. Key idea: collaboration can improve quality when agents have different responsibilities—not merely split work into sequential steps.

## Demo 6: build a routed agentic workflow

Run:

```bash
python 06_routed_workflow.py
```

[`06_routed_workflow.py`](06_routed_workflow.py) adds two classes:

- `RouterAgent` classifies each request as `housing`, `neighborhood`, or `full-search`.
- `HomeFindingWorkflow` validates the route and controls which agents run.

For `full-search`, the workflow is:

```text
route -> find listings -> evaluate neighborhoods -> recommend one option
```

The terminal trace exposes every stage rather than jumping to the final answer:

```text
User goal
  -> RouterAgent selects full-search
  -> HousingAgent returns listing research
  -> handoff: HousingAgent -> NeighborhoodAgent
  -> NeighborhoodAgent returns area research
  -> handoffs: both specialists -> RecommendationAgent
  -> RecommendationAgent produces the final answer
```

Each handoff is an ordinary Python dictionary with `from`, `to`, and `content` fields. This makes an important point visible: agents do not communicate magically; the workflow moves their messages.

The route is validated against a Python set. Unexpected model output safely falls back to `full-search`. This illustrates a durable production lesson: let the model make bounded semantic decisions, but let deterministic code enforce allowed actions.

Try these prompts by changing the string in `main()`:

- “Show me rentals under $2,500.” → `housing`
- “What is Mueller like?” → `neighborhood`
- “Help my family choose an Austin-area rental under $2,500.” → `full-search`

The reusable specialist classes live in [`agents/`](agents/), while the deterministic housing tools and sample data live in [`tools/housing_search.py`](tools/housing_search.py).

## The four-step mental model

| Demo | New capability | What is still plain Python? |
|---|---|---|
| Model call | Language generation | Function call and messages list |
| Single agent | Role, memory, tool, goal | Class, list, method |
| Collaboration | Agent handoff | Return value passed to a method |
| Workflow | Routing and coordination | Validation, branches, sequence |

## Live-demo troubleshooting

- `WEBINAR_KEY_VAULT_URL` error: export the Key Vault URL in the same terminal.
- Browser sign-in fails: verify that pop-ups are allowed, select an identity with Key Vault access, and confirm that the browser can redirect back to the local application.
- Key Vault `403`: check the role assignment, then allow a few minutes for RBAC propagation.
- Model `404`: the value of `aoai-deployment` must be the deployment name, not merely the model family name.
- Quota or region error: deploy the model in a region where your subscription has capacity.

## After the webinar

Replace one in-memory tool with a real housing or commute API, add structured JSON outputs for routing, and record a trace containing route, tool calls, latency, and final answer. Those changes improve reliability without changing the core architecture participants just built.

## Official references

- [Create an Azure OpenAI resource and deploy a model](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/create-resource)
- [Create an RBAC-enabled Key Vault with Azure CLI](https://learn.microsoft.com/en-us/azure/key-vault/general/manage-with-cli2)
- [Azure OpenAI v1 API and Python client examples](https://learn.microsoft.com/en-gb/azure/ai-foundry/foundry-models/how-to/use-chat-completions)
