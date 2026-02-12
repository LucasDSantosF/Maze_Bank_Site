<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" ref="sidebarRef" id="offcanvasPix" >
      <div class="offcanvas-header border-bottom py-3">
          <h5 class="offcanvas-title fw-bold text-dark">
          <i class="bi bi-qr-code-scan text-danger me-2"></i>Área Pix
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body bg-light">
          <div class="card border-0 shadow-sm mb-4 rounded-4 overflow-hidden">
          <button 
              class="btn btn-danger py-3 fw-bold d-flex align-items-center justify-content-center gap-2"
              @click="$emit('abrirTransferencia')">
              <i class="bi bi-send-fill"></i> Transferir via Pix
          </button>
          </div>

          <section class="mb-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="fw-bold m-0">Minhas Chaves</h6>
              <a href="#" class="text-danger small fw-bold text-decoration-none" @click="$emit('abrirChaves')">Gerenciar</a>
          </div>
          <div class="card border-0 shadow-sm rounded-4">
              <div class="list-group list-group-flush">
              <div v-for="chave in minhasChaves" :key="chave.chave" class="list-group-item bg-transparent d-flex justify-content-between py-3">
                  <span class="text-muted small">{{ chave.tipo }}</span>
                  <span class="fw-bold small">{{ chave.chave }}</span>
              </div>
              </div>
          </div>
          </section>

          <section>
          <div class="d-flex justify-content-between align-items-center mb-3">
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
  </div>

  <ErrorModal 
    v-if="erroFatal" 
    :erroMsg="erroMsg" 
    @retry="recarregar" 
  />
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { Offcanvas } from 'bootstrap';
import { pix } from '../../api/models/apis';
import ErrorModal from './ErrorModal.vue';

const isloading = ref(true);
const erroFatal = ref(false);
const erroMsg = ref(undefined);
const sidebarRef = ref(null);
let pixOffcanvas = null;

const minhasChaves = ref([]);
const ultimasTransferencias = ref([]);

onMounted(async () => {
  await pegarChaves();
  await pegarTransferencias();
  isloading.value = false;

  await nextTick();

  if (sidebarRef.value) {
    pixOffcanvas = new Offcanvas(sidebarRef.value);
  }
});

const recarregar = async () => {
  erroFatal.value = false;
  await pegarChaves();
  await pegarTransferencias();
};

async function pegarChaves() {
  try {
    const response = await pix.chaves();
    minhasChaves.value = response.data;
  } catch (error) {
    erroMsg.value = error.response?.data?.message || undefined;
    erroFatal.value = true;
  }
}

async function pegarTransferencias() {
  try {
    const response = await pix.resumo();
    ultimasTransferencias.value = response.data.map((transferencias) => {
       return {
        nome: transferencias.recebedor_nome, 
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

const abrirPix = () => {
  if (pixOffcanvas) {
    pixOffcanvas.show();
  } else {
    const el = document.getElementById('offcanvasPix');
    if (el) {
      pixOffcanvas = new Offcanvas(el);
      pixOffcanvas.show();
    }
  }
};

const formatarTipo = (tipo) => tipo === "PIX_ENVIADO" ? '-' : '+'


const isEntrada = (tipo) => tipo === "PIX_RECEBIDO"

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

defineExpose({
  abrirPix
});
</script>

<style scoped>
#offcanvasPix {
  height: calc(100vh - 72px) !important;
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;
  transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.avatar-sm {
  width: 35px;
  height: 35px;
  font-size: 0.9rem;
}

.last-item-border:last-child {
  border-bottom: none !important;
}

.offcanvas-body {
  background-color: #f8f9fa;
}

.list-group-item:active {
  background-color: rgba(0,0,0,0.05);
}
</style>