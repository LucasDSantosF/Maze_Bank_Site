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
            <h2 class="fw-bold h1 text-white">
              {{ isLogin ? 'Bem-vindo' : 'Crie sua conta' }}
            </h2>
            <p class="opacity-75">
              {{ isLogin ? 'Entre na sua conta para continuar' : 'Preencha os dados para se tornar um cliente' }}
            </p>
          </div>

          <ToastAlert v-if="mostrarToast"/>

          <ErrorAlert 
              v-if="mostrarErro"
              :mensagem="erroMsg"
              @close="mostrarErro = false"
          />

          <SuccessAlert
              v-if="sucessoRegistro"
              @close="sucessoRegistro = false"
          />

          <SignIn 
            v-if="isLogin"
            @update:dados="dadosSignIn = $event"
          />

          <SignUp 
            v-if="!isLogin"
            @update:dados="dadosSignUp = $event"
            @update:valido="signUpValida = $event"
          />
          
          <div class="mb-4 mt-2">
            <p v-if="isLogin" class="m-0">
              <small class="opacity-75">Não tem uma conta? </small>
              <a 
                href="#" 
                @click.prevent="toggleMode(false, 'Registrar')" 
                class="text-white fw-semibold">Criar conta
              </a>
            </p>
            <p v-else class="m-0">
              <small class="opacity-75">Já possui cadastro? </small>
              <a 
                href="#" 
                @click.prevent="toggleMode(true, 'Entrar')" 
                class="text-white fw-semibold">Voltar para o Login
              </a>
            </p>
          </div>

          <button 
              class="btn btn-light w-100 py-3 fs-5 fw-bold text-danger shadow-lg transition-transform"
              :disabled="isLoadingBotao"
              @click="onClick">
                <span 
                    v-if="isLoadingBotao" 
                    class="spinner-border spinner-border-sm me-2" 
                    role="status" 
                />
                <span>{{ labelButton }}</span> 
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

const router = useRouter();

const isLogin = ref(true);
const labelButton = ref('Entrar');
const isLoadingBotao = ref(false);
const mostrarToast = ref(false);
const mostrarErro = ref(false);
const sucessoRegistro = ref(false);
const erroMsg = ref(undefined);

const dadosSignIn = ref({});
const dadosSignUp = ref({});
const signUpValida = ref(false);

onMounted(async () => {
    const isAuthenticated = await auth.checkAuth();
    if (isAuthenticated) router.push({ name: 'Home' });
});

function toggleMode(loginMode, label) {
    isLogin.value = loginMode;
    labelButton.value = label;
    mostrarErro.value = false;
}

function showAlertAndHide() {
    mostrarToast.value = false;
    setTimeout(() => {
        mostrarToast.value = true;
        setTimeout(() => { mostrarToast.value = false; }, 3500);
    }, 10); 
}

const onClick = () => {
    if (isLogin.value) {
      signIn();
    } else if (!isLogin.value && signUpValida.value) {
      signUp();
    } else {
      showAlertAndHide();
    }
};

async function signIn() {
    try {
        isLoadingBotao.value = true;
        mostrarErro.value = false;
        
        const credentials = {
            cpf: dadosSignIn.value.cpf,
            senha: dadosSignIn.value.password,
        };

        await auth.login(credentials);
        router.push({ name: 'Home' });
    } catch (error) {
        erroMsg.value = error.response?.data?.message || undefined;
        mostrarErro.value = true;
    } finally {
        isLoadingBotao.value = false;
    } 
}

async function signUp() {
    try {
        isLoadingBotao.value = true;
        mostrarErro.value = false;

        const payload = {
            cpf: dadosSignUp.value.cpf,
            nome: dadosSignUp.value.nome,
            sobrenome: dadosSignUp.value.sobrenome,
            email: dadosSignUp.value.email,
            senha: dadosSignUp.value.password,
        };

        await auth.registrar(payload);

        sucessoRegistro.value = true;
        toggleMode(true, 'Entrar'); 
    } catch (error) {
        erroMsg.value = error.response?.data?.message || undefined;
        signUpValida.value = false;
        mostrarErro.value = true;
    } finally {
        isLoadingBotao.value = false;
    } 
}
</script>

<style scoped>
.login-form-container {
  width: 100%;
  max-width: 450px;
}

.transition-transform:active {
  transform: scale(0.98);
}
</style>