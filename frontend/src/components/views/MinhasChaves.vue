<template>
  <div class="offcanvas offcanvas-bottom border-0" tabindex="-1" id="offcanvasChaves">
    <div class="offcanvas-header border-bottom py-3">
      <h5 class="offcanvas-title fw-bold text-dark">
        <i class="bi bi-key text-danger me-2"></i>Minhas Chaves
      </h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>

    <div class="offcanvas-body bg-light">
      <div class="mb-4">
        <button class="btn btn-danger w-100 py-3 fw-bold d-flex align-items-center justify-content-center gap-2 rounded-4 shadow-sm" 
                data-bs-toggle="modal" data-bs-target="#modalNovaChave">
          <i class="bi bi-plus-lg"></i> Cadastrar Nova Chave
        </button>
      </div>

      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="list-group list-group-flush">
          <div v-for="(chave, index) in chaves" :key="index" class="list-group-item py-3 border-bottom last-item-border">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <small class="text-muted d-block small-label text-uppercase">{{ chave.tipo }}</small>
                <span class="fw-bold text-dark">{{ chave.valor }}</span>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-light btn-sm rounded-circle shadow-sm" @click="copiarChave(chave.valor)" title="Copiar">
                  <i class="bi bi-copy text-primary"></i>
                </button>
                <button class="btn btn-light btn-sm rounded-circle shadow-sm" @click="prepararExclusao(index)" title="Excluir">
                  <i class="bi bi-trash text-danger"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="modalNovaChave" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 rounded-4 shadow">
        <div class="modal-header border-0 pb-0">
          <h5 class="fw-bold">Nova Chave Pix</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" id="closeModalCadastro"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label small fw-bold text-muted">Tipo de Chave</label>
            <select class="form-select border-0 bg-light p-3 rounded-3" v-model="novaChave.tipo" @change="novaChave.valor = ''">
              <option value="CPF">CPF</option>
              <option value="E-mail">E-mail</option>
              <option value="Celular">Celular</option>
              <option value="Aleatória">Chave Aleatória</option>
            </select>
          </div>
          
          <div class="mb-3">
            <label class="form-label small fw-bold text-muted">Valor da Chave</label>
            
            <input 
              v-if="novaChave.tipo === 'CPF' || novaChave.tipo === 'Celular'"
              type="text" 
              class="form-control border-0 bg-light p-3 rounded-3" 
              v-model="novaChave.valor" 
              v-mask="maskSelector"
              :placeholder="placeholderSelector"
            >

            <input 
              v-else-if="novaChave.tipo === 'E-mail'"
              type="text" 
              class="form-control border-0 bg-light p-3 rounded-3" 
              v-model="novaChave.valor" 
              :placeholder="placeholderSelector"
            >

            <input 
              v-else
              type="text" 
              class="form-control border-0 bg-secondary bg-opacity-10 p-3 rounded-3" 
              value="Gerada automaticamente pelo sistema" 
              disabled
              style="cursor: not-allowed;"
            >
          </div>
        </div>
        <div class="modal-footer border-0 pt-0">
          <button type="button" class="btn btn-light p-3 flex-grow-1 fw-bold" data-bs-dismiss="modal">Cancelar</button>
          <button type="button" class="btn btn-danger p-3 flex-grow-1 fw-bold" @click="salvarChave">Salvar</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="modalConfirmarExclusao" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
      <div class="modal-content border-0 rounded-4 shadow">
        <div class="modal-body text-center py-4">
          <div class="text-warning mb-3">
            <i class="bi bi-exclamation-triangle-fill" style="font-size: 3rem;"></i>
          </div>
          <h5 class="fw-bold">Excluir Chave?</h5>
          <p class="text-muted small">Essa ação removerá a chave permanentemente da sua conta Maze Bank.</p>
          <div class="d-flex gap-2 mt-4">
            <button class="btn btn-light w-100 fw-bold" data-bs-dismiss="modal">Não</button>
            <button class="btn btn-danger w-100 fw-bold" @click="confirmarExclusao">Sim, Excluir</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Offcanvas, Modal } from 'bootstrap';

// ESTADOS REATIVOS
const chaves = ref([
  { tipo: 'CPF', valor: '123.456.789-00' },
  { tipo: 'E-mail', valor: 'michael.ds@maze.com' },
  { tipo: 'Celular', valor: '(11) 98765-4321' }
]);

const novaChave = ref({ tipo: 'CPF', valor: '' });
const indexParaExcluir = ref(null);

// REFERÊNCIAS DO BOOTSTRAP
let chavesOffcanvas = null;
let modalExcluirBS = null;

// LÓGICA DE MÁSCARAS E PLACEHOLDERS
const maskSelector = computed(() => {
  if (novaChave.value.tipo === 'CPF') return '###.###.###-##';
  if (novaChave.value.tipo === 'Celular') return '(##) #####-####';
  return '';
});

const placeholderSelector = computed(() => {
  const map = {
    'CPF': '000.000.000-00',
    'Celular': '(00) 00000-0000',
    'E-mail': 'exemplo@maze.com',
    'Aleatória': 'Gerada pelo sistema'
  };
  return map[novaChave.value.tipo];
});

// INICIALIZAÇÃO DOS COMPONENTES JS
onMounted(() => {
  const elOffcanvas = document.getElementById('offcanvasChaves');
  if (elOffcanvas) chavesOffcanvas = new Offcanvas(elOffcanvas);

  const elModalExcluir = document.getElementById('modalConfirmarExclusao');
  if (elModalExcluir) modalExcluirBS = new Modal(elModalExcluir);
});

// FUNÇÕES DE AÇÃO
const abrirChaves = () => chavesOffcanvas?.show();

const copiarChave = (valor) => {
  navigator.clipboard.writeText(valor);
  alert('Chave copiada com sucesso!');
};

const salvarChave = () => {
  // Lógica para chave Aleatória
  if (novaChave.value.tipo === 'Aleatória') {
    const hash = Math.random().toString(36).substring(2, 10).toUpperCase();
    novaChave.value.valor = `MAZE-${hash}`;
  }

  if (novaChave.value.valor) {
    chaves.value.push({ ...novaChave.value });
    
    // Reset e Fechamento
    novaChave.value.valor = '';
    novaChave.value.tipo = 'CPF';
    document.getElementById('closeModalCadastro').click();
  } else {
    alert('Por favor, preencha o valor da chave.');
  }
};

// CONTROLE DE EXCLUSÃO
const prepararExclusao = (index) => {
  indexParaExcluir.value = index;
  modalExcluirBS.show();
};

const confirmarExclusao = () => {
  if (indexParaExcluir.value !== null) {
    chaves.value.splice(indexParaExcluir.value, 1);
    indexParaExcluir.value = null;
    modalExcluirBS.hide();
  }
};

// EXPOSIÇÃO PARA O PAI (HOME)
defineExpose({ abrirChaves });
</script>

<style scoped>
#offcanvasChaves {
  height: calc(100vh - 72px) !important;
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;
  transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.small-label {
  font-size: 0.65rem;
  letter-spacing: 1px;
  font-weight: 800;
}

.last-item-border:last-child {
  border-bottom: none !important;
}

.form-control:focus, .form-select:focus {
  background-color: hsl(var(--card)) !important;
  border-color: hsl(var(--primary)) !important;
  box-shadow: none;
}

.btn-light {
  background-color: hsl(var(--card)) !important;
  border: none;
}

.btn-light:hover {
  background-color: #e2e6ea;
}
</style>