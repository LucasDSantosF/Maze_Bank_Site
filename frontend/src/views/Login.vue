<template>
  <div class="container-fluid vh-100 d-flex p-0">
    <div class="row g-0 w-100">
      
      <div class="col-lg-5 d-none d-lg-flex flex-column align-items-center justify-content-center p-5 border-end">
        <div class="text-center">
            <img src="/Maze-Bank-logo.png" alt="Maze Bank Logo" class="img-fluid p-2">
          <h1 class="display-3 fw-bold m-0 text-danger">MAZE BANK</h1>
          <p class="fs-5 text-muted">O banco do futuro, hoje.</p>
        </div>
      </div>

      <div class="col-lg-7 d-flex align-items-center justify-content-center maze-gradient text-white">
        <div class="login-form-container p-4 p-md-5">
          <div class="text-center mb-5">
            <h2 class="fw-bold h1 text-white">Bem-vindo</h2>
            <p class="opacity-75">Entre na sua conta para continuar</p>
          </div>

          <ToastAlert v-if="mostrarToast"/>

          <SignIn 
            v-if="isLogin"
            @update:dados="dadosSignIn = $event"
          />

          <SignUp 
            v-if="!isLogin"
            @update:dados="dadosSignUp = $event"
            @update:valido="signUpValida = $event"
          />

          <ErrorAlert 
              v-if="mostrarErro"
              :mensagem="erroMsg"
              @close="mostrarErro = false"
          />

          <SuccessAlert
              v-if="sucessoRegistro"
              @close="sucessoRegistro = false"
          />
          
          <div v-if="isLogin" class="d-flex justify-content-between align-items-center mb-3">
            <p class="align-item-center ">
              <small class="opacity-75">Não tem uma conta? </small>
              <a 
                href="#" 
                @click.prevent="isLogin = false, labelButton = 'Registrar'" 
                class="text-white fw-semibold">Criar conta
              </a>
            </p>
          </div>
            <button 
              class="btn btn-light w-100 py-3 fs-5 fw-bold text-danger shadow"
              form="handleData"
              :disabled="isLoadingBotao"
              @click="onClick">
                <span 
                    v-if="isLoadingBotao" 
                    class="spinner-border spinner-border-sm" 
                    role="status" 
                    aria-hidden="true"
                />
                <span v-else>{{labelButton}}</span> 
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import { auth } from '../api/models/apis'
import SignIn from '../components/SignIn.vue';
import SignUp from '../components/SignUp.vue';
import ToastAlert from '../components/Alert/ToastAlert.vue';
import ErrorAlert from '../components/Alert/ErrorAlert.vue';
import SuccessAlert from '../components/Alert/SuccessAlert.vue';

const isLogin = ref(true);
const labelButton = ref('Entrar');
const dadosSignIn = ref({});
const dadosSignUp = ref({});
const signUpValida = ref(false);
const mostrarToast = ref(false);
const isLoadingBotao = ref(false);
const mostrarErro = ref(false);
const erroMsg = ref(undefined);
const sucessoRegistro = ref(false);

const router = useRouter();

async function carregarSessao() {
    const isAuthenticated = await auth.checkAuth();
    
    if (isAuthenticated) {
        router.push({ name: 'Home' });
    }
};

onMounted(carregarSessao);

function showAlertAndHide() {
    mostrarToast.value = false;
    
    setTimeout(() => {
        mostrarToast.value = true;
        
        setTimeout(() => {
            mostrarToast.value = false;
        }, 3500);
    }, 10); 
}

const onClick = () => {
    if (isLogin.value) {
      signIn();
    } else if (!isLogin.value && signUpValida.value) {
      signUp();
    } else {
      showAlertAndHide();
    };
};

async function signIn() {
    try {
        isLoadingBotao.value = true;
        const credentials = {
            cpf: dadosSignIn.value.cpf,
            senha: dadosSignIn.value.password,
        };

        const response = await auth.login(credentials);

        router.push({ name: 'Home' });
    } catch (error) {
        erroMsg.value = error.response?.data.detail || undefined;
        mostrarErro.value = true;
    } finally {
      isLoadingBotao.value = false;
    } 
}

async function signUp() {
    try {
      isLoadingBotao.value = true;
        const payload = {
            cpf: dadosSignUp.value.cpf,
            nome: dadosSignUp.value.nome,
            sobrenome: dadosSignUp.value.sobrenome,
            email: dadosSignUp.value.email,
            senha: dadosSignUp.value.password,
        };

        const response = await auth.registrar(payload);

        sucessoRegistro.value = true;
        isLogin.value = true;
    } catch (error) {
        erroMsg.value = error.response?.data.detail || undefined;
        signUpValida.value = false;
        mostrarErro.value = true;
    } finally {
      isLoadingBotao.value = false;
    } 
}
</script>