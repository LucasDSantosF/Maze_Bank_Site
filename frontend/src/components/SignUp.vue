<template>
<form @submit.prevent="handleLogin">
    <div class="mb-4">
        <label class="form-label fw-semibold text-white">Nome</label>
        <div class="input-group shadow-sm">
            <input 
                type="text"
                class="form-control maze-input-inverted ps-2"
                placeholder="Digite seu nome"
                @input="validar"
                v-model="nome">
        </div>
    </div>

    <div class="mb-4">
        <label class="form-label fw-semibold text-white">Sobrenome</label>
        <div class="input-group shadow-sm">
            <input 
                type="text"
                class="form-control maze-input-inverted ps-2"
                placeholder="Digite seu nome"
                @input="validar"
                v-model="sobrenome">
        </div>
    </div>

    <div class="mb-4">
        <label class="form-label fw-semibold text-white">E-mail</label>
        <div class="input-group shadow-sm">
            <input 
                type="text"
                class="form-control maze-input-inverted ps-2"
                placeholder="seu@email.com"
                @input="validar"
                v-model="email">
        </div>
    </div>

    <div class="mb-4">
        <label class="form-label fw-semibold text-white">CPF</label>
        <div class="input-group shadow-sm">
            <input 
                type="text"
                class="form-control maze-input-inverted ps-2"
                v-mask="'###.###.###-##'"
                placeholder="000.000.000-00"
                @input="validar"
                v-model="cpf">
        </div>
    </div>

    <div class="mb-1">
        <label class="form-label fw-semibold text-white">Senha</label>
        <div class="input-group">
            <span class="input-group-text bg-white border-0">
                <i class="bi bi-lock text-danger"></i>
            </span>
            <input 
                :type="showPassword ? 'text' : 'password'"
                class="form-control maze-input-inverted"
                @input="validar"
                placeholder="••••••••"
                v-model="password">
            <span 
                class="input-group-text bg-white border-0"
                @click="showPassword = !showPassword"
                style="cursor: pointer;">
                <i :class="showPassword ? 'bi bi-eye-slash text-danger' : 'bi bi-eye text-danger'"></i>
            </span>
        </div>
        <div class="mt-1 mb-0">
            <small class="opacity-75"><strong>A senha deve conter no mínimo 8 caracteres,</strong></small>
        </div>
        <div class="mb-0">
            <small class="opacity-75"><strong>incluindo letras maiúsculas, minúsculas,</strong></small>
        </div>
        <div :class="isPassword ? 'mb-4' : 'mb-2'">
            <small class="opacity-75"><strong>números e caracteres especiais.</strong></small>
        </div>
        <div class="mb-4" v-show="!isPassword">
            <p class="opacity-75 mb-0"><strong>Senha incorreta:</strong></p>
            <small class="opacity-80 mt-0"><strong>{{ msgSenha }}</strong></small>
        </div>


    </div>

    <div class="mb-4">
        <label class="form-label fw-semibold text-white">Confirmar senha</label>
        <div class="input-group">
            <span class="input-group-text bg-white border-0">
                <i class="bi bi-lock text-danger"></i>
            </span>
            <input 
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-control maze-input-inverted"
                @input="validar"
                placeholder="••••••••"
                v-model="comfirmPassword">
            <span 
                class="input-group-text bg-white border-0"
                @click="showConfirmPassword = !showConfirmPassword"
                style="cursor: pointer;">
                <i :class="showConfirmPassword ? 'bi bi-eye-slash text-danger' : 'bi bi-eye text-danger'"></i>
            </span>
        </div>
        <div class="mb-1" v-show="!isPasswordConfirm">
            <small class="opacity-80"><strong>As senhas digitadas são diferentes.</strong></small>
        </div>
        <div class="mb-4" v-show="!isPasswordConfirm">
            <small class="opacity-80"><strong>Certifique-se de que sejam iguais.</strong></small>
        </div>
        
    </div>
</form>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';
import { validarSenha } from '../utils/validarSenha';

const emit = defineEmits(['update:dados', 'update:valido']);

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const nome = ref('');
const sobrenome = ref('');
const cpf = ref('');
const email = ref('');
const password = ref('');
const comfirmPassword = ref('');
const isPassword = ref(false);
const isPasswordConfirm  = ref(true);
const msgSenha = ref('');

function limparApenasDigitos(valor) {
    if (!valor) return '';
    return valor.toString().replace(/\D/g, '');
}

function validar() {
  const senhaValidada = validarSenha(password.value);
  msgSenha.value = senhaValidada.mensagem;
  isPassword.value = senhaValidada.valido;
  isPasswordConfirm.value = password.value == comfirmPassword.value;
  const cpfLimpo = limparApenasDigitos(cpf.value)
  const isValido = isPassword.value && isPasswordConfirm.value 
    && nome.value.length != 0 && sobrenome.value.length != 0 
    && email.value.includes('@') && cpfLimpo.length === 11

console.log(isValido)
console.log(password.value)

  emit(
    'update:dados', {
        nome: nome.value,
        sobrenome: sobrenome.value,
        cpf: limparApenasDigitos(cpf.value),
        email: email.value,
        password: password.value,
    }
  );
  emit('update:valido', isValido);
}

watch([nome, cpf, email, password], validar, { immediate: true });
</script>