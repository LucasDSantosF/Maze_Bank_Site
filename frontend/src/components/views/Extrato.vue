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
                  @click="filtroAtivo = filtro.id"
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
                       v-model="periodo.inicio">
              </div>
            </div>
            <div class="col-6">
              <div class="date-field">
                <span class="date-label">Fim</span>
                <input type="date" class="form-control border-0 bg-white rounded-3 shadow-sm pt-4" 
                       v-model="periodo.fim">
              </div>
            </div>
          </div>
          <div v-if="periodo.inicio || periodo.fim" class="mt-2 text-end">
             <button class="btn btn-link btn-sm text-danger p-0 extra-small fw-bold text-decoration-none" @click="limparDatas">
               LIMPAR FILTRO DE DATA
             </button>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="list-group list-group-flush">
          <button v-for="item in transacoesFiltradas" :key="item.id"
                  @click="verDetalhes(item)"
                  class="list-group-item list-group-item-action py-3 border-0 border-bottom d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-3">
              <div :class="['icon-box rounded-circle d-flex align-items-center justify-content-center', 
                            item.tipo === 'entrada' ? 'bg-success bg-opacity-10 text-success' : 'bg-danger bg-opacity-10 text-danger']">
                <i :class="item.tipo === 'entrada' ? 'bi bi-arrow-down-left' : 'bi bi-arrow-up-right'"></i>
              </div>
              <div>
                <p class="m-0 fw-bold small text-dark">{{ item.titulo }}</p>
                <p class="m-0 text-muted extra-small">{{ formatarData(item.data) }} • {{ item.categoria }}</p>
              </div>
            </div>
            <span :class="['fw-bold', item.tipo === 'entrada' ? 'text-success' : 'text-dark']">
              {{ item.tipo === 'entrada' ? '+' : '-' }} {{ formatarMoeda(item.valor) }}
            </span>
          </button>
          
          <div v-if="transacoesFiltradas.length === 0" class="p-5 text-center">
            <i class="bi bi-calendar-x text-muted display-6"></i>
            <p class="text-muted mt-2 small">Nenhuma transação neste período.</p>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Offcanvas, Modal } from 'bootstrap';

let offcanvasBS = null;
let modalBS = null;

const filtroAtivo = ref('todos');
const periodo = ref({ inicio: '', fim: '' });
const itemSelecionado = ref(null);

const opcoesFiltro = [
  { id: 'todos', label: 'Tudo' },
  { id: 'entrada', label: 'Entradas' },
  { id: 'saida', label: 'Saídas' },
  { id: 'pix', label: 'Pix' }
];

const transacoes = ref([
  { id: 1, tipo: 'saida', titulo: 'Pagamento de Conta', categoria: 'Pix', valor: 150.00, data: '2026-01-25', destino: 'Energisa S/A' },
  { id: 2, tipo: 'entrada', titulo: 'Depósito Recebido', categoria: 'Transferência', valor: 2500.00, data: '2026-01-24', origem: 'Maze Bank Corp' },
  { id: 3, tipo: 'saida', titulo: 'Restaurante Vinewood', categoria: 'Crédito', valor: 89.90, data: '2026-01-22', destino: 'Vinewood Grill' },
  { id: 4, tipo: 'saida', titulo: 'Transferência Pix', categoria: 'Pix', valor: 450.00, data: '2026-01-20', destino: 'Franklin Clinton' }
]);

const transacoesFiltradas = computed(() => {
  return transacoes.value.filter(t => {
    const matchFiltro = filtroAtivo.value === 'todos' || t.tipo === filtroAtivo.value || t.categoria.toLowerCase() === filtroAtivo.value;
    const dataTransacao = new Date(t.data);
    const dataInicio = periodo.value.inicio ? new Date(periodo.value.inicio) : null;
    const dataFim = periodo.value.fim ? new Date(periodo.value.fim) : null;
    
    let matchData = true;
    if (dataInicio) matchData = matchData && dataTransacao >= dataInicio;
    if (dataFim) matchData = matchData && dataTransacao <= dataFim;
    return matchFiltro && matchData;
  }).sort((a, b) => new Date(b.data) - new Date(a.data));
});

const detalhesComprovante = computed(() => {
  if (!itemSelecionado.value) return {};
  const t = itemSelecionado.value;
  return {
    "Transação": t.titulo,
    "Data": formatarData(t.data),
    "ID Transação": Math.random().toString(36).substr(2, 9).toUpperCase(),
    [t.tipo === 'entrada' ? 'Origem' : 'Destino']: t.origem || t.destino,
    "Status": "Concluído"
  };
});

onMounted(() => {
  offcanvasBS = new Offcanvas(document.getElementById('offcanvasExtrato'));
  modalBS = new Modal(document.getElementById('modalDetalheTransacao'));
});

const limparDatas = () => { periodo.value = { inicio: '', fim: '' }; };
const abrirExtrato = () => offcanvasBS?.show();
const verDetalhes = (item) => {
  itemSelecionado.value = item;
  modalBS?.show();
};

const formatarMoeda = (val) => val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
const formatarData = (dataStr) => {
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

defineExpose({ abrirExtrato });
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