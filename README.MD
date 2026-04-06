# 🔥 FireQuest

> Sistema completo de gamificação de produtividade: transforme sua rotina em um jogo.

---

## 🚀 Visão Geral

O **FireQuest** é uma plataforma que converte tarefas do dia a dia em **missões**, recompensando o usuário com **XP**, **ranking** e **progressão**.

Projetado com arquitetura moderna e foco em escalabilidade, o sistema integra:

* produtividade acadêmica 📚
* desenvolvimento pessoal 🧠
* exercícios físicos 💪
* metas e hábitos 🎯

---

## 🧠 Conceito

Cada tarefa é tratada como uma missão:

* 🎯 Dificuldade (0–10)
* ⏱ Urgência (0–10)

📌 Cálculo:

XP = dificuldade + urgência

### Regras:

* atraso → -50% XP
* validação → XP proporcional
* XP acumulado → ranking global

---

## 🏗️ Arquitetura

```bash
/backend   → API (FastAPI)
/frontend  → Web (React)
/mobile    → App (React Native)
```

---

## ⚙️ Tecnologias

### Backend

* FastAPI
* SQLAlchemy
* JWT (Autenticação)

### Frontend

* React

### Mobile

* React Native

---

## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Token)**.

Após login:

```http
Authorization: Bearer <token>
```

Todas as rotas protegidas exigem esse token.

---

## 📡 API

Documentação interativa:

```bash
http://127.0.0.1:8000/docs
```

---

## 🎮 Funcionalidades

### 👤 Usuários

* Cadastro e login
* Perfil
* Ranking global

---

### 🎯 Missões

* Criar missão
* Definir dificuldade e urgência
* Concluir missão
* Ganhar XP

---

### 📊 Sistema de XP

* cálculo automático
* penalidade por atraso
* validação proporcional

---

### 🏆 Ranking

* leaderboard global
* ordenação por XP

---

### 📜 Histórico

* registro de missões concluídas
* data de conclusão

---

### 🎯 Metas

* metas diárias
* metas personalizadas

---

## 📦 Padrão de Resposta da API

### ✅ Sucesso

```json
{
  "success": true,
  "data": {}
}
```

### ❌ Erro

```json
{
  "success": false,
  "error": "mensagem"
}
```

---

## ⚙️ Como rodar o projeto

### 1. Clonar

```bash
git clone https://github.com/seu-usuario/firequest.git
cd firequest/backend
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar ambiente

```bash
cp .env.example .env
```

---

### 5. Rodar servidor

```bash
python -m uvicorn app.main:app --reload
```

---

## 📁 Estrutura do Projeto

```bash
backend/
frontend/
mobile/
```

---

## 🎨 Design (Frontend)

Interface inspirada em HUD futurista:

* azul neon
* fundo escuro
* glassmorphism
* efeitos glow

---

## 🧩 Integração

Frontend e mobile consomem a API central:

```text
Frontend → API → Banco
Mobile   → API → Banco
```

---

## ⚠️ Boas práticas

* Nunca subir `.env`
* Nunca expor `SECRET_KEY`
* Sempre usar token nas requisições
* Backend centraliza toda lógica

---

## 🚀 Roadmap

* [x] Backend completo
* [ ] Frontend web
* [ ] App mobile

---

## 👨‍💻 Equipe

* GuiPaicheco
* Itevee

---

## 💡 Status

🟢 Backend finalizado
🟡 Mobile em desenvolvimento
🔴 Frontend a desenvolver

---

## 🔥 FireQuest

> “Transforme sua rotina em progresso.”
