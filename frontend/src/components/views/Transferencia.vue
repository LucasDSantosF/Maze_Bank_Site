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
      <ErrorAlert
        v-if="mostrarErro"
        :mensagem="erroMsgAlert"
        @close="mostrarErro = false"
      />
      
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
            <div v-for="contato in contatos" :key="contato.nome" 
                class="list-group-item py-3 d-flex align-items-center justify-content-between border-0 border-bottom">
              
              <div class="d-flex align-items-center gap-3 cursor-pointer flex-grow-1">
                <div class="avatar-sm bg-danger text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
                  {{ contato.nome.charAt(0) }}
                </div>
                <div class="text-start">
                  <p class="m-0 fw-bold small text-dark">{{ contato.nome }}</p>
                  <p class="m-0 text-muted extra-small">Ag. {{ contato.dados.agencia || '0001' }} / Cc. {{ contato.dados.conta }}</p>
                  <p v-if="contato.chave.chave" class="m-0 text-muted extra-small text-truncate" style="max-width: 150px;">
                    <i class="bi bi-qr-code-scan"></i> {{ contato.chave.tipo }}: {{ contato.chave.chave }}
                  </p>
                </div>
              </div>

              <div class="d-flex gap-2">
                <button v-if="contato.chave" 
                        @click.stop="iniciarPixDireto(contato)" 
                        class="btn btn-sm btn-outline-danger rounded-circle action-btn"
                        title="Transferir via Pix">
                  <i class="bi bi-qr-code-scan"></i>
                </button>

                <button @click.stop="iniciarTedDireto(contato)" 
                        class="btn btn-sm btn-outline-dark rounded-circle action-btn"
                        title="Transferir via TED">
                  <i class="bi bi-bank"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <section>
            <div class="d-flex justify-content-between align-items-center mb-3 mt-4">
                <h6 class="fw-bold m-0">Últimas Transferências</h6>
                <a href="#" class="text-danger small fw-bold text-decoration-none"  @click="$emit('abrirExtrato')">Ver Extrato</a>
            </div>
            <div class="card border-0 shadow-sm rounded-4 p-2">
                <div v-for="t in ultimasTransferencias" :key="t.nome" class="d-flex align-items-center justify-content-between p-2 border-bottom last-item-border">
                <div class="d-flex align-items-center gap-3">
                    <div 
                      :class="['icon-box rounded-circle d-flex align-items-center justify-content-center', 
                      t.is_entrada ? 'bg-success bg-opacity-10 text-success' : 'bg-danger bg-opacity-10 text-danger']">
                        <i :class="t.is_entrada ? 'bi bi-arrow-down-left' : 'bi bi-arrow-up-right'"></i>
                    </div>
                    <div>
                    <p class="m-0 fw-bold small text-dark">{{ t.nome }}</p>
                    <p class="m-0 text-muted small" style="font-size: 0.7rem;">{{ t.data }}</p>
                    </div>
                </div>
                <span :class="['fw-bold small', t.is_entrada ? 'text-success' : 'text-dark']">{{ t.valor }}</span>
                </div>
            </div>
            </section>
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
        <button 
          @click="sinalizar" 
          class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mb-3" 
          :disabled="(!dados.valor || dados.valor <= 0) && isLoadingBotaoSinalizar">
          <span 
              v-if="isLoadingBotaoSinalizar" 
              class="spinner-border spinner-border-sm me-2" 
              role="status" 
          />
          <span>Continuar</span>
        </button>
      </div>

      <div v-if="step === 4" class="flex-grow-1 d-flex flex-column">
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
          <div class="text-center mb-4">
            <span class="text-muted small">Você está enviando</span>
            <h2 class="fw-bold text-dark">{{ formatarMoedaFinal(dados.valor) }}</h2>
          </div>
          <div class="d-flex flex-column gap-3">
            <div v-if="fluxo === 'pix'" class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Chave Pix ({{dadosConfirmar.chave.tipo }})</label>
              <p class="m-0 fw-medium text-dark">{{ dadosConfirmar.chave.chave }}</p>
            </div>
            <div class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">De</label>
              <p class="m-0 fw-bold text-dark">{{ dadosConfirmar.remetente.nome || 'Remetente' }}</p>
            </div>
            <div class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Dados Bancários</label>
              <p v-if="dadosConfirmar.remetente.conta" class="m-0 fw-medium text-dark">
                Ag. {{ dadosConfirmar.remetente.agencia || '0001' }} / Cc. {{ dadosConfirmar.remetente.conta }}
              </p>
              <p v-if="dadosConfirmar.remetente.cpf" class="m-0 fw-medium text-dark">CPF: {{ dadosConfirmar.remetente.cpf }} </p>
            </div>
            <div class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Para</label>
              <p class="m-0 fw-bold text-dark">{{ dadosConfirmar.recebedor.nome || 'Recebedor Externo' }}</p>
            </div>
            <div class="border-bottom pb-2">
              <label class="extra-small text-muted text-uppercase fw-bold">Dados Bancários</label>
              <p  v-if="dadosConfirmar.recebedor.conta" class="m-0 fw-medium text-dark">Ag. {{ dadosConfirmar.recebedor.agencia }} / Cc. {{ dadosConfirmar.recebedor.conta }}</p>
              <p v-if="dadosConfirmar.recebedor.cpf" class="m-0 fw-medium text-dark">CPF: {{ dadosConfirmar.recebedor.cpf }} </p>
            </div>
          </div>
        </div>
        <button 
          @click="processarPagamento" 
          class="btn btn-danger w-100 py-3 rounded-4 fw-bold shadow-lg mt-auto mb-3"
          :disabled="isLoadingBotaoConfirmar">
          <span 
              v-if="isLoadingBotaoConfirmar" 
              class="spinner-border spinner-border-sm me-2" 
              role="status" 
          />
          <span>Confirmar Envio</span>
        </button>
      </div>

      <div v-if="step === 'sucesso'" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
        <div class="status-circle bg-success text-white mb-4 animate-bounce">
          <i class="bi bi-check-lg display-3"></i>
        </div>
        <h3 class="fw-bold">Envio realizado!</h3>
        <p class="text-muted">O valor de <span class="fw-bold text-dark">{{ formatarMoedaFinal(dados.valor) }}</span> foi enviado para <strong>{{ dadosConfirmar.recebedor.nome }}</strong>.</p>
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

  <ErrorModal 
    v-if="erroFatal" 
    :erroMsg="erroMsg" 
    @retry="recarregar" 
  />
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap';
import { transactions } from '../../api/models/apis';
import ErrorModal from './ErrorModal.vue';
import ErrorAlert from '../Alert/ErrorAlert.vue';

const router = useRouter();

let offcanvasBS = null;
const step = ref(1);
const fluxo = ref('');
const mostrarErro = ref(false);
const erroMsgAlert = ref(undefined);
const erroFatal = ref(false);
const isLoadingBotaoSinalizar = ref(false);
const isLoadingBotaoConfirmar = ref(false);
const erroMsg = ref(undefined);
const dados = ref({ 
  tipoChave: 'cpf', 
  chave: '', 
  agencia: '', 
  conta: '', 
  valor: 0, 
  nome: '' 
});
const dadosConfirmar = ref({
  id_transferencia: '',
  tipoChave: 'cpf', 
  chave: '', 
  remetente: {
    nome: '',
    conta: '',
    cpf: '',
  },
  recebedor: {
        nome: '',
        cpf: '',
        agencia: '',
        conta: ''
  },
  chave: {
    chave: '', 
    tipo: ''
  },
  valor: 0,
});
const contatos = ref([]);
const ultimasTransferencias = ref([]);

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

const tituloStep = computed(() => {
  const titulos = { 1: 'Transferir', 2: 'Dados de envio', 3: 'Qual o valor?', 4: 'Confirmar' };
  return titulos[step.value] || '';
});

const iniciarFluxo = (t) => { fluxo.value = t; step.value = 2; };
const proximoStep = () => step.value++;
const voltarStep = () => step.value--;
const iniciarPixDireto = (contato) => {
  dados.value.chave = contato.chave.chave
  dados.value.tipoChave = contato.chave.tipo
  fluxo.value = 'pix'; 
  step.value = 3; 
};
const iniciarTedDireto = (contato) => { 
  dados.value.agencia = contato.dados.agencia
  dados.value.conta = contato.dados.conta
  fluxo.value = 'ted'; 
  step.value = 3; 
};

const formatarTipo = (tipo) => isEntrada(tipo) ? '+' : '-'

const isEntrada = (tipo) => tipo === 'DEPOSITO' || tipo.endsWith('_RECEBIDO') || tipo.endsWith('_RECEBIDA');

const getNomeExibicao = (item) => {
  if (item.tipo === 'SAQUE') return 'Saque Caixa Eletrônico';
  if (item.tipo === 'DEPOSITO') return 'Depósito Recebido';

  return isEntrada(item.tipo) ? (item.remetente_nome || 'Maze User') : (item.recebedor_nome || 'Maze User');
};

const formatarData = (dataString) => {
  if (!dataString) return "";

  const dataAlvo = new Date(dataString);
  const hoje = new Date();

  const dataAlvoZerada = new Date(dataAlvo.getFullYear(), dataAlvo.getMonth(), dataAlvo.getDate());
  const hojeZerado = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());

  const diffDias = Math.round((hojeZerado - dataAlvoZerada) / (1000 * 60 * 60 * 24));

  if (diffDias === 0) return "Hoje";
  if (diffDias === 1) return "Ontem";

  const dia = dataAlvo.getDate().toString().padStart(2, '0');
  const mes = dataAlvo.toLocaleString('pt-BR', { month: 'short' }).replace('.', '');
  const ano = dataAlvo.getFullYear();

  const mesFormatado = mes.charAt(0).toUpperCase() + mes.slice(1);

  return `${dia} ${mesFormatado} ${ano}`;
};

const resetarFluxoCompleto = () => {
  offcanvasBS?.hide();
  router.push({name: 'Login'})
};

onMounted(async () => {
  await pegarContatos();
  await pegarTransferencias();

  const el = document.getElementById('offcanvasTransferencia');
  if (el) offcanvasBS = new Offcanvas(el);
});

const recarregar = async () => {
  erroFatal.value = false;
  await pegarContatos();
  await pegarTransferencias();
};

async function pegarContatos() {
  try {
    const response = await transactions.contatos();
    contatos.value = response.data
  } catch (error) {
    erroMsg.value = error.response?.data?.message || undefined;
    erroFatal.value = true;
  }
}

async function pegarTransferencias() {
  try {
    const response = await transactions.resumo();
    ultimasTransferencias.value = response.data.map((transferencias) => {
      const nome = transferencias.tipo == 'SAQUE' ? '' : transferencias.recebedor_nome
       return {
        nome: getNomeExibicao(transferencias), 
        valor: `${formatarTipo(transferencias.tipo)} R$ ${(transferencias.valor/100).toFixed(2)}`, 
        data: formatarData(transferencias.data),
        is_entrada: isEntrada(transferencias.tipo),
       }
    })
  } catch (error) {
    erroMsg.value = error.response?.data?.message || undefined;
    erroFatal.value = true;
  }
}

async function sinalizar() {
  isLoadingBotaoSinalizar.value = true;
  if(dados.value.agencia != '' && dados.value.conta != '') {
    await ted();
  }  else {
    await pix();
  };
  isLoadingBotaoSinalizar.value = false;
}


async function ted() {
  try {
    const payload = {
      valor: dados.value.valor,
      agencia: dados.value.agencia,
      conta: dados.value.conta,
    }
    const response = await transactions.ted(payload);
    dadosConfirmar.value = response.data
    proximoStep();
  } catch (error) {
    erroMsgAlert.value = error.response?.data?.message || undefined;
    mostrarErro.value = true;
  }
}

async function pix() {
  try {
    const payload = {
      valor: dados.value.valor,
      chave: dados.value.chave,
      tipo_chave: dados.value.tipoChave,
    }
    const response = await transactions.pix(payload);
    dadosConfirmar.value = response.data
    proximoStep();
  } catch (error) {
    erroMsgAlert.value = error.response?.data?.message || undefined;
    mostrarErro.value = true;
  }
}

async function processarPagamento() {
  isLoadingBotaoConfirmar.value = true;
  try {
    const payload = {
      id_transferencia: dadosConfirmar.value.id_transferencia,
    }

    const response = await transactions.confirmar(payload);
    step.value = 'sucesso';
  } catch (error) {
    step.value = 'erro';
  } finally {
    isLoadingBotaoConfirmar.value = false;
  }
};

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