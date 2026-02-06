<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasSaque">
    <div v-if="step === 1" class="offcanvas-header border-bottom py-3">
      <h5 class="offcanvas-title fw-bold text-dark">
        <i class="bi bi-cash-stack text-danger me-2"></i>Sacar Dinheiro
      </h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" @click="resetarSaque"></button>
    </div>

    <div class="offcanvas-body bg-light d-flex flex-column">
      
      <div v-if="step === 1" class="flex-grow-1 d-flex flex-column justify-content-center">
        <div class="text-center mb-5">
          <label class="form-label small fw-bold text-muted text-uppercase mb-3">Quanto deseja sacar?</label>
          <div class="d-flex flex-column align-items-center justify-content-center w-100">
            <div class="input-money-container bg-white shadow-sm d-flex align-items-center justify-content-center p-4 rounded-5">
                <span class="fs-2 fw-bold text-danger">R$</span>
                
                <input 
                type="text" 
                class="money-input fw-bold text-dark border-0 bg-transparent" 
                :value="valorExibido"
                @input="handleValorInput"
                :style="{ width: inputWidth }"
                inputmode="numeric"
                placeholder="0,00"
                >
            </div>
          </div>
          <p class="text-muted small mt-3">Saldo disponível: <span class="fw-bold">R$ 5.000,00</span></p>
        </div>

        <button @click="processarSaque" 
                class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mt-auto mb-3" 
                :disabled="!valorSaque || valorSaque <= 0">
          Confirmar Saque
        </button>
      </div>

      <div v-if="step === 'sucesso'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-icon bg-success text-white rounded-circle mb-4 animate__animated animate__bounceIn">
          <i class="bi bi-check-lg display-1"></i>
        </div>
        <h3 class="fw-bold text-dark">Saque Autorizado!</h3>
        <p class="text-muted">Retire seu dinheiro na boca do caixa. O valor de <span class="fw-bold text-dark">{{ formatarMoedaFinal(valorSaque) }}</span> foi debitado da sua conta.</p>
        
        <button @click="resetarSaque" class="btn btn-outline-dark w-100 py-3 rounded-4 fw-bold mt-5">
          Voltar ao Início
        </button>
      </div>

      <div v-if="step === 'erro'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-icon bg-danger text-white rounded-circle mb-4 animate__animated animate__shakeX">
          <i class="bi bi-x-lg display-1"></i>
        </div>
        <h3 class="fw-bold text-dark">Saque Recusado</h3>
        <p class="text-muted">Infelizmente você não possui saldo suficiente para realizar esta operação ou excedeu seu limite diário.</p>
        
        <div class="w-100 mt-5 d-flex flex-column gap-2">
          <button @click="step = 1" class="btn btn-danger w-100 py-3 rounded-4 fw-bold">
            Tentar outro valor
          </button>
          <button @click="resetarSaque" class="btn btn-light w-100 py-3 rounded-4 fw-bold">
            Cancelar
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap';

let offcanvasBS = null;
const step = ref(1);
const valorSaque = ref(0);
const saldoSimulado = 500000;

const valorExibido = computed(() => {
  if (!valorSaque.value) return '0,00';
  
  return (valorSaque.value / 100).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
});

const handleValorInput = (event) => {
  let somenteNumeros = event.target.value.replace(/\D/g, "");

  valorSaque.value = somenteNumeros ? parseInt(somenteNumeros) : 0;
  event.target.value = valorExibido.value;
};

const formatarMoedaFinal = (centavos) => {
  return (centavos / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

const inputWidth = computed(() => {
  const tamanho = valorExibido.value.length;
  return `${tamanho * 22 + 20}px`; 
});

// LÓGICA DE PROCESSO
const processarSaque = () => {
  setTimeout(() => {
    if (valorSaque.value > saldoSimulado) {
      step.value = 'erro';
    } else {
      step.value = 'sucesso';
    }
  }, 800);
};

const resetarSaque = () => {
  offcanvasBS?.hide();
  setTimeout(() => {
    step.value = 1;
    valorSaque.value = 0;
  }, 400);
};

onMounted(() => {
  const el = document.getElementById('offcanvasSaque');
  if (el) offcanvasBS = new Offcanvas(el);
});

const abrirSaque = () => offcanvasBS?.show();

defineExpose({ abrirSaque });
</script>

<style scoped>
#offcanvasSaque {
  height: calc(100vh - 72px) !important;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}

.input-money-box {
  min-width: 220px;
  max-width: 300px;
  transition: all 0.2s ease;
}

.money-display {
  font-size: 2.5rem;
  width: 100%;
  outline: none;
}

.status-icon {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input-money-container {
  display: inline-flex; 
  max-width: 95%;
  transition: all 0.2s ease;
  overflow: visible;
}

.money-input {
  font-size: 2.5rem;
  outline: none;
  text-align: left;
  padding-left: 10px;
  overflow: hidden; 
  white-space: nowrap;
}
</style>