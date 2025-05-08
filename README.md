# 🧰 TCP Proxy em Python

Este projeto implementa um **proxy TCP** escrito em Python. Ele permite interceptar, modificar e monitorar pacotes entre um cliente e um servidor remoto — ideal para testes, debugging ou análise de tráfego.

---

## ⚙️ Funcionalidades

- Interceptação de tráfego bidirecional
- Impressão do conteúdo em formato **hex dump**
- Threads para conexões simultâneas
- Buffer de recebimento configurável
- Funções de manipulação de requisição e resposta
- Detecção de fim de conexão

---

## 📌 Uso


python proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]

🔍 Exemplo
bash
Copiar
Editar
python proxy.py 127.0.0.1 9000 10.12.132.1 9000 True
receive_first: define se o proxy deve receber dados do servidor remoto antes de enviar algo do cliente.

🔎 Funções principais
hexdump(): exibe o tráfego interceptado no formato hexadecimal

proxy_handler(): lida com o fluxo entre cliente e servidor

receive_from(): coleta dados de forma segura com timeout

request_handler() / response_handler(): pontos ideais para injetar/modificar pacotes
