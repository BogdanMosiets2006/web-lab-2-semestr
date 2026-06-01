<template>
  <div class="workload-table">

    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h4 class="mb-0 me-auto">{{ labels.title }}</h4>

      <select v-model="filters.semester" class="form-select form-select-sm w-auto" @change="loadData(1)">
        <option value="">{{ labels.allSemesters }}</option>
        <option value="1">{{ labels.sem1 }}</option>
        <option value="2">{{ labels.sem2 }}</option>
      </select>
      <select v-model="filters.financing" class="form-select form-select-sm w-auto" @change="loadData(1)">
        <option value="">{{ labels.allFinancing }}</option>
        <option :value="labels.budget">{{ labels.budgetCap }}</option>
        <option :value="labels.contract">{{ labels.contractCap }}</option>
      </select>

      <button class="btn btn-success btn-sm" @click="openCreate" v-if="isAuth">
        <i class="bi bi-plus-lg me-1"></i>{{ labels.add }}
      </button>
      <button class="btn btn-outline-danger btn-sm" @click="showClearConfirm = true" v-if="isAuth && total > 0">
        <i class="bi bi-x-circle me-1"></i>{{ labels.clearAll }}
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-bordered table-hover table-sm align-middle">
        <thead class="table-dark">
          <tr>
            <th>#</th>
            <th>{{ labels.discipline }}</th>
            <th>{{ labels.teacher }}</th>
            <th>{{ labels.course }}</th>
            <th>{{ labels.form }}</th>
            <th>{{ labels.semShort }}</th>
            <th>{{ labels.financingShort }}</th>
            <th>{{ labels.lectures }}</th>
            <th>{{ labels.lab }}</th>
            <th>{{ labels.practical }}</th>
            <th>{{ labels.total }}</th>
            <th v-if="isAuth">{{ labels.actions }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="isAuth ? 12 : 11" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
            </td>
          </tr>
          <tr v-else-if="records.length === 0">
            <td :colspan="isAuth ? 12 : 11" class="text-center text-muted py-4">
              {{ labels.noData }}
            </td>
          </tr>
          <tr v-for="(rec, idx) in records" :key="rec.id">
            <td class="text-muted small">{{ (currentPage - 1) * perPage + idx + 1 }}</td>
            <td>{{ rec.discipline?.name ?? '—' }}</td>
            <td class="text-nowrap">{{ rec.teacher?.name ?? '—' }}</td>
            <td class="text-center">{{ rec.course ?? '—' }}</td>
            <td>{{ rec.education_form ?? '—' }}</td>
            <td class="text-center">{{ rec.semester }}</td>
            <td>
              <span :class="rec.financing === labels.budget ? 'badge bg-primary' : 'badge bg-warning text-dark'">
                {{ rec.financing }}
              </span>
            </td>
            <td class="text-end">{{ rec.lectures }}</td>
            <td class="text-end">{{ rec.laboratory }}</td>
            <td class="text-end">{{ rec.practical }}</td>
            <td class="text-end fw-bold">{{ rec.total }}</td>
            <td v-if="isAuth" class="text-nowrap">
              <button class="btn btn-outline-primary btn-sm me-1" @click="openEdit(rec)">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-outline-danger btn-sm" @click="confirmDelete(rec)">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="d-flex flex-wrap align-items-center gap-3 mt-3" v-if="total > perPage">
      <nav>
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="loadData(currentPage - 1)">&lsaquo;</button>
          </li>
          <li v-for="p in visiblePages" :key="p" class="page-item" :class="{ active: p === currentPage }">
            <button class="page-link" @click="loadData(p)">{{ p }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === lastPage }">
            <button class="page-link" @click="loadData(currentPage + 1)">&rsaquo;</button>
          </li>
        </ul>
      </nav>

      <button class="btn btn-outline-secondary btn-sm ms-auto" @click="lazyLoad" :disabled="lazyLoading || allLoaded">
        <span v-if="lazyLoading" class="spinner-border spinner-border-sm me-1"></span>
        <i v-else class="bi bi-arrow-down-circle me-1"></i>
        {{ allLoaded ? labels.allLoaded : labels.loadMore }}
      </button>

      <span class="text-muted small">
        {{ labels.shown }} {{ records.length }} {{ labels.of }} {{ total }}
      </span>
    </div>

    <WorkloadModal
      v-if="showModal"
      :record="editingRecord"
      :dicts="dicts"
      @close="showModal = false"
      @saved="onSaved"
    />

    <!-- Delete confirm -->
    <div v-if="deletingRecord" class="modal d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">{{ labels.deleteTitle }}</h5>
            <button type="button" style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:white;" @click="deletingRecord = null">&times;</button>
          </div>
          <div class="modal-body">
            {{ labels.deleteConfirm }}
            <strong>{{ deletingRecord.discipline?.name }}</strong>?
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="deletingRecord = null">{{ labels.cancel }}</button>
            <button class="btn btn-danger" @click="deleteRecord" :disabled="deleteLoading">
              <span v-if="deleteLoading" class="spinner-border spinner-border-sm me-1"></span>
              {{ labels.delete }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Clear all confirm -->
    <div v-if="showClearConfirm" class="modal d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">{{ labels.clearAllTitle }}</h5>
            <button type="button" style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:white;" @click="showClearConfirm = false">&times;</button>
          </div>
          <div class="modal-body">
            {{ labels.clearAllConfirm }} <strong>{{ total }}</strong> {{ labels.clearAllRecords }}
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showClearConfirm = false">{{ labels.cancel }}</button>
            <button class="btn btn-danger" @click="clearAll" :disabled="clearLoading">
              <span v-if="clearLoading" class="spinner-border spinner-border-sm me-1"></span>
              {{ labels.clearAll }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import WorkloadModal from './WorkloadModal.vue'

export default {
  name: 'WorkloadTable',
  components: { WorkloadModal },

  props: {
    isAuth: { type: Boolean, default: false },
  },

  data() {
    return {
      records: [], total: 0, currentPage: 1, lastPage: 1, perPage: 10,
      loading: false, lazyLoading: false, lazyPage: 1,
      filters: { semester: '', financing: '' },
      showModal: false, editingRecord: null,
      deletingRecord: null, deleteLoading: false,
      showClearConfirm: false, clearLoading: false,
      dicts: { teachers: [], departments: [], disciplines: [], academicYears: [] },
      labels: {
        title: 'Учебная нагрузка',
        allSemesters: 'Все семестры',
        sem1: 'I семестр',
        sem2: 'II семестр',
        allFinancing: 'Все (бюджет/контракт)',
        budget: 'бюджет',
        contract: 'контракт',
        budgetCap: 'Бюджет',
        contractCap: 'Контракт',
        add: '+Добавить',
        clearAll: 'Очистить всё',
        discipline: 'Дисциплина',
        teacher: 'Преподаватель',
        course: 'Курс',
        form: 'Форма',
        semShort: 'Сем.',
        financingShort: 'Финансиров.',
        lectures: 'Лекции',
        lab: 'Лаб.',
        practical: 'Практ.',
        total: 'ИТОГО',
        actions: 'Действия',
        noData: 'Нет данных',
        allLoaded: 'Все данные загружены',
        loadMore: 'Загрузить ещё',
        shown: 'Показано',
        of: 'из',
        deleteTitle: 'Удалить запись?',
        deleteConfirm: 'Удалить запись по дисциплине',
        cancel: 'Отмена',
        delete: 'Удалить',
        clearAllTitle: 'Очистить все записи?',
        clearAllConfirm: 'Вы уверены? Будет удалено',
        clearAllRecords: 'записей.',
      },
    }
  },

  computed: {
    allLoaded() { return this.lazyPage >= this.lastPage },
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end   = Math.min(this.lastPage, this.currentPage + 2)
      for (let p = start; p <= end; p++) pages.push(p)
      return pages
    },
  },

  mounted() {
    this.loadData(1)
    if (this.isAuth) this.loadDicts()
  },

  methods: {
    async loadData(page) {
      this.loading = true
      this.currentPage = page
      this.lazyPage = page
      try {
        const { data } = await axios.get('/api/workload', {
          params: { page, per_page: this.perPage, ...this.filters },
        })
        this.records = data.data
        this.total = data.total
        this.lastPage = data.last_page
      } finally { this.loading = false }
    },

    async lazyLoad() {
      if (this.allLoaded || this.lazyLoading) return
      this.lazyLoading = true
      const nextPage = this.lazyPage + 1
      try {
        const { data } = await axios.get('/api/workload', {
          params: { page: nextPage, per_page: this.perPage, ...this.filters },
        })
        this.records = [...this.records, ...data.data]
        this.lazyPage = nextPage
        this.total = data.total
        this.lastPage = data.last_page
      } finally { this.lazyLoading = false }
    },

    async loadDicts() {
      const [t, dep, dis, ay] = await Promise.all([
        axios.get('/api/dict/teachers'),
        axios.get('/api/dict/departments'),
        axios.get('/api/dict/disciplines'),
        axios.get('/api/dict/academic-years'),
      ])
      this.dicts.teachers = t.data
      this.dicts.departments = dep.data
      this.dicts.disciplines = dis.data
      this.dicts.academicYears = ay.data
    },

    openCreate() { this.editingRecord = null; this.showModal = true },
    openEdit(record) { this.editingRecord = record; this.showModal = true },
    onSaved() { this.showModal = false; this.loadData(this.currentPage) },
    confirmDelete(record) { this.deletingRecord = record },

    async deleteRecord() {
      this.deleteLoading = true
      try {
        await axios.delete(`/api/workload/${this.deletingRecord.id}`)
        this.deletingRecord = null
        this.loadData(this.currentPage)
      } finally { this.deleteLoading = false }
    },

    async clearAll() {
      this.clearLoading = true
      try {
        await axios.delete('/api/workload-all')
        this.showClearConfirm = false
        this.loadData(1)
      } finally { this.clearLoading = false }
    },
  },
}
</script>
