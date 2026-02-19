# 🚀 Projeto Vue 3 + Vite + Bootstrap 5

Este é um projeto base em **Vue 3** utilizando **Vite** como bundler, **Bootstrap 5** para estilos e **Vue Router** para navegação entre páginas.  
A aplicação contém duas telas iniciais: **Login** e **Home**.

## 📂 Estrutura de Pastas
```text
├── api/            # Configurações de serviços e chamadas HTTP (Axios)
│   ├── models/     # Definições de estruturas de dados
│   └── axios.js    # Instância personalizada do Axios
├── assets/         # Arquivos estáticos (imagens, fontes, ícones)
├── components/     # Componentes reutilizáveis (botões, inputs, cards)
│   ├── Alert/      # Componentes de alertas do sistema
│   └── views/      # Sub-componentes específicos de telas
├── router/         # Configuração de rotas (Vue Router)
├── utils/          # Funções utilitárias e ajudantes (ex: validarSenha.js)
├── views/          # Páginas/Telas principais da aplicação (Home, Login)
├── App.vue         # Componente raiz
├── main.js         # Ponto de entrada (importação de libs e CSS)
└── style.css       # Estilos globais
```

## 💻 Instalação e comandos principais

### 1️⃣ Criar o projeto com Vite + Vue 3

```bash
npm create vite@latest my-app -- --template vue
```

### 2️⃣ Acessar o projeto e instalar dependências

```bash
cd my-app
npm install
```

### 3️⃣ Instalar o Bootstrap 5 e Bootstrap Icons

  ```bash
  npm install bootstrap bootstrap-icons
  ```

  - #### Importe o CSS e JS do Bootstrap no main.js:
    
    ```js
    import 'bootstrap/dist/css/bootstrap.min.css'
    import 'bootstrap-icons/font/bootstrap-icons.css'
    ```

### 4️⃣ Instalar Vue Router

```bash
npm install vue-router
```

- #### No arquivo src/main.js:
  ```js
  createApp(App).use(router).mount('#app') // <-- registra o router na aplicação
  ```
- #### O App.vue deve conter:
  ```html
  <template>
    <div id="app">
      <router-view /> <!-- Aqui o Vue Router renderiza a página atual -->
    </div>
  </template>
  ```
  O ```<router-view />``` funciona como um “slot” que exibe a página correspondente à rota atual.

  #### Exemplo: 
    ```/home → renderiza Home.vue```

### 5️⃣ Instalação do vue-mask

#### Doc: *https://vuejs-tips.github.io/vue-the-mask/*

```bash
npm i -S vue-the-mask 
```

- #### No arquivo **Main.js** adicionar o import do vue-mask:

  ```js
  import { mask } from 'vue-the-mask'
  ```
- #### Adicionar a diretiva no Vue do **Main.js**:

  ```js
  Vue.directive('mask',mask)
  ```

  #### Exemplo de uso:

  ```js
  v-mask="['(##) ####-####','(##) #####-####']"
  ```

### 6️⃣  Instalando Axios
  ```bash
  npm install axios
  ```

----------

## Comandos principais do Vue 3 + Vite

| Comando | 	Descrição | 
|----------|----------|
| npm install	| Instala todas as dependências do projeto | 
| npm run dev	| Inicia o servidor local de desenvolvimento (geralmente em http://localhost:5173) | 
| npm run build	| Gera a build otimizada para produção na pasta /dist | 
| npm run preview	| Serve a build de produção localmente (para testar) | 
----------

## 📈 Próximos Passos (Roadmap)

* [ ] **Gerenciamento de Estado (Pinia): Implementar o Pinia para armazenar os dados do usuário logado.**

* [ ] **Skeleton Screens: Adicionar carregamentos suaves (esqueletos de tela) em vez de apenas o Spinner de loading.**

* [ ] **Internacionalização (i18n): Preparar a aplicação para suporte a múltiplos idiomas (Português/Inglês).**

* [ ] **Dark Mode: Implementar alternância de temas (Claro/Escuro) utilizando variáveis CSS.**

* [ ] **Testes Unitários: Iniciar a cobertura de testes nos componentes críticos (como o formulário de Login) utilizando Vitest.**

* [ ] **CI/CD: Configurar um fluxo automatizado (GitHub Actions) para rodar os testes e fazer o deploy no Vercel ou Netlify a cada novo push.**