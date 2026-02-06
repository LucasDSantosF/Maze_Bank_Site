<script setup>
import { ref, onMounted } from 'vue';

const toastEl = ref(null);

onMounted(() => {
  const bootstrap = window.bootstrap;
  
  if (bootstrap && toastEl.value) {
    const toast = new bootstrap.Toast(toastEl.value, {
      autohide: true,
      delay: 3000
    });
    toast.show();
  } else {
    console.error("Bootstrap não encontrado ou elemento não carregado");
  }
});
</script>

<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1080;">
    <div 
      ref="toastEl" 
      class="toast show" 
      role="alert" 
      aria-live="assertive" 
      aria-atomic="true"
    >
      <div class="toast-body d-flex align-items-center bg-white border-start border-danger border-4 rounded shadow">
        <i class="bi bi-exclamation-triangle-fill text-danger me-3 fs-5"></i>
        <span class="text-dark m-0">
          Por favor, preencha todos os campos obrigatórios.
        </span>
      </div>
    </div>
  </div>
</template>