<template>
  <div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.8); backdrop-filter: blur(4px); z-index: 9999;">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0">
        <div class="modal-body text-center p-5">
          <div class="text-danger mb-4">
            <i class="bi bi-shield-slash" style="font-size: 4rem;"></i>
          </div>
          <h4 class="fw-bold text-dark">Conexão Perdida</h4>
          <p class="text-muted">{{ erroMsg }}</p>
          
          <div class="d-grid gap-2 mt-4">
            <button @click="$emit('recarregar')" class="btn btn-danger py-2 fw-bold">
              Tentar Novamente
            </button>
            <button @click="handleLogout" class="btn btn-link text-muted">
              Sair da conta
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { auth } from '../../api/models/apis';

defineProps({
  erroMsg: {
    type: String,
    default: 'Erro inesperado.'
  },
})

// Definimos que este componente emite um evento chamado 'retry'
defineEmits(['recarregar'])

const router = useRouter();

const handleLogout = async () => {
  try {
    await auth.logout();
    router.push({ name: 'Login' });
  } catch (error) {
    router.push({ name: 'Login' });
  }
};
</script>