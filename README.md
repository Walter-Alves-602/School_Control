# Sistema de Controle de Computadores por Salas

Sistema para gerenciamento remoto de computadores organizados por salas/laboratórios,
com suporte a diferentes sistemas operacionais. Funciona para **qualquer escola**:
toda a configuração específica (rede, salas, credenciais) vem de um arquivo `.env`.

O sistema expõe uma **API (FastAPI)** para ser consumida por uma interface web (feita
separadamente) e também pode ser usado via **linha de comando** (`main.py`).

## 📁 Estrutura do Projeto

```
CCI/
├── .env                    # Configuração local desta escola (NÃO versionado)
├── .env.example            # Modelo de configuração (versionado)
├── config.py               # Carrega o .env e monta a configuração de cada sala
├── sala_config.py          # Consulta de configuração/comandos por sala
├── csv_manager.py          # Leitura do CSV com MAC, IP e Sala dos computadores
├── ssh_manager.py          # Conexões e comandos SSH
├── power_manager.py        # Wake-on-LAN e gerenciamento de energia
├── admin_tasks.py          # Tarefas administrativas por sala (desligar, reiniciar, etc)
├── computadores.csv        # Inventário de computadores (MAC, IP, Sala)
├── main.py                 # Interface de linha de comando
├── api.py                  # API FastAPI (usada pela interface web)
├── auth/                   # Autenticação e usuários (SQLite)
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py         # Hash de senha (bcrypt) e JWT
│   └── deps.py             # Dependências de autenticação/autorização
├── routers/                 # Rotas da API
│   ├── auth_router.py
│   ├── users_router.py
│   └── salas_router.py
├── scripts/
│   └── create_user.py      # Cria usuários (nome, login, senha, cargo)
└── requirements.txt
```

## ⚙️ Configuração (.env)

Copie `.env.example` para `.env` e ajuste para a sua escola:

```bash
cp .env.example .env
```

Principais variáveis:

- `SCHOOL_NAME` — nome da escola (aparece no título da API).
- `WOL_BROADCAST_IP` — IP de broadcast usado para o Wake-on-LAN.
- `COMPUTERS_CSV_PATH` — caminho do CSV com o inventário (`MAC,IP,Sala`).
- `SALAS` — lista de salas, separadas por vírgula. Deve corresponder à coluna
  `Sala` do CSV.
- `DEFAULT_SALA_OS` / `DEFAULT_SALA_USERNAME` / `DEFAULT_SALA_PASSWORD` /
  `DEFAULT_SALA_SSH_PORT` — valores usados para salas sem configuração específica.
- `SALA_<NOME>_OS` / `SALA_<NOME>_USERNAME` / `SALA_<NOME>_PASSWORD` /
  `SALA_<NOME>_SSH_PORT` — sobrescrevem a configuração padrão para uma sala
  específica (troque espaços do nome da sala por `_` e use maiúsculas).
  `OS` aceita `linux` ou `windows`; os comandos (desligar, reiniciar, atualizar,
  instalar pacote, etc) são escolhidos automaticamente a partir disso.
- `SECRET_KEY` — chave usada para assinar os tokens JWT da API. Gere uma com:
  `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_URL` — banco SQLite dos usuários (padrão: `sqlite:///./users.db`).
- `ALLOWED_CARGO` — cargo autorizado a usar o sistema (padrão: `TI`).
- `CORS_ORIGINS` — origens permitidas para a interface web consumir a API.

## 📊 Formato do CSV de computadores

```csv
MAC,IP,Sala
0A-E0-AF-AE-05-4F,35.0.0.100,Servidor
0A-E0-AF-F4-13-A1,35.0.0.101,Paris
```

## 🚀 Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # e edite com os dados da sua escola
```

## 👤 Usuários e autenticação

Os usuários (nome, login, senha e cargo) ficam em um banco SQLite. Apenas
usuários com cargo igual a `ALLOWED_CARGO` (padrão `"TI"`) conseguem usar a
API — usuários com outro cargo até fazem login, mas recebem `403`.

Crie o primeiro usuário TI:

```bash
python scripts/create_user.py --name "Fulano da Silva" --login fulano --cargo TI
```

O script pede a senha de forma interativa (não fica salva em texto puro em
nenhum arquivo).

## 🌐 Executando a API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Documentação interativa (Swagger) em `http://localhost:8000/docs`.

### Autenticação

`POST /auth/login` — recebe `username`/`password` (form, padrão OAuth2) e
retorna um token JWT:

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=fulano&password=SUA_SENHA"
```

Use o token nas demais chamadas: `Authorization: Bearer <token>`.

### Principais rotas

| Método | Rota                          | Descrição                                  |
|--------|--------------------------------|---------------------------------------------|
| POST   | `/auth/login`                 | Login, retorna token JWT                     |
| GET    | `/auth/me`                    | Dados do usuário autenticado                 |
| GET    | `/users`                      | Lista usuários (TI)                          |
| POST   | `/users`                      | Cria usuário (TI)                            |
| DELETE | `/users/{id}`                 | Remove usuário (TI)                          |
| GET    | `/salas`                      | Lista salas e quantidade de computadores     |
| GET    | `/salas/{sala}`                | Detalhe da sala e seus computadores          |
| POST   | `/salas/{sala}/wake`           | Envia Wake-on-LAN para a sala                |
| GET    | `/salas/{sala}/connectivity`   | Testa conectividade SSH da sala              |
| GET    | `/salas/{sala}/system-info`    | Coleta informações do sistema                |
| POST   | `/salas/{sala}/poweroff`       | Desliga os computadores da sala              |
| POST   | `/salas/{sala}/restart`        | Reinicia os computadores da sala             |
| POST   | `/salas/{sala}/update`         | Atualiza o sistema operacional da sala       |
| POST   | `/salas/{sala}/install`        | Instala um pacote (`{"package": "nome"}`)    |
| POST   | `/salas/{sala}/command`        | Executa comando personalizado                |

Todas as rotas acima (exceto `/auth/login`) exigem o header `Authorization`
com um token válido de um usuário TI.

## 🖥️ Uso via terminal

```bash
python main.py
```

Menu interativo com as mesmas operações disponíveis na API.

## 🔧 Sistemas operacionais suportados

Cada sala é configurada com `os = linux` ou `os = windows`; os comandos
(desligar, reiniciar, atualizar, instalar pacote, informações do sistema)
são resolvidos automaticamente a partir do modelo de comandos daquele SO,
em `config.py` (`OS_COMMAND_TEMPLATES`).

## 🚨 Importante

- `.env` e `*.db` não devem ser commitados (já estão no `.gitignore`).
- Confirme sempre antes de operações destrutivas (desligar, reiniciar) na
  interface que for construída sobre esta API.
- Teste conectividade (`/salas/{sala}/connectivity`) antes de operações em massa.
