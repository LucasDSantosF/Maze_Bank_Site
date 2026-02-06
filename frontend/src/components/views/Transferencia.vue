<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasTransferencia">
    <div v-if="step !== 'sucesso' && step !== 'erro'" class="offcanvas-header border-bottom py-3">
      <div class="d-flex align-items-center">
        <button v-if="step > 1" @click="voltarStep" class="btn btn-sm btn-light rounded-circle me-3">
          <i class="bi bi-arrow-left"></i>
        </button>
        <h5 class="offcanvas-title fw-bold text-dark">{{ tituloStep }}</h5>
      </div>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" @click="resetarFluxoCompleto"></button>
    </div>

    <div class="offcanvas-body bg-light d-flex flex-column">
      
      <div v-if="step === 1">
        <div class="row g-2 mb-4">
          <div class="col-6">
            <button @click="iniciarFluxo('pix')" class="btn btn-outline-danger w-100 py-4 rounded-4 fw-bold shadow-sm">
              <i class="bi bi-qr-code-scan d-block mb-1 fs-3"></i> Pix
            </button>
          </div>
          <div class="col-6">
            <button @click="iniciarFluxo('ted')" class="btn btn-outline-dark w-100 py-4 rounded-4 fw-bold shadow-sm">
              <i class="bi bi-bank d-block mb-1 fs-3"></i> Transferir
            </button>
          </div>
        </div>

        <h6 class="fw-bold mb-3 small text-muted text-uppercase">Contatos Recentes</h6>
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
          <div class="list-group list-group-flush">
            <button v-for="contato in contatos" :key="contato.nome" 
                    @click="selecionarContato(contato)"
                    class="list-group-item list-group-item-action py-3 d-flex align-items-center gap-3 border-0 border-bottom">
              <div class="avatar-sm bg-danger text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
                {{ contato.nome.charAt(0) }}
              </div>
              <div class="text-start">
                <p class="m-0 fw-bold small text-dark">{{ contato.nome }}</p>
                <p class="m-0 text-muted extra-small">{{ contato.banco }}</p>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div v-if="step === 2">
        <div v-if="fluxo === 'pix'" class="mb-3">
          <label class="form-label small fw-bold text-muted">Tipo de Chave</label>
          <select class="form-select border-0 bg-white p-3 rounded-3 shadow-sm mb-4" v-model="dados.tipoChave" @change="dados.chave = ''">
            <option value="cpf">CPF</option>
            <option value="celular">Celular</option>
            <option value="email">E-mail</option>
            <option value="aleatoria">Chave Aleatória</option>
          </select>

          <label class="form-label small fw-bold text-muted">Identificação da Chave</label>
          <input 
            v-if="maskSelector"
            type="text" 
            class="form-control border-0 bg-white p-3 rounded-3 shadow-sm" 
            v-model="dados.chave" 
            v-mask="maskSelector"
            :placeholder="placeholderSelector"
          >
          <input 
            v-else
            type="text" 
            class="form-control border-0 bg-white p-3 rounded-3 shadow-sm" 
            v-model="dados.chave" 
            :placeholder="placeholderSelector"
          >
        </div>

        <div v-else class="mb-3">
          <label class="form-label small fw-bold text-muted">Agência</label>
          <input type="text" class="form-control border-0 bg-white p-3 rounded-3 shadow-sm mb-3" 
                 v-model="dados.agencia" v-mask="'####'" placeholder="0001">

          <label class="form-label small fw-bold text-muted">Conta com dígito</label>
          <input type="text" class="form-control border-0 bg-white p-3 rounded-3 shadow-sm" 
                 v-model="dados.conta" v-mask="'#######-#'" placeholder="0000000-0">
        </div>

        <button @click="proximoStep" class="btn btn-danger w-100 py-3 rounded-4 fw-bold mt-3" 
                :disabled="fluxo === 'pix' ? !dados.chave : (!dados.agencia || !dados.conta)">
          Continuar
        </button>
      </div>

      <div v-if="step === 3" class="flex-grow-1 d-flex flex-column">
        <div class="d-flex flex-grow-1 align-items-center justify-content-center">
          <div class="input-money-container bg-white shadow-sm d-flex align-items-center justify-content-center p-4 rounded-5">
            <span class="fs-2 fw-bold text-danger">R$</span>
            <input 
              type="text" class="money-input fw-bold text-dark border-0 bg-transparent" 
              :value="valorExibido" @input="handleValorInput" :style="{ width: inputWidth }"
              inputmode="numeric" placeholder="0,00"
            >
          </div>
        </div>
        <button @click="proximoStep" class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mb-3" 
                :disabled="!dados.valor || dados.valor <= 0">
          Continuar
        </button>
      </div>

      <div v-if="step === 4" class="flex-grow-1 d-flex flex-column">
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
          <div class="text-center mb-4">
            <span class="text-muted small">Você está enviando</span>
            <h2 class="fw-bold text-dark">{{ formatarMoedaFinal(dados.valor) }}</h2>
          </div>
          <div class="d-flex flex-column gap-3">
            <div class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Para</label>
              <p class="m-0 fw-bold text-dark">{{ dados.nome || 'Destinatário Externo' }}</p>
            </div>
            <div v-if="fluxo === 'pix'" class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Chave Pix ({{ dados.tipoChave }})</label>
              <p class="m-0 fw-medium text-dark">{{ dados.chave }}</p>
            </div>
            <div v-else class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Dados Bancários</label>
              <p class="m-0 fw-medium text-dark">Ag. {{ dados.agencia }} / Cc. {{ dados.conta }}</p>
            </div>
          </div>
        </div>
        <button @click="processarPagamento" class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mt-auto mb-3">
          Confirmar Envio
        </button>
      </div>

      <div v-if="step === 'sucesso'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-circle bg-success text-white mb-4 animate-bounce">
          <i class="bi bi-check-lg display-3"></i>
        </div>
        <h3 class="fw-bold">Envio realizado!</h3>
        <button @click="resetarFluxoCompleto" class="btn btn-dark w-100 py-3 rounded-4 fw-bold mt-5">Concluir</button>
      </div>

      <div v-if="step === 'erro'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-circle bg-danger text-white mb-4 animate-shake">
          <i class="bi bi-x-lg display-3"></i>
        </div>
        <h3 class="fw-bold">Erro no envio</h3>
        <button @click="step = 4" class="btn btn-danger w-100 py-3 rounded-4 fw-bold mt-5">Tentar novamente</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap';



let offcanvasBS = null;
const step = ref(1);
const fluxo = ref('');
const dados = ref({ tipoChave: 'cpf', chave: '', agencia: '', conta: '', valor: 0, nome: '' });

const contatos = [{ nome: 'Franklin Clinton', banco: 'Maze Bank' }, { nome: 'Lamar Davis', banco: 'Fleeca Bank' }];

// MÁSCARAS V-MASK
const maskSelector = computed(() => {
  if (dados.value.tipoChave === 'cpf') return '###.###.###-##';
  if (dados.value.tipoChave === 'celular') return '(##) #####-####';
  return null;
});

const placeholderSelector = computed(() => {
  const map = { cpf: '000.000.000-00', celular: '(00) 00000-0000', email: 'seu@email.com', aleatoria: 'Chave' };
  return map[dados.value.tipoChave];
});

// LÓGICA DO DINHEIRO (MANUAL PARA PRECISÃO)
const valorExibido = computed(() => {
  if (dados.value.valor === 0) return "0,00";
  return (dados.value.valor / 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
});

const handleValorInput = (event) => {
  let somenteNumeros = event.target.value.replace(/\D/g, "");
  if (somenteNumeros.length > 10) somenteNumeros = somenteNumeros.slice(0, 10);
  dados.value.valor = somenteNumeros ? parseInt(somenteNumeros) : 0;
  event.target.value = valorExibido.value;
};

const inputWidth = computed(() => `${valorExibido.value.length * 22 + 20}px`);
const formatarMoedaFinal = (val) => (val / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

// NAVEGAÇÃO
const tituloStep = computed(() => {
  const titulos = { 1: 'Transferir', 2: 'Dados de envio', 3: 'Qual o valor?', 4: 'Confirmar' };
  return titulos[step.value] || '';
});

const iniciarFluxo = (t) => { fluxo.value = t; step.value = 2; };
const selecionarContato = (c) => { dados.value.nome = c.nome; fluxo.value = 'ted'; step.value = 3; };
const proximoStep = () => step.value++;
const voltarStep = () => step.value--;

const processarPagamento = () => {
  setTimeout(() => { step.value = dados.value.valor > 500000 ? 'erro' : 'sucesso'; }, 1000);
};

const resetarFluxoCompleto = () => {
  offcanvasBS?.hide();
  setTimeout(() => { 
    step.value = 1; 
    dados.value = { tipoChave: 'cpf', chave: '', agencia: '', conta: '', valor: 0, nome: '' }; 
  }, 400);
};

onMounted(() => {
  const el = document.getElementById('offcanvasTransferencia');
  if (el) offcanvasBS = new Offcanvas(el);
});

const abrirTransferencia = () => offcanvasBS?.show();
defineExpose({ abrirTransferencia });
</script>

<style scoped>
#offcanvasTransferencia { 
  height: calc(100vh - 72px) !important; 
  border-radius: 30px 30px 0 0; 
}

.avatar-sm { 
  width: 45px; 
  height: 45px; 
}

.extra-small { 
  font-size: 0.7rem;
}
.input-money-container { 
  display: inline-flex; 
  max-width: 95%; 
  transition: all 0.2s ease; 
}
.money-input { 
  font-size: 2.5rem; 
  outline: none; 
  text-align: left; 
  padding-left: 10px; 
  width: 100%; 
}
.status-circle {
  width: 100px; 
  height: 100px; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
}
</style>