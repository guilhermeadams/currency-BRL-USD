# Currency Exchange Rate Dashboard

Este é um aplicativo de dashboard para visualizar as taxas de câmbio entre o Real (BRL) e o Dólar Americano (USD) em tempo real e histórico. O aplicativo é construído usando **FastAPI** para o backend e uma página **HTML** para o frontend.

## Funcionalidades

- **Última Taxa de Câmbio**: Consulta a taxa de câmbio mais recente de BRL para USD.
- **Taxas Históricas**: Consulta as taxas de câmbio históricas para um intervalo de datas específico ou para um determinado número de dias anteriores.
- **Dashboard Interativo**: Visualiza as informações em um gráfico de linha para fácil análise.

## Arquitetura do Projeto

A versão inicial do projeto possui a seguinte estrutura simples:

```
currency_service/
├── main.py                  # Arquivo principal da aplicação FastAPI
├── static/
│   └── index.html           # Página HTML do frontend
├── tests/
│   └── test_main.py         # Testes unitários para o backend
└── requirements.txt         # Lista de dependências do projeto
```

### Diagrama de Arquitetura

```plaintext
                    ┌─────────────────────────────────────────────────────┐
                    │                      FastAPI                        │
                    │                                                     │
                    │  ┌───────────────────────────────────────────────┐  │
                    │  │                  Endpoints                    │  │
                    │  │    /api/latest       /api/historical          │  │
                    │  └───────────────────────────────────────────────┘  │
                    │                │                      │             │
                    │                │                      │             │
                    │   ┌────────────▼───────────┐   ┌──────▼───────────┐ │
                    │   │ Async HTTP Client      │   │  Scheduler       │ │
                    │   │ (AwesomeAPI)           │   │ (Periodic Fetch) │ │
                    │   └────────────────────────┘   └──────────────────┘ │
                    │                     │                               │
                    │                     ▼                               │
                    │       ┌─────────────────────────────┐               │
                    │       │       Database Interface    │               │
                    │       │ (Mocked, Replaceable with   │               │
                    │       │   Actual Database Access)   │               │
                    │       └─────────────────────────────┘               │
                    └─────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                    ┌────────────────┐
                                    │   Frontend     │
                                    │ (HTML + JS)    │
                                    └────────────────┘
```

### 1. `main.py`

Este arquivo é o ponto de entrada da aplicação FastAPI. Ele configura a instância do FastAPI, define as rotas para as APIs, configura o middleware de CORS, e monta os arquivos estáticos para servir a interface HTML.

- **Rota `/api/latest`**: Busca a taxa de câmbio mais recente de BRL para USD utilizando uma API pública.
- **Rota `/api/historical`**: Busca as taxas de câmbio históricas de acordo com o intervalo de datas fornecido ou o número de dias.
- **Rota `/`**: Serve o arquivo `index.html` para o frontend.

### 2. `static/index.html`

Este arquivo HTML é o frontend do aplicativo, proporcionando uma interface de usuário que permite visualizar a taxa de câmbio atual e as taxas históricas em um gráfico interativo.

- **JavaScript**: Utiliza scripts para buscar dados da API e atualizá-los dinamicamente no gráfico.
- **CSS**: Estiliza a página para uma apresentação limpa e intuitiva.

### 3. `tests/test_main.py`

Este arquivo contém testes unitários para verificar o funcionamento correto das rotas do backend.

- **Testes**: Verificam se as respostas das rotas `/api/latest` e `/api/historical` estão corretas e se os erros são tratados adequadamente.

## Requisitos

- Python 3.7 ou superior
- Pip (gerenciador de pacotes do Python)

## Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/currency_service.git
cd currency_service
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**

- **Windows:**

  ```bash
  venv\Scriptsctivate
  ```

- **Linux/MacOS:**

  ```bash
  source venv/bin/activate
  ```

4. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

## Execução

1. **Inicie o aplicativo:**

```bash
uvicorn main:app --reload
```

2. **Abra o navegador e acesse o seguinte URL:**

```
http://127.0.0.1:8000/
```

## Testes

Para executar os testes automatizados:

```bash
pytest tests/
```

## Explicação da Arquitetura

A arquitetura inicial é simples e direta, com apenas três componentes principais:

- **Backend (`main.py`)**: Define todas as rotas e a lógica para buscar dados da API externa.
- **Frontend (`index.html`)**: Fornece uma interface de usuário interativa para visualizar as taxas de câmbio.
- **Testes (`test_main.py`)**: Garante que a API funciona corretamente e trata os erros de maneira adequada.

Esta arquitetura permite fácil desenvolvimento e testes iniciais do aplicativo, enquanto mantém a possibilidade de expansão futura para novos recursos e módulos.

## Melhorias Futuras

- **Modularização**: Separar as responsabilidades em múltiplos arquivos para melhorar a manutenção e escalabilidade.
- **Suporte a Múltiplas Moedas**: Adicionar suporte para outras moedas além do BRL e USD.
- **Autenticação**: Implementar autenticação para proteger as APIs.

## Contribuição

Sinta-se à vontade para contribuir com este projeto! Faça um fork do repositório, crie um branch com sua feature ou correção de bug, e envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para obter mais detalhes.
