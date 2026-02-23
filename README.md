# 🏦 Maze Bank - Full Stack Banking
**O Maze Bank é uma aplicação completa que simula um sistema bancário real. Ele une um Backend robusto focado em integridade financeira e segurança com um Frontend moderno e responsivo.**

<img width="450" height="450" src="https://github.com/user-attachments/assets/ffa20ed0-6bf8-4303-99cd-08b571e709a1" />
<img width="450" height="450" src="https://github.com/user-attachments/assets/ece2b39c-7340-4444-8d7c-4e9062969d22" />

## 🏗️ Arquitetura do Projeto
**O repositório está dividido em dois módulos principais:**

```text
Maze_Bank_Site/
├── backend/    # API REST construída com FastAPI e Python
└── frontend/   # Interface do usuário construída com Vue 3 e Vite
```
<img width="450" height="450" src="https://github.com/user-attachments/assets/18a1b20f-87cc-49ff-a956-9c1b44aae6df" />

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

<img width="450" height="450" src="https://github.com/user-attachments/assets/ee5dafd6-b2c3-40b9-ab2f-9792de543930" />

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

<img width="450" height="450" src="https://github.com/user-attachments/assets/dff034e3-cabc-408c-b388-222f28a3d729" />
<img width="450" height="450" src="https://github.com/user-attachments/assets/d9c73867-1ac7-4115-8329-447a2bb17f4b" />

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
