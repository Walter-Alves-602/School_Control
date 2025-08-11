# Instruções para Configuração do Cliente Linux Mint (Sala Zion)

Para que o controle remoto via SSH funcione corretamente nos computadores Linux Mint da sala Zion, siga os passos abaixo em cada máquina:

## 1. Instalar o servidor SSH
Abra o terminal e execute:

```
sudo apt update
sudo apt install openssh-server -y
```

## 2. Verificar se o serviço SSH está ativo
```
systemctl status ssh
```
Se não estiver ativo, inicie com:
```
sudo systemctl start ssh
sudo systemctl enable ssh
```

## 3. Configurar o sudo para não pedir senha (opcional, mas recomendado para automação)
Edite o arquivo sudoers com:
```
sudo visudo
```
Adicione a linha (substitua `usuario` pelo nome do usuário desejado):
```
usuario ALL=(ALL) NOPASSWD:ALL
```

## 4. (Opcional) Permitir login SSH apenas na rede interna
Edite `/etc/ssh/sshd_config` e ajuste:
```
PermitRootLogin no
PasswordAuthentication yes
```
Reinicie o SSH:
```
sudo systemctl restart ssh
```

## 5. Testar a conexão
De outro computador, execute:
```
ssh usuario@IP_DO_CLIENTE
```
Se conectar sem pedir senha de sudo, a configuração está correta.

---

**Observação:**
- Mantenha o SSH restrito à rede interna para maior segurança.
- Use chaves SSH para maior segurança, se desejar.
- O usuário usado para automação deve ter senha definida.
