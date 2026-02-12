<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasDeposito">
    <div v-if="step === 1" class="offcanvas-header border-bottom py-3">
      <h5 class="offcanvas-title fw-bold text-dark">
        <i class="bi bi-piggy-bank text-danger me-2"></i>Depositar
      </h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" @click="resetarDeposito"></button>
    </div>

    <div class="offcanvas-body bg-light d-flex flex-column">
      
      <div v-if="step === 1" class="flex-grow-1 d-flex flex-column justify-content-center">
        <div class="text-center mb-5">
          <label class="form-label small fw-bold text-muted text-uppercase mb-3">Valor do depósito</label>
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
          <p class="text-muted small mt-3 px-4">O valor será creditado na sua conta após a conferência dos envelopes/notas.</p>
        </div>

        <button 
          @click="processarDeposito" 
          class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mt-auto mb-3" 
          :disabled="(!valorDeposito || valorDeposito <= 0)&& isLoadingBotao">
          <span 
              v-if="isLoadingBotao" 
              class="spinner-border spinner-border-sm me-2" 
              role="status"
          />
          <span>Confirmar Depósito</span>
        </button>
      </div>

      <div v-if="step === 'sucesso'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-icon bg-success text-white rounded-circle mb-4 animate__animated animate__bounceIn">
          <i class="bi bi-arrow-down-circle-fill display-1"></i>
        </div>
        <h3 class="fw-bold text-dark">Recebemos seu depósito!</h3>
        <p class="text-muted">O valor de <span class="fw-bold text-dark">{{ formatarMoedaFinal(valorDeposito) }}</span> está em processamento e logo estará disponível em seu saldo.</p>
        
        <button @click="resetarDeposito" class="btn btn-outline-dark w-100 py-3 rounded-4 fw-bold mt-5">
          Concluir
        </button>
      </div>

      <div v-if="step === 'erro'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-icon bg-warning text-dark rounded-circle mb-4 animate__animated animate__shakeX">
          <i class="bi bi-exclamation-triangle-fill display-1"></i>
        </div>
        <h3 class="fw-bold text-dark">Ops! Algo deu errado</h3>
        <p class="text-muted">
          Não conseguimos processar sua solicitação no momento. {{ erroMsg }}. Por favor, tente novamente em alguns instantes.
        </p>
        
        <div class="w-100 mt-5 d-flex flex-column gap-2">
          <button @click="step = 1" class="btn btn-danger w-100 py-3 rounded-4 fw-bold">
            Tentar Novamente
          </button>
          <button @click="resetarDeposito" class="btn btn-light w-100 py-3 rounded-4 fw-bold">
            Cancelar
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap';
import { transactions } from '../../api/models/apis';

const router = useRouter();

let offcanvasBS = null;
const step = ref(1);
const valorDeposito = ref(0);
const isLoadingBotao = ref(false);
const erroMsg = ref('');

const valorExibido = computed(() => {
  if (!valorDeposito.value) return '0,00';
  
  return (valorDeposito.value / 100).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
});

const handleValorInput = (event) => {
  let somenteNumeros = event.target.value.replace(/\D/g, "");

  valorDeposito.value = somenteNumeros ? parseInt(somenteNumeros) : 0;
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
const processarDeposito = async () => {
  isLoadingBotao.value = true;
  try {
    const payload = {
      valor: valorDeposito.value,
    }

    const response = await transactions.deposito(payload);
    step.value = 'sucesso';
  } catch (error) {
    erroMsg.value = error.response?.data?.message || 'Algo deu errado.';

    step.value = 'erro';
  } finally {
    isLoadingBotao.value = false;
  }
};

const resetarDeposito = () => {
  offcanvasBS?.hide();
  router.push({name: 'Login'})
};

onMounted(() => {
  const el = document.getElementById('offcanvasDeposito');
  if (el) offcanvasBS = new Offcanvas(el);
});

const abrirDeposito = () => offcanvasBS?.show();

defineExpose({ abrirDeposito });
</script>

<style scoped>
#offcanvasDeposito {
  height: calc(100vh - 72px) !important;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}

.input-money-box {
  min-width: 220px;
  max-width: 320px;
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