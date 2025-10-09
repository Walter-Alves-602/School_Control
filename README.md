# Sistema de Controle de Computadores por Salas

Sistema avançado para gerenciamento remoto de computadores organizados por salas/laboratórios, com suporte a diferentes sistemas operacionais e configurações específicas por ambiente.

## 🆕 NOVA VERSÃO - Sistema Baseado em Salas

Esta versão foi completamente reformulada para trabalhar com **salas/laboratórios**, onde cada sala pode ter:
- Sistema operacional diferente (Linux Mint, Ubuntu Server, Windows 10)
- Credenciais específicas
- Porta SSH personalizada
- Comandos otimizados por sistema

## 📁 Estrutura do Projeto

```
CCI/
├── main.py                 # Interface principal do sistema
├── csv_manager.py          # Gerenciamento do CSV com MACs, IPs e Salas
├── ssh_manager.py          # Conexões e comandos SSH por sala
├── admin_tasks.py          # Tarefas administrativas por sala
├── power_manager.py        # Wake-on-LAN e gerenciamento de energia
├── sala_config.py          # Configurações específicas por sala
├── computadores.csv        # Arquivo com MAC, IP e Sala dos computadores
├── teste_sistema.py        # Teste rápido do sistema
└── README.md              # Este arquivo
```

## 📊 Formato do CSV

O arquivo `computadores.csv` deve ter o formato:

```csv
MAC,IP,Sala
0A-E0-AF-AE-05-4F,35.0.0.100,Servidor
0A-E0-AF-F4-13-A1,35.0.0.101,Paris
0A-E0-AF-D1-01-1B,35.0.0.136,Zion
C0-7C-D1-A9-FD-59,35.0.0.172,Monitoria
```

## ⚙️ Configuração por Salas

No arquivo `sala_config.py`, configure cada sala:

```python
SALAS_CONFIG = {
    "Paris": {
        "os": "Linux Mint",
        "username": "aluno", 
        "password": "in12345678",
        "ssh_port": 22
    },
    "Zion": {
        "os": "Linux Mint",
        "username": "aluno",
        "password": "in12345678", 
        "ssh_port": 22
    },
    "Servidor": {
        "os": "Ubuntu Server",
        "username": "admin",
        "password": "admin123",
        "ssh_port": 22
    },
    "Monitoria": {
        "os": "Windows 10",
        "username": "administrator",
        "password": "win123",
        "ssh_port": 22
    }
}
```

## 🚀 Como Usar

### 1. Interface Principal
```bash
python main.py
```

### 2. Teste Rápido
```bash
python teste_sistema.py
```

### 3. Funções Principais

#### Wake-on-LAN por Sala
```python
from csv_manager import wake_computers_by_sala
success = wake_computers_by_sala("Paris")
```

#### Comandos SSH por Sala
```python
from ssh_manager import execute_ssh_command_by_sala
results = execute_ssh_command_by_sala("hostname", "Zion")
```

#### Tarefas Administrativas
```python
from admin_tasks import poweroff_sala, restart_sala, get_system_info_sala

# Desligar todos os computadores de uma sala
poweroff_sala("Paris")

# Reiniciar uma sala
restart_sala("Zion") 

# Informações do sistema
get_system_info_sala("Servidor")
```

## 📋 Menu Principal

O sistema oferece um menu interativo com as seguintes opções:

1. **Listar salas disponíveis** - Mostra todas as salas e quantidades
2. **Wake-on-LAN por sala** - Acorda computadores de uma sala específica
3. **Testar conectividade SSH** - Verifica quais computadores estão online
4. **Informações do sistema** - Coleta dados dos computadores
5. **Desligar computadores** - Desliga todos os computadores de uma sala
6. **Reiniciar computadores** - Reinicia todos os computadores
7. **Atualizar sistemas** - Executa atualizações do sistema operacional
8. **Instalar pacote** - Instala software em todos os computadores
9. **Comando personalizado** - Executa qualquer comando
10. **Manter acordado** - Previne suspensão temporariamente
11. **Relatório completo** - Diagnóstico detalhado de uma sala

## 🔧 Características por Sistema Operacional

### Linux Mint / Ubuntu Server
- Comandos: `apt`, `systemctl`, `poweroff`, `reboot`
- SSH nativo
- Gerenciamento completo via terminal

### Windows 10
- Comandos: `shutdown`, `choco install`, `sfc`
- SSH via OpenSSH Server
- Comandos adaptados para PowerShell/CMD

## 🛠️ Dependências

```bash
pip install paramiko
```

## 📈 Funcionalidades Avançadas

### 1. Validação Automática
- Verifica se salas existem no CSV
- Valida configurações antes de executar
- Mostra informações detalhadas de cada operação

### 2. Relatórios Detalhados
- Status de conectividade por IP
- Resumo de operações executadas
- Informações específicas por sistema operacional

### 3. Segurança
- Confirmação para operações destrutivas
- Senhas por sala (não hardcoded)
- Timeout configurável para conexões

### 4. Flexibilidade
- Suporte a múltiplos sistemas operacionais
- Comandos adaptativos por plataforma
- Configuração modular por sala

## 🔍 Diagnóstico e Troubleshooting

### Teste de Conectividade
```python
from ssh_manager import test_ssh_connection_by_sala
connectivity = test_ssh_connection_by_sala("Paris")
```

### Verificar Configurações
```python
from sala_config import get_sala_config
config = get_sala_config("Zion")
print(config)
```

### Validar CSV
```python
from csv_manager import list_salas_summary
salas = list_salas_summary()
print(salas)
```

## 📚 Migração da Versão Anterior

Se você tinha o sistema antigo com formato `MAC,IP`:

1. Adicione a coluna `Sala` ao seu CSV
2. Configure as salas no `sala_config.py`
3. Use as novas funções `*_by_sala()`

As funções antigas ainda funcionam para compatibilidade.

## 🎯 Casos de Uso

- **Laboratórios de Informática**: Gerenciamento de múltiplas salas com sistemas diferentes
- **Centros de Treinamento**: Controle remoto de ambientes específicos
- **Empresas**: Administração de departamentos com configurações distintas
- **Escolas**: Gerenciamento de laboratórios por disciplina

## 🚨 Importante

- Sempre confirme operações destrutivas (desligar, reiniciar)
- Teste conectividade antes de operações em massa
- Mantenha backups das configurações
- Use timeouts apropriados para sua rede

## 📞 Suporte

Para problemas ou dúvidas:
1. Execute `python teste_sistema.py` para diagnóstico
2. Verifique os logs de erro no terminal
3. Confirme se as configurações das salas estão corretas
4. Teste conectividade SSH manualmente se necessário

## 📁 Estrutura dos Módulos

### 🔌 `ssh_manager.py` - Gerenciamento SSH
- **`execute_ssh_command_on_multiple_hosts()`** - Executa comandos SSH em múltiplos computadores
- **`generate_ip_range()`** - Gera sequências de IPs

**Exemplo:**
```python
from ssh_manager import execute_ssh_command_on_multiple_hosts, generate_ip_range

# Gerar IPs e executar comando
ips = generate_ip_range("192.168.1", 10, 20)
results = execute_ssh_command_on_multiple_hosts(
    command="hostname",
    ip_generator=ips,
    password="senha",
    username="usuario"
)
```

### ⚡ `power_manager.py` - Gerenciamento de Energia
- **`wake_on_lan()`** - Envia pacote Wake-on-LAN
- **`prevent_sleep()`** - Previne suspensão dos computadores
- **`enable_sleep()`** - Reabilita suspensão
- **`keep_awake_temporarily()`** - Mantém acordado por período específico

**Exemplo:**
```python
from power_manager import wake_on_lan, prevent_sleep

# Acordar computador específico
wake_on_lan("AA:BB:CC:DD:EE:FF")

# Prevenir suspensão em range de IPs
ips = generate_ip_range("192.168.1", 10, 20)
prevent_sleep(ips, "senha", "usuario")
```

### 📄 `csv_manager.py` - Gerenciamento de Arquivo CSV
- **`load_macs_from_csv()`** - Carrega dados MAC/IP do CSV
- **`get_macs_only()`** - Retorna apenas lista de MACs
- **`get_ips_only()`** - Retorna apenas lista de IPs
- **`get_mac_ip_dict()`** - Retorna dicionário {IP: MAC}
- **`wake_all_computers_from_csv()`** - Wake-on-LAN para todos do CSV
- **`find_mac_by_ip()`** - Busca MAC por IP
- **`find_ip_by_mac()`** - Busca IP por MAC

**Exemplo:**
```python
from csv_manager import get_ips_only, wake_all_computers_from_csv

# Obter IPs do arquivo
ips = get_ips_only("macs.csv")

# Acordar todos os computadores do CSV
wake_all_computers_from_csv("macs.csv")
```

### 🛠️ `admin_tasks.py` - Tarefas Administrativas
- **`execute_poweroff()`** - Desliga computadores
- **`install_package()`** - Instala pacotes via apt
- **`install_clonezilla()`** - Instala Clonezilla especificamente
- **`get_system_info()`** - Coleta informações do sistema
- **`update_all_systems()`** - Atualiza sistemas operacionais
- **`restart_computers()`** - Reinicia computadores
- **`execute_on_all_from_csv()`** - Executa comando em todos do CSV

**Exemplo:**
```python
from admin_tasks import install_clonezilla, execute_poweroff
from csv_manager import get_ips_only

# Instalar clonezilla em todos
ips = get_ips_only("macs.csv")
install_clonezilla(iter(ips), "senha", "usuario")

# Desligar todos os computadores
execute_poweroff(iter(ips), "senha", "usuario")
```

## 🚀 Como Usar

### 1. Arquivo Principal
Execute o `main_new.py` para ver exemplos e testar o sistema:
```bash
python main_new.py
```

### 2. Uso Modular
Importe apenas os módulos que precisar:
```python
# Para tarefas básicas SSH
from ssh_manager import execute_ssh_command_on_multiple_hosts

# Para trabalhar com CSV
from csv_manager import get_ips_only, wake_all_computers_from_csv

# Para tarefas administrativas
from admin_tasks import install_package, execute_poweroff
```

### 3. Exemplos Práticos

#### Acordar todos os computadores:
```python
from csv_manager import wake_all_computers_from_csv
wake_all_computers_from_csv("macs.csv")
```

#### Instalar software em todos:
```python
from csv_manager import get_ips_only
from admin_tasks import install_package

ips = get_ips_only("macs.csv")
install_package(iter(ips), "senha", "clonezilla", "usuario")
```

#### Executar comando personalizado:
```python
from csv_manager import get_ips_only
from ssh_manager import execute_ssh_command_on_multiple_hosts

ips = get_ips_only("macs.csv")
results = execute_ssh_command_on_multiple_hosts(
    command="df -h",
    ip_generator=iter(ips),
    password="senha",
    username="usuario"
)
```

## 📋 Formato do Arquivo CSV

O arquivo `macs.csv` deve ter o formato:
```
MAC_ADDRESS,IP_ADDRESS
0A-E0-AF-A2-12-53,35.0.0.152
00-E0-4C-DC-07-05,35.0.0.170
```

## ⚙️ Configuração

Edite as variáveis no início dos arquivos:
- **USERNAME**: Nome do usuário padrão
- **PASSWORD**: Senha padrão
- **CSV_FILE**: Caminho para o arquivo CSV

## 🔧 Dependências

```bash
pip install paramiko
```

## 📁 Estrutura de Arquivos

```
CCI/
├── main_new.py          # Arquivo principal com exemplos
├── ssh_manager.py       # Gerenciamento SSH
├── power_manager.py     # Gerenciamento de energia/Wake-on-LAN
├── csv_manager.py       # Gerenciamento de arquivo CSV
├── admin_tasks.py       # Tarefas administrativas
├── macs.csv            # Arquivo com MACs e IPs
├── requirements.txt    # Dependências
└── README.md          # Esta documentação
```

## 🎯 Vantagens da Estrutura Modular

- ✅ **Organização**: Cada módulo tem responsabilidade específica
- ✅ **Reutilização**: Importe apenas o que precisar
- ✅ **Manutenção**: Fácil de encontrar e modificar funções
- ✅ **Escalabilidade**: Fácil adicionar novas funcionalidades
- ✅ **Legibilidade**: Código mais limpo e compreensível