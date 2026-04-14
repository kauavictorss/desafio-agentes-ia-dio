# Desafio Agentes de IA - Organizador de Tarefas Trello 📋

Este projeto faz parte do desafio prático do bootcamp **CI&T - Do Prompt ao Agente** da **Digital Innovation One (DIO)**, no módulo **Criando Agentes de IA**.

O objetivo é desenvolver um agente inteligente capaz de interagir com APIs externas (Trello) para automatizar a organização de tarefas diárias, utilizando o framework **Google ADK** e o modelo **Gemini 2.5 Flash**.

---

## 🎯 Objetivo do Projeto
Criar um assistente pessoal que:
1.  Inicie a conversa perguntando sobre as tarefas do dia.
2.  Adicione automaticamente novos cards ao Trello com nome e descrição.
3.  Permita listar tarefas existentes filtradas por status.
4.  Possibilite a movimentação de tarefas entre colunas (A Fazer -> Em Andamento -> Concluído).

---

## 🛠️ Pré-requisitos e Requisitos Técnicos
Para executar este projeto, você precisará de:
- **Python 3.10+** instalado.
- Uma conta ativa no **Trello**.
- Uma chave de API do **Google Gemini** (obtida no Google AI Studio).
- O framework **Google ADK** instalado (`pip install google-adk`).

---

## 🚀 Passo a Passo para Execução

### 1. Preparação do Ambiente Virtual
Clone o repositório e configure o ambiente:
```bash
# Entrar na pasta do projeto
cd desafio-agentes-ia-dio

# Criar o ambiente virtual
python -m venv .lab-dio

# Ativar o ambiente (Windows)
.\.lab-dio\Scripts\activate

# Ativar o ambiente (Linux/Mac)
source .lab-dio/bin/activate
```

### 2. Instalação das Dependências
```bash
python -m pip install -r agents/agent04/requirements.txt
```

### 3. Configuração das Chaves de API (.env)
O agente utiliza variáveis de ambiente para se conectar ao Google e ao Trello. Configure o arquivo `.env` localizado em `agents/agent04/agenttaskmanager/`:

```env
GOOGLE_API_KEY=sua_chave_gemini
TRELLO_API_KEY=sua_chave_trello
TRELLO_API_SECRET=seu_secret_trello
TRELLO_TOKEN=seu_token_trello
```
> **Dica:** Obtenha suas chaves do Trello em [trello.com/app-key](https://trello.com/app-key).

### 4. Preparação do Trello
Para que o agente funcione corretamente, crie no seu Trello:
- Um Quadro chamado: **DESAFIO DIO AGENT IA**
- Três listas: **A FAZER**, **EM ANDAMENTO** e **CONCLUÍDO**.

### 5. Execução do Chat
Para interagir com o agente via interface web:
```bash
# Entre na pasta do agente
cd agents/agent04/agenttaskmanager

# Inicie a interface de chat
adk web
```

---

## 📚 Bootcamp CI&T - Do Prompt ao Agente
Este projeto demonstra a aplicação prática de:
- **Engenharia de Prompt:** Instruções estruturadas para o agente.
- **Tools/Function Calling:** Capacidade do LLM de executar funções Python reais.
- **Integração de APIs:** Conexão entre IA Generativa e ferramentas de produtividade.

---

Desenvolvido por você como parte da jornada de aprendizado na **DIO** em parceria com a **CI&T**.
