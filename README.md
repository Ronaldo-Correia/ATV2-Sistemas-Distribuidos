# 🖥️ SIMULADOR DE SISTEMA DISTRIBUÍDO COM RELÓGIO DE LAMPORT E CAPTURA DE ESTADO GLOBAL

## 🔎 VISÃO GERAL

Este projeto tem como objetivo implementar uma simulação distribuída com três processos que se comunicam via sockets TCP, integrando conceitos fundamentais de sistemas distribuídos, como RELÓGIO LÓGICO DE LAMPORT e o algoritmo de CAPTURA DE ESTADO GLOBAL DE CHANDY-LAMPORT.

## ⚙️ FUNCIONALIDADES

- Implementação de três processos simulando quiosques autônomos de pedidos em uma praça de alimentação.
- Comunicação entre processos via sockets TCP.
- Relógio de Lamport para eventos internos, envio e recebimento de mensagens.
- Captura de estado global com algoritmo de Chandy-Lamport.
- Registro de eventos e timestamps em logs.
- Snapshot do estado local e mensagens em trânsito.

## 🧱 ARQUITETURA

- LINGUAGEM: Java  
- MODELO DE COMUNICAÇÃO: Cliente-Servidor com Sockets TCP  
- TRÊS PROCESSOS: representando quiosques (ProcessoA, ProcessoB, ProcessoC)  
- UM DOS PROCESSOS: é responsável por iniciar a captura de snapshot

## ▶️ EXECUÇÃO

Cada processo pode ser executado independentemente:

- java ProcessoA
- java ProcessoB
- java ProcessoC



## ⏱️ RELÓGIO DE LAMPORT
O Relógio de Lamport é utilizado para garantir a ordenação causal entre eventos em um sistema distribuído. Cada processo mantém um contador que:

É incrementado a cada evento interno.

É incrementado ao enviar mensagens.

É atualizado para max(local, recebido) + 1 ao receber mensagens.

Os timestamps de Lamport são registrados nos logs dos eventos e ajudam a analisar a sequência de eventos no sistema.

## 📸 CAPTURA DE ESTADO GLOBAL (CHANDY-LAMPORT)
A captura de estado é realizada com os seguintes passos:

Um processo inicia o snapshot e grava seu estado local.

Envia mensagens de marcador ("marker") para todos os canais de saída.

Ao receber o primeiro marcador, os outros processos gravam seu estado local e propagam o marcador.

Os processos registram todas as mensagens recebidas entre o registro de estado local e o recebimento do marcador.

Após receber marcador de todos os canais, o processo considera seu snapshot completo.

O resultado do snapshot inclui:

Estado local de cada processo.

Mensagens em trânsito em cada canal.

##  📜 LOGS E REGISTROS
Os eventos gerados por cada processo (internos, envio e recebimento de mensagens) são registrados com seus timestamps em arquivos de log ou na saída do terminal, permitindo:

Verificar a ordem dos eventos conforme o relógio de Lamport.

Analisar o estado capturado globalmente.

##  📁 REPOSITÓRIO
O código-fonte completo está disponível em:
https://github.com/seu-usuario/simulador-distribuido

##  ✅ REQUISITOS
Java 8 ou superior

Sistema operacional compatível com sockets TCP

##  👨‍💻 AUTORES
Ronaldo Correia

Marcelo de Jesus
