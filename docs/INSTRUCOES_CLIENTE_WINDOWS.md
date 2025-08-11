# Instruções para Configuração do Cliente Windows (Sala Paris)

Para que o controle remoto via WinRM funcione corretamente nos computadores Windows 10 da sala Paris, siga os passos abaixo em cada máquina:

## 1. Habilitar o WinRM
Abra o PowerShell como Administrador e execute:

```
winrm quickconfig -q
winrm set winrm/config/winrs @{MaxMemoryPerShellMB="1024"}
winrm set winrm/config @{MaxTimeoutms="1800000"}
winrm set winrm/config/service @{AllowUnencrypted="true"}
winrm set winrm/config/service/auth @{Basic="true"}
```

## 2. Permitir conexões remotas
Ainda no PowerShell, execute:

```
Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value true
Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value true
```

## 3. Liberar a porta 5985 no firewall
Execute:

```
netsh advfirewall firewall add rule name="WinRM HTTP" dir=in action=allow protocol=TCP localport=5985
```

## 4. (Opcional) Definir senha para o usuário
Certifique-se de que o usuário que será usado para autenticação remota possui senha definida.

## 5. Testar a conexão
De outro computador, teste a conexão com:

```
winrs -r:http://IP_DO_CLIENTE:5985 -u:USUARIO -p:SENHA cmd
```

Se aparecer o prompt remoto, a configuração está correta.

---

**Observação:**
- O WinRM por padrão não é seguro para redes públicas. Use apenas em redes internas e confiáveis.
- Para ambientes de domínio, as configurações podem ser feitas via GPO.
