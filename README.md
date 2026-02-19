# 🏦 Maze Bank - Full Stack Banking
**O Maze Bank é uma aplicação completa que simula um sistema bancário real. Ele une um Backend robusto focado em integridade financeira e segurança com um Frontend moderno e responsivo.**

## 🏗️ Arquitetura do Projeto
**O repositório está dividido em dois módulos principais:**

```text
Maze_Bank_Site/
├── backend/    # API REST construída com FastAPI e Python
└── frontend/   # Interface do usuário construída com Vue 3 e Vite
```
## 🛠️ Tecnologias Utilizadas

### 🎨 Frontend
* **Vue 3 + Vite**: Performance e reatividade.

* **Bootstrap 5**: Estilização rápida e responsiva.

* **Vue Router**: Navegação em Single Page Application (SPA).

* **Axios**: Integração com a API.

* **Vue-the-mask**: Máscaras de input para CPF e Telefone.

### ⚙️ Backend
* **FastAPI**: Endpoints assíncronos e documentação automática (Swagger).

* **SQLAlchemy + SQLite**: Persistência de dados e ORM.

* **JWT (JSON Web Token)**: Autenticação e segurança de rotas.

* **Bcrypt**: Hashing seguro de senhas.

## 🚀 Como Executar o Projeto
**Para rodar a aplicação completa, você precisará de dois terminais abertos.**

### 1️⃣ Configurando o Backend
```Bash
cd backend
python -m venv venv # Windows
# ou
source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
# Siga as instruções do .env no README do backend
uvicorn app.main:app --reload
```
### 2️⃣ Configurando o Frontend
```Bash
cd frontend
npm install
npm run dev
```

**Nota: Certifique-se de que a baseURL no arquivo src/api/axios.js do frontend aponta para o endereço do backend (geralmente http://localhost:8000).**

## 📉 Próximos Passos (Roadmap Unificado)
**Abaixo estão as metas de evolução para ambos os módulos:**

### 🎨 Módulo Backend
- [ ] **Testes Automatizados**: Implementação com Pytest.

- [ ] **Docker**: Containerização completa da solução.

- [ ] **Redis**: Cache para transações temporárias.

### ⚙️ Módulo Frontend
- [ ] **Gerenciamento de Estado**: Implementar Pinia para dados do usuário.

- [ ] **Dark Mode**: Alternância de temas via CSS Variables.

- [ ] **Skeleton Screens**: Melhorar a UX durante carregamentos assíncronos.

- [ ] **Internacionalização** (i18n): Suporte para Português e Inglês.

##  🔐 Segurança e Privacidade
**O projeto segue premissas da LGPD, aplicando máscara automática de CPF em extratos e utilizando criptografia de ponta a ponta para dados sensíveis.**

## ✒️ Autores
**Lucas Dos Santos Francisco**