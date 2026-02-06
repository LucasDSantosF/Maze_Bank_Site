<template>
  <div class="alert alert-danger d-flex align-items-start responsive-alert" role="alert">
    
    <i class="bi bi-exclamation-triangle-fill flex-shrink-0 me-3 fs-5 fs-sm-6 alert-icon"></i>
    
    <div>
      <h4 class="alert-heading fs-5 fs-sm-6 mb-1">{{ titulo }}</h4>
      <span class="fs-6 fs-sm-7">Não foi possível completar a operação. {{ mensagem }}. {{subtexto}}.</span> 
    </div>
    
    <button type="button" class="btn-close ms-auto mt-1" aria-label="Close" @click="fecharAlerta"></button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const emit = defineEmits(['close']); 

defineProps({
  titulo: {
    type: String,
    default: 'Solicitação não processada'
  },
  mensagem: {
    type: String,
    default: 'Erro inesperado'
  },
  subtexto: {
    type: String,
    default: 'Por favor, tente novamente em instantes'
  }
});

function fecharAlerta() {
    emit('close');
}
</script>

<style scoped>
.alert-icon {
    margin-right: 1rem;
    align-self: flex-start;
}

@media (max-width: 600px) {
    .alert-icon {
        align-self: flex-start !important; 
        
        margin-top: -0.1rem !important; 
        
        margin-right: 0.5rem !important; 
    }
    
    .responsive-alert {
        align-items: flex-start !important;
        padding: 0.5rem !important;
    }
    
    .responsive-alert .btn-close {
        align-self: flex-start !important;
        margin-top: 0.1rem !important;
    }
}
</style>