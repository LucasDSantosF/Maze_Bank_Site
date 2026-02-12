<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasExtrato">
    <div class="offcanvas-header border-bottom py-3">
      <h5 class="offcanvas-title fw-bold text-dark">
        <i class="bi bi-receipt text-danger me-2"></i>Extrato
      </h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
    </div>

    <div class="offcanvas-body bg-light">
      <div class="mb-4">
        <label class="form-label extra-small fw-bold text-muted text-uppercase mb-2">Filtrar por tipo</label>
        <div class="d-flex gap-2 overflow-auto pb-2 custom-scrollbar">
          <button v-for="filtro in opcoesFiltro" :key="filtro.id"
                  @click="alterarFiltroTipo(filtro.id)"
                  :class="['btn btn-sm rounded-pill px-3 fw-bold transition', 
                           filtroAtivo === filtro.id ? 'btn-danger shadow-sm' : 'btn-white border-0 text-muted shadow-sm']">
            {{ filtro.label }}
          </button>
        </div>
        
        <div class="mt-3">
          <label class="form-label extra-small fw-bold text-muted text-uppercase mb-2">Período Selecionado</label>
          <div class="row g-2">
            <div class="col-6">
              <div class="date-field">
                <span class="date-label">Início</span>
                <input type="date" class="form-control border-0 bg-white rounded-3 shadow-sm pt-4" 
                       v-model="periodo.inicio" @change="carregarExtrato">
              </div>
            </div>
            <div class="col-6">
              <div class="date-field">
                <span class="date-label">Fim</span>
                <input type="date" class="form-control border-0 bg-white rounded-3 shadow-sm pt-4" 
                       v-model="periodo.fim" @change="carregarExtrato">
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div v-if="carregando" class="text-center py-5">
          <div class="spinner-border text-danger spinner-border-sm" role="status"></div>
          <p class="extra-small text-muted mt-2">Sincronizando Maze Bank...</p>
        </div>

        <div v-else class="list-group list-group-flush">
          <button v-for="item in transacoesFiltradas" :key="item.id"
                  @click="verDetalhes(item)"
                  class="list-group-item list-group-item-action py-3 border-0 border-bottom d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-3">
              <div :class="['icon-box rounded-circle d-flex align-items-center justify-content-center', 
                            isEntrada(item.tipo) ? 'bg-success bg-opacity-10 text-success' : 'bg-danger bg-opacity-10 text-danger']">
                <i :class="isEntrada(item.tipo) ? 'bi bi-arrow-down-left' : 'bi bi-arrow-up-right'"></i>
              </div>
              <div class="text-start">
                <p class="m-0 fw-bold small text-dark">{{ getNomeExibicao(item) }}</p>
                <p class="m-0 text-muted extra-small">{{ formatarData(item.data) }} • {{ formatarCategoria(item.tipo) }}</p>
              </div>
            </div>
            <span :class="['fw-bold', isEntrada(item.tipo) ? 'text-success' : 'text-dark']">
              {{ isEntrada(item.tipo) ? '+' : '-' }} {{ formatarMoeda(item.valor) }}
            </span>
          </button>
          
          <div v-if="transacoesFiltradas.length === 0" class="p-5 text-center">
            <p class="text-muted small">Nenhuma transação encontrada.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="modalDetalheTransacao" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 rounded-5 shadow-lg overflow-hidden">
        <div class="bg-danger p-4 text-white text-center">
          <i class="bi bi-check-circle-fill display-4"></i>
          <h5 class="fw-bold mt-2">Comprovante</h5>
        </div>
        <div class="modal-body p-4" v-if="itemSelecionado">
          <div class="text-center mb-4">
            <span class="text-muted small">Valor total</span>
            <h2 class="fw-bold text-dark">{{ formatarMoeda(itemSelecionado.valor) }}</h2>
          </div>
          <div class="d-flex flex-column gap-3">
            <div v-for="(val, key) in detalhesComprovante" :key="key">
              <label class="extra-small text-muted text-uppercase fw-bold">{{ key }}</label>
              <p class="m-0 fw-medium text-dark">{{ val }}</p>
            </div>
          </div>
        </div>
        <div class="modal-footer border-0 p-4">
          <button type="button" class="btn btn-light w-100 py-3 fw-bold rounded-4" data-bs-dismiss="modal">Fechar</button>
        </div>
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
import { ref, computed, onMounted } from 'vue';
import { Offcanvas, Modal } from 'bootstrap';
import { transactions } from '../../api/models/apis';
import ErrorModal from './ErrorModal.vue';

let offcanvasBS = null;
let modalBS = null;

const erroFatal = ref(false);
const erroMsg = ref(undefined);
const carregando = ref(false);
const filtroAtivo = ref('todos');
const periodo = ref({ inicio: '', fim: '' });
const itemSelecionado = ref(null);
const transacoes = ref([]);

const opcoesFiltro = [
  { id: 'todos', label: 'Tudo' },
  { id: 'entrada', label: 'Entradas' },
  { id: 'saida', label: 'Saídas' },
  { id: 'pix', label: 'Pix' }
];

onMounted(async () => {
  offcanvasBS = new Offcanvas(document.getElementById('offcanvasExtrato'));
  modalBS = new Modal(document.getElementById('modalDetalheTransacao'));
  await carregarExtrato();
});

const recarregar = async () => {
  erroFatal.value = false;
  await carregarExtrato();
};

const isEntrada = (tipo) => tipo === 'DEPOSITO' || tipo.endsWith('_RECEBIDO') || tipo.endsWith('_RECEBIDA');

const getNomeExibicao = (item) => {
  if (item.tipo === 'SAQUE') return 'Saque Caixa Eletrônico';
  if (item.tipo === 'DEPOSITO') return 'Depósito Recebido';

  return isEntrada(item.tipo) ? (item.remetente_nome || 'Maze User') : (item.recebedor_nome || 'Maze User');
};

const formatarCategoria = (tipo) => {
  if (tipo.includes('PIX')) return 'Pix';
  if (tipo.includes('TRANSFERENCIA')) return 'TED';
  if (tipo === 'DEPOSITO') return 'Depósito';
  return 'Saque';
};

const carregarExtrato = async () => {
  carregando.value = true;
  try {
    const filtros = {
      tipo: filtroAtivo.value === 'todos' ? null : filtroAtivo.value,
      data_inicio: periodo.value.inicio ? `${periodo.value.inicio}T00:00:00` : null,
      data_fim: periodo.value.fim ? `${periodo.value.fim}T23:59:59` : null
    };
    const response = await transactions.extrato(filtros)
    transacoes.value = response.data;
  } catch (e) {
    erroMsg.value = error.response?.data?.message || undefined;
    erroFatal.value = true;
  } finally {
    carregando.value = false;
  }
};

const alterarFiltroTipo = (id) => {
  filtroAtivo.value = id;
  carregarExtrato();
};

const transacoesFiltradas = computed(() => {
  return [...transacoes.value].sort((a, b) => new Date(b.data) - new Date(a.data));
});

const verDetalhes = (item) => {
  itemSelecionado.value = item;
  modalBS.show();
};

const detalhesComprovante = computed(() => {
  if (!itemSelecionado.value) return {};
  const t = itemSelecionado.value;
  return {
    "Operação": formatarCategoria(t.tipo),
    "ID": t.id_transferencia.split('-')[0].toUpperCase(),
    "Data": new Date(t.data).toLocaleString('pt-BR'),
    [isEntrada(t.tipo) ? 'Remetente' : 'Recebedor']: getNomeExibicao(t),
    "Documento": isEntrada(t.tipo) ? t.remetente_cpf : t.recebedor_cpf,
    "Status": "Efetivado"
  };
});

const formatarMoeda = (val) => {
  const real = (val || 0) / 100;
  return real.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

const formatarData = (dataString) => {
  if (!dataString) return "";
  const d = new Date(dataString);
  const hoje = new Date();
  if (d.toDateString() === hoje.toDateString()) return "Hoje";
  hoje.setDate(hoje.getDate() - 1);
  if (d.toDateString() === hoje.toDateString()) return "Ontem";
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }).replace('.', '');
};

defineExpose({ abrirExtrato: () => offcanvasBS.show() });
</script>

<style scoped>
#offcanvasExtrato {
  height: calc(100vh - 72px) !important;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}

.date-field {
  position: relative;
}

.date-label {
  position: absolute;
  top: 5px;
  left: 12px;
  font-size: 0.65rem;
  font-weight: 800;
  color: hsl(var(--primary)) !important;
  z-index: 5;
}

.icon-box { width: 45px; height: 45px; flex-shrink: 0; }
.extra-small { font-size: 0.72rem; }
.btn-white { background-color: hsl(var(--card)) !important; }

.custom-scrollbar::-webkit-scrollbar { display: none; }
.custom-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

input[type="date"] {
  font-size: 0.8rem;
  font-weight: 600;
}
</style>