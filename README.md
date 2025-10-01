### AutoU: Classificador Inteligente de Emails

O AutoU é um classificador de emails que usa Inteligência Artificial (IA) para categorizar mensagens como Produtivas ou Improdutivas e sugerir uma resposta automática, economizando seu tempo.

Desenvolvido com FastAPI (Python) no backend e uma interface moderna em HTML, CSS e JavaScript, com a IA fornecida pela Groq API.

----------------------------------------------------------------------------------------------------------------------

### Funcionalidades 
Classificação Inteligente: Categoriza emails como:

✅ Produtivo: Requer ação ou resposta imediata.

❌ Improdutivo: Não exige atenção urgente.

Sugestão de Resposta: Gera uma resposta curta e educada automaticamente.

Entrada Flexível: Aceita texto colado diretamente ou upload de arquivos .txt e .pdf.

Histórico Completo: Sidebar expansível com histórico dos emails classificados, permitindo gerenciamento individual ou limpeza total.

Design Moderno: Interface responsiva em tons de azul escuro, focada na usabilidade.

Sistema de Fallback: Se a IA falhar, um sistema de classificação local simples assume para garantir a operação.

--------------------------------------------------------------------------------------------------------------------

### Tecnologias Utilizadas

FastAPI -	Estrutura de API rápida e robusta (Backend Python).
Groq API - 	Motor de IA para classificação e sugestão (Modelos LLaMA 3.1 / Mixtral).
HTML + CSS + JS	- Interface do usuário (Frontend interativo e responsivo).
pdfminer.six -	Ferramenta para leitura e extração de texto de arquivos PDF.
Fallback Local	- Classificação de emergência caso a Groq API não responda.

----------------------------------------------------------------------------------------------------------------------

### Como Rodar o Projeto Localmente

1. Clone o Repositório:
- git clone <url-do-repositorio>

----------------------------------------------------------------------------------------------------------------------
2. Crie e Ative o Ambiente Virtual:
python -m venv venv
 
- Linux/macOS - source venv/bin/activate
 
- Windows - .\venv\Scripts\activate

----------------------------------------------------------------------------------------------------------------------
3. Instale as Dependências:
- pip install -r requirements.txt

----------------------------------------------------------------------------------------------------------------------

### Configuração da Groq API

Você precisará de uma chave de API para o serviço de IA.


- Obtenha sua chave gratuita: Groq Cloud
- Faça loging e procure por API Keys
- create API Keys


Copie o arquivo de exemplo e crie o .env na raiz do projeto:
cp .env.example .env


Edite o arquivo .env e adicione sua chave:
GROQ_API_KEY=sua_chave_aqui

você pode exportar a variável no seu terminal:

- Linux/macOS: export GROQ_API_KEY="sua_chave_aqui"

- Windows (PowerShell): setx GROQ_API_KEY "sua_chave_aqui"



----------------------------------------------------------------------------------------------------------------------

### Inicie o Servidor

Com as dependências e a chave configuradas, é só rodar:
uvicorn backend.main:app --reload

----------------------------------------------------------------------------------------------------------------------

### Acesse!
Abra seu navegador e acesse: http://127.0.0.1:8000

----------------------------------------------------------------------------------------------------------------------

 ### Observações de Produção
Para Deploy (em serviços como Render ou Railway), certifique-se de configurar a variável de ambiente GROQ_API_KEY no painel do serviço, em vez de usar o arquivo .env.
O sistema de Fallback (em backend/fallback.py) garante que, mesmo sem a Groq API, o aplicativo forneça uma classificação básica.
