<template>
  <div class="min-vh-100 bg-light" v-if="!isloading">
    
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-2 fixed-top">
      <div class="container">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img src="/src/assets/imagens/Maze-Bank-png-logo-download.png" alt="Logo" height="50">
        </a>

        <div class="d-flex align-items-center gap-3">
          <div class="d-flex align-items-center gap-2 border-start ps-3 avatar-group-container">
            <div 
              class="avatar-circle cursor-pointer" 
              @click="toggleSidebar"
            >
              {{ user.avatar }}
            </div>
            <div class="d-none d-md-block">
              <p class="m-0 fw-bold small">{{ user.nome }} {{ user.sobrenome }}</p>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div 
      class="offcanvas offcanvas-end border-0 shadow" 
      tabindex="-1" 
      ref="sidebarRef" 
      aria-labelledby="sidebarPerfilLabel"
    >
      <div class="offcanvas-header bg-danger text-white">
        <h5 class="offcanvas-title fw-bold" id="sidebarPerfilLabel">Meu Perfil</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body d-flex flex-column">
        <div class="text-center mb-4">
          <div class="avatar-circle mx-auto mb-2" style="width: 80px; height: 80px; font-size: 2rem;">
            {{ user.avatar }}
          </div>
          <h5 class="fw-bold mb-0 text-dark">{{ user.nome }} {{ user.sobrenome }}</h5>
        </div>

        <div class="list-group list-group-flush">
          <div class="list-group-item px-0 py-3">
            <small class="text-muted d-block small-label">E-mail</small>
            <span class="fw-semibold text-dark">{{ user.email }}</span>
          </div>
          <div class="list-group-item px-0 py-3">
            <small class="text-muted d-block small-label">CPF</small>
            <span class="fw-semibold text-dark">{{ user.cpf }}</span>
          </div>
          <div class="list-group-item px-0 py-3">
            <div class="row">
              <div class="col-6">
                <small class="text-muted d-block small-label">Agência</small>
                <span class="fw-semibold text-dark">{{ user.agencia }}</span>
              </div>
              <div class="col-6">
                <small class="text-muted d-block small-label">Conta</small>
                <span class="fw-semibold text-dark">{{ user.conta }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-auto pt-5">
          <button @click="handleLogout" class="btn btn-outline-danger w-100 py-2 d-flex align-items-center justify-content-center gap-2 fw-bold shadow-sm">
            <i class="bi bi-box-arrow-right"></i> Sair da Conta
          </button>
        </div>
      </div>
    </div>

    <main class="container py-5 mt-5">
      <header class="mb-4 pt-4"> 
        <h2 class="display-6 fw-bold text-dark">Olá, {{ user.nome }}! 👋</h2>
        <p class="text-muted fs-6">Confira seu resumo financeiro</p>
      </header>

      <section class="card-saldo maze-gradient text-white p-4 mb-5 shadow-lg position-relative overflow-hidden">
        <div class="row align-items-center position-relative" style="z-index: 2;">
          <div class="col-md-8">
            <p class="small opacity-75 mb-1">Saldo disponível</p>
            <h2 class="fs-2 fw-bold d-flex align-items-center gap-3 mb-0">
              <span>{{ isSaldoVisible ? user.saldo : 'R$ ••••••••' }}</span>
              <i 
                :class="['bi cursor-pointer opacity-50 fs-4', isSaldoVisible ? 'bi-eye' : 'bi-eye-slash']" 
                @click="isSaldoVisible = !isSaldoVisible">
              </i>
            </h2>
          </div>
        </div>
        <i class="bi bi-wallet2 position-absolute end-0 top-50 translate-middle-y opacity-10" 
           style="font-size: 10rem; margin-right: -1rem;"></i>
      </section>

      <section class="row g-4">
        <div v-for="acao in acoes" :key="acao.nome" class="col-6 col-md-3">
          <div class="card h-100 border-0 shadow-sm py-4 text-center action-card" @click="executarAcao(acao)">
            <div :class="['icon-box mx-auto mb-3 shadow-sm', acao.colorClass]">
              <i :class="['bi', acao.icon]"></i>
            </div>
            <span class="fw-bold text-dark">{{ acao.nome }}</span>
          </div>
        </div>
      </section>

      <Pix ref="pixComponent" @abrirChaves="abrirGerenciarChaves" @abrirExtrato="abrirExtrato" @abrirTransferencia="abrirTransferencia" />
      <MinhasChaves ref="chavesComponent" />
      <Transferencia ref="transferenciaComponent" />
      <Extrato ref="extratoComponent" />
      <Saque ref="saqueComponent" />
      <Deposito ref="depositoComponent" />
    </main>
  </div>

  <Loading class="min-vh-100 bg-light" v-if="isloading"/>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted, nextTick } from 'vue';
import { Offcanvas } from 'bootstrap';
import { auth } from '../api/models/apis';

// Imports de Componentes
import Pix from '../components/views/Pix.vue';
import MinhasChaves from '../components/views/MinhasChaves.vue';
import Transferencia from '../components/views/Transferencia.vue';
import Extrato from '../components/views/Extrato.vue';
import Saque from '../components/views/Saque.vue';
import Deposito from '../components/views/Deposito.vue';
import Loading from '../components/loading.vue';

const router = useRouter();
const isloading = ref(true);
const user = ref({});
const isSaldoVisible = ref(false);

const sidebarRef = ref(null);
let bsOffcanvas = null;

const pixComponent = ref(null);
const chavesComponent = ref(null);
const transferenciaComponent = ref(null);
const extratoComponent = ref(null);
const saqueComponent = ref(null);
const depositoComponent = ref(null);

onMounted(async () => {
  await pegarUsuario();
  isloading.value = false;

  await nextTick();

  if (sidebarRef.value) {
    bsOffcanvas = new Offcanvas(sidebarRef.value);
  }
});

async function pegarUsuario() {
  try {
    const response = await auth.usuario();
    user.value = {
      nome: response.nome,
      sobrenome: response.sobrenome,
      avatar: `${response.nome.charAt(0)}${response.sobrenome.charAt(0)}`.toUpperCase(),
      email: response.email,
      cpf: response.cpf,
      agencia: response.detalhes_bancarios.agencia,
      conta: response.detalhes_bancarios.conta,
      saldo: response.detalhes_bancarios.saldo.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
      })
    };
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
  }
}

const toggleSidebar = () => {
  if (bsOffcanvas) bsOffcanvas.show();
};

const acoes = [
  { nome: 'Transferir', icon: 'bi-send', colorClass: 'bg-danger text-white' },
  { nome: 'Pix', icon: 'bi-qr-code-scan', colorClass: 'bg-danger text-white' },
  { nome: 'Extrato', icon: 'bi-clock-history', colorClass: 'bg-dark text-white' },
  { nome: 'Saque', icon: 'bi-cash-stack', colorClass: 'bg-dark text-white' },
  { nome: 'Depósito', icon: 'bi-box-arrow-in-down', colorClass: 'bg-dark text-white' }
];

const executarAcao = (acao) => {
  if (acao.nome === 'Pix') pixComponent.value?.abrirPix();
  if (acao.nome === 'Transferir') transferenciaComponent.value?.abrirTransferencia();
  if (acao.nome === 'Extrato') extratoComponent.value?.abrirExtrato();
  if (acao.nome === 'Saque') saqueComponent.value?.abrirSaque();
  if (acao.nome === 'Depósito') depositoComponent.value?.abrirDeposito();
};

const abrirTransferencia = () => transferenciaComponent.value?.abrirTransferencia();
const abrirExtrato = () => extratoComponent.value?.abrirExtrato();
const abrirGerenciarChaves = () => chavesComponent.value?.abrirChaves();

const handleLogout = async () => {
  if (bsOffcanvas) bsOffcanvas.hide();
  try {
    await auth.logout();
    router.push({ name: 'Login' });
  } catch (error) {
    console.log(error)
  }
};
</script>

<style scoped>
.avatar-circle {
  width: 45px;
  height: 45px;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  cursor: pointer;
}

.maze-gradient {
  background: linear-gradient(135deg, #dc3545 0%, #a71d2a 100%);
}

.action-card {
  transition: transform 0.2s;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-5px);
}

.icon-box {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
</style>