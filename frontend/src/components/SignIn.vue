<template>
<form @submit.prevent="handleLogin">
    <div class="mb-4">
        <label class="form-label fw-semibold text-white">E-mail</label>
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-0 pe-0">
                <i class="bi bi-person text-danger"></i>
            </span>
            <input 
                type="text"
                class="form-control maze-input-inverted ps-2"
                v-mask="'###.###.###-##'"
                placeholder="000.000.000-00"
                @input="validar"
                v-model="login">
        </div>
    </div>

    <div class="mb-3">
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
    </div>
</form>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';

const emit = defineEmits(['update:dados']);

const showPassword = ref(false);
const login = ref('');
const password = ref('');

function limparApenasDigitos(valor) {
    if (!valor) return '';
    return valor.toString().replace(/\D/g, '');
}

function validar() {
  emit(
    'update:dados', {
        cpf: limparApenasDigitos(login.value),
        password: password.value,
    }
  );
}

watch([login, password], validar, { immediate: true });
</script>