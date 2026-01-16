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

          <SignIn 
            v-if="isLoading"
            @update:dados="dadosSignIn = $event"
          />

          <SignUp 
            v-if="!isLoading"
            @update:dados="dadosSignUp = $event"
            @update:valido="signUpValida = $event"
          />
          
          <div v-if="isLoading" class="d-flex justify-content-between align-items-center mb-3">
            <p class="align-item-center ">
              <small class="opacity-75">Não tem uma conta? </small>
              <a 
                href="#" 
                @click.prevent="isLoading = false, labelButton = 'Registrar'" 
                class="text-white fw-semibold">Criar conta
              </a>
            </p>
          </div>
          <button 
            class="btn btn-light w-100 py-3 fs-5 fw-bold text-danger shadow"
            form="handleData"
            @click="handleLogin">
            {{labelButton}}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import SignIn from '../components/SignIn.vue';
import SignUp from '../components/SignUp.vue';

const isLoading = ref(true);
const labelButton = ref('Entrar');
const dadosSignIn = ref({});
const dadosSignUp = ref({});
const signUpValida = ref(false);

const router = useRouter();

const handleLogin = () => {
  console.log('login: ', dadosSignIn.value);
  console.log('registrar: ', dadosSignUp.value);
  router.push({name: 'Home'});
};
</script>