# 🚀 Projeto Vue 3 + Vite + Bootstrap

Este é um projeto base em **Vue 3** utilizando **Vite** como bundler, **Bootstrap 5** para estilos e **Vue Router** para navegação entre páginas.  
A aplicação contém duas telas iniciais: **Login** e **Home**.

---

## 💻 Instalação e comandos principais

### 1️⃣ Criar o projeto com Vite + Vue 3

```bash
npm create vite@latest my-app -- --template vue
```

2️⃣ Acessar o projeto e instalar dependências

```bash
cd my-app
npm install
```

3️⃣ Instalar o Bootstrap 5

```bash
npm install bootstrap
```
Importe o CSS e JS do Bootstrap no main.js:
```bash
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
```

4️⃣ Instalar Vue Router

```bash
npm install vue-router
```

No arquivo src/main.js:
```js
createApp(App).use(router).mount('#app') // <-- registra o router na aplicação
```
O App.vue deve conter:
```js
<template>
  <div id="app">
    <router-view /> <!-- Aqui o Vue Router renderiza a página atual -->
  </div>
</template>
```
O ```<router-view />``` funciona como um “slot” que exibe a página correspondente à rota atual.

Exemplo: 
  /home → renderiza Home.vue


5️⃣ Instalação do vue-mask

Doc: https://vuejs-tips.github.io/vue-the-mask/

```bash
npm i -S vue-the-mask 
```

No arquivo **Main.js** adicionar o import do vue-mask:

```js
import { mask } from 'vue-the-mask'
```

Adicionar a diretiva no Vue do **Main.js**:

```js
Vue.directive('mask',mask)
```

Exemplo de uso:

```js
v-mask="['(##) ####-####','(##) #####-####']"
```

----------

## Comandos principais do Vue 3 + Vite

| Comando | 	Descrição | 
|----------|----------|
| npm install	| Instala todas as dependências do projeto | 
| npm run dev	| Inicia o servidor local de desenvolvimento (geralmente em http://localhost:5173) | 
| npm run build	| Gera a build otimizada para produção na pasta /dist | 
| npm run preview	| Serve a build de produção localmente (para testar) | 