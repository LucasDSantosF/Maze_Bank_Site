# 🏦 Maze Bank API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

O **Maze Bank API** é um sistema de core banking robusto que simula operações bancárias reais. O projeto foca em integridade de dados financeiros, segurança via tokens JWT e uma arquitetura escalável.

---

## 🚀 Diferenciais do Projeto

* **Precisão Decimal**: Utiliza `Numeric/Decimal` para garantir cálculos monetários exatos.

* **Two-Step Transfer**: Fluxo de transferência em duas etapas (Sinalização -> Confirmação) para maior segurança do usuário.

* **Segurança Avançada**: Autenticação baseada em JWT (JSON Web Token) com expiração configurável.

* **Privacidade (LGPD)**: Lógica de máscara de CPF automática em extratos bancários.

* **Arquitetura Modular**: Código organizado por domínios (Auth, Pix, Extrato, Transactions).

---

## 🛠️ Tecnologias e Bibliotecas

- **FastAPI**: Desenvolvimento de endpoints assíncronos e documentação automática.

- **SQLAlchemy**: ORM para mapeamento e manipulação do banco de dados.

- **Python-Jose**: Geração e validação de tokens JWT.

- **Passlib (Bcrypt)**: Hashing seguro de senhas.

- **Python-Dotenv**: Gestão de variáveis de ambiente.

---

## 📂 Estrutura de Pastas

```text
backend/
└── app/
    ├── api/          # Roteadores modulares (Auth, Pix, Extrato, etc.)
    ├── db/           # Configuração de conexão e sessão do banco
    ├── models/       # Modelos SQLAlchemy e definições de tabelas
    ├── .env          # Variáveis de ambiente (Chaves e Configurações)
    ├── config.py     # Centralização da lógica de leitura do .env
    └── main.py       # Ponto de entrada da aplicação
```

## 🛠️ Instalação e Requisitos

Certifique-se de ter o **Python 3.10 ou superior** instalado.

### 1️⃣ Clone o repositório:**
```bash
   git clone [https://github.com/seu-usuario/Maze_Bank_Site.git](https://github.com/seu-usuario/Maze_Bank_Site.git)
```
```bash
   cd Maze_Bank_Site
```

### 2️⃣ Criar / ativar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
venv/Scripts/activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Instale as dependências:**

```Bash
pip install nome_do_pacote
```

### 4️⃣ Criar o requirements.txt
**Para gerar um arquivo com todos os pacotes instalados atualmente no ambiente:**
```Bash
pip freeze > requirements.txt
```
### 5️⃣ Instalar pacotes de um requirements.txt
**Se você clonar este projeto em outro computador ou servidor, instale todas as dependências com:**

```Bash
pip install -r requirements.txt
```
---

## ⚙️ Configuração de Ambiente

**Para a segurança da aplicação, as chaves não são enviadas para o repositório. Siga os passos abaixo:**

* Localize o arquivo `backend/app/.env.example`.

* Renomeie-o para `.env` (na mesma pasta `backend/app/`).

* Gere uma chave secreta segura rodando o comando abaixo no terminal:

    ```Bash
        python -c "import secrets; print(secrets.token_hex(32))"
    ```
    **Cole o resultado no campo SECRET_KEY dentro do seu novo arquivo `.env`.**

## 🏁 Como Executar
**Com o ambiente virtual ativado e as dependências instaladas, execute:**

```Bash
cd backend # Entre na pasta do backend (se já não estiver nela)
```

## Inicie o servidor
```Bash
cd app
uvicorn main:app --reload
```
-   **Acesse a documentação interativa em:**

    **Swagger UI:** http://127.0.0.1:8000/docs

    **Redoc:** http://127.0.0.1:8000/redoc

## 📈 Próximos Passos (Roadmap)
* [ ] **Testes Automatizados: Implementação com Pytest.**

* [ ] **Docker: Containerização do backend e banco de dados.**

* [ ] **Redis: Cache para sinalizações de transferência temporárias.**

* [ ] **Frontend: Integração completa com a interface Next.js/React.**