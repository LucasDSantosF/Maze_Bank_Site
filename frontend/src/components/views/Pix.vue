<template>
    <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasPix">
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
                    <div class="avatar-sm bg-secondary bg-opacity-10 text-secondary rounded-circle d-flex align-items-center justify-content-center">
                    <i class="bi bi-person"></i>
                    </div>
                    <div>
                    <p class="m-0 fw-bold small text-dark">{{ t.nome }}</p>
                    <p class="m-0 text-muted small" style="font-size: 0.7rem;">{{ t.data }}</p>
                    </div>
                </div>
                <span class="fw-bold text-dark small">- R$ {{ t.valor.toFixed(2) }}</span>
                </div>
            </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Offcanvas } from 'bootstrap';

let pixOffcanvas = null;

const minhasChaves = ref([
  { tipo: 'CPF', chave: '123.***.***-00' },
  { tipo: 'E-mail', chave: 'michael.ds@maze.com' },
  { tipo: 'Celular', chave: '(11) 9****-1234' }
]);

const ultimasTransferencias = ref([
  { nome: 'Franklin Clinton', valor: 500.00, data: 'Hoje' },
  { nome: 'Lamar Davis', valor: 150.00, data: 'Ontem' },
  { nome: 'Trevor Philips', valor: 2500.00, data: '15 Jan' }
]);

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

onMounted(() => {
  const el = document.getElementById('offcanvasPix');
  if (el) pixOffcanvas = new Offcanvas(el);
});

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