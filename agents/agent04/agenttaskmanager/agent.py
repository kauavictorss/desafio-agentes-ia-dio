from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# Suas credenciais (devem estar no arquivo .env)
API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')

def get_temporal_context():
    """Retorna a data e hora atual formatada."""
    now = datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S')

def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str = None):
    """Cria um novo card no board 'DESAFIO DIO AGENT IA' na lista 'A FAZER'."""
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )
        
        boards = client.list_boards()
        # Busca o board ignorando maiúsculas/minúsculas
        meu_board = next((b for b in boards if b.name.strip().upper() == 'DESAFIO DIO AGENT IA'), None)
        
        if not meu_board:
            nomes_boards = ", ".join([f"'{b.name}'" for b in boards])
            return f"❌ Erro: Board 'DESAFIO DIO AGENT IA' não encontrado. Encontrei: {nomes_boards}"

        listas = meu_board.list_lists()
        # Busca a lista 'A FAZER' ou 'TO DO' ignorando maiúsculas/minúsculas
        minha_lista = next((l for l in listas if l.name.strip().upper() in ['A FAZER', 'TO DO', 'TODO']), None)
        
        if not minha_lista:
            nomes_listas = ", ".join([f"'{l.name}'" for l in listas])
            return f"❌ Erro: Lista 'A FAZER' não encontrada no board. Encontrei: {nomes_listas}"
        
        card = minha_lista.add_card(
            name=nome_da_task,
            desc=descricao_da_task,
            due=due_date
        )
        return f"✅ Tarefa '{nome_da_task}' adicionada com sucesso!"
    except Exception as e:
        return f"❌ Erro ao adicionar tarefa: {str(e)}"

def listar_tarefas(status: str = "todas"):
    """Lista as tarefas do board filtradas por status."""
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = next((b for b in boards if b.name.strip().upper() == 'DESAFIO DIO AGENT IA'), None)
        
        if not meu_board:
            return "❌ Board 'DESAFIO DIO AGENT IA' não encontrado."
            
        listas = meu_board.list_lists()        

        status_norm = status.lower().strip()
        if status_norm == "todas":
            listas_filtradas = listas
        elif status_norm in ["a fazer", "todo"]:
            listas_filtradas = [l for l in listas if l.name.strip().upper() in ['A FAZER', 'TO DO', 'TODO']]
        elif status_norm in ["em andamento", "doing"]:
            listas_filtradas = [l for l in listas if l.name.strip().upper() in ['EM ANDAMENTO', 'DOING']]
        elif status_norm in ["concluido", "done", "concluído"]:
            listas_filtradas = [l for l in listas if l.name.strip().upper() in ['CONCLUÍDO', 'CONCLUIDO', 'DONE']]
        else:
            listas_filtradas = listas

        tarefas = []
        for lista in listas_filtradas:
            cards = lista.list_cards()
            for card in cards:
                tarefas.append({
                    "nome": card.name,
                    "descricao": card.desc,
                    "vencimento": card.due,
                    "status": lista.name
                })
        
        return tarefas if tarefas else "Nenhuma tarefa encontrada."
    except Exception as e:
        return f"❌ Erro ao listar tarefas: {str(e)}"

def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    """Move uma tarefa para um novo status (a fazer, em andamento, concluido)."""
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = next((b for b in boards if b.name.strip().upper() == 'DESAFIO DIO AGENT IA'), None)
        
        if not meu_board:
            return "❌ Board não encontrado."

        listas = meu_board.list_lists()
                       
        status_map = {
            "a fazer": ["A FAZER", "TO DO", "TODO"],
            "em andamento": ["EM ANDAMENTO", "DOING"],
            "concluido": ["CONCLUÍDO", "CONCLUIDO", "DONE"]
        }
        
        opcoes_destino = status_map.get(novo_status.lower().strip())
        if not opcoes_destino:
            return "❌ Status inválido. Use: 'a fazer', 'em andamento' ou 'concluido'"
        
        lista_destino = next((l for l in listas if l.name.strip().upper() in opcoes_destino), None)
        if not lista_destino:
            return f"❌ Lista de destino para '{novo_status}' não encontrada."
        
        card_encontrado = None
        for lista in listas:
            cards = lista.list_cards()
            card_encontrado = next((c for c in cards if c.name.lower().strip() == nome_da_task.lower().strip()), None)
            if card_encontrado: break
        
        if not card_encontrado:
            return f"❌ Tarefa '{nome_da_task}' não encontrada em nenhuma lista."
        
        card_encontrado.change_list(lista_destino.id)
        return f"✅ '{nome_da_task}' movida para {novo_status}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de Organização de Tarefas',
    instruction="""
        Você é um assistente pessoal de organização de tarefas especializado no Trello.
        Sua missão é ajudar o usuário a gerenciar seu dia de forma eficiente.
        
        REGRAS DE INTERAÇÃO:
        1. Assim que for ativado, use 'get_temporal_context' para saber a data e hora atual.
        2. Inicie a conversa saudando o usuário, informando a data e perguntando: "Quais são as suas tarefas para hoje?".
        3. Para cada tarefa dita pelo usuário, use 'adicionar_tarefa' para criar um card no board 'DESAFIO DIO AGENT IA'.
        4. Após adicionar uma tarefa, pergunte: "Tem mais alguma tarefa que deseja organizar?".
        5. Continue até que o usuário diga que não tem mais nada.
        6. Você também pode listar tarefas existentes ou mudar o status delas se o usuário solicitar.
        7. Seja sempre organizado, proativo e educado.
    """,
    tools=[get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa],
)
