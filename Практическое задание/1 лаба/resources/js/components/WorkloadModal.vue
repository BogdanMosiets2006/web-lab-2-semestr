<template>
  <div class="modal d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">
            <i :class="isEdit ? 'bi bi-pencil-square' : 'bi bi-plus-circle'" class="me-2"></i>
            {{ isEdit ? labels.editTitle : labels.addTitle }}
          </h5>
          <button type="button" style="background:none;border:none;font-size:1.5rem;cursor:pointer;line-height:1;" @click="$emit('close')">&times;</button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submit" id="workload-form">

            <div class="form-row mb-3">
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.teacher }} <span class="text-danger">*</span></label>
                <select v-model="form.teacher_id" class="form-control" :class="err('teacher_id')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option v-for="t in dicts.teachers" :key="t.id" :value="t.id">{{ t.name }}</option>
                </select>
                <div class="invalid-feedback">{{ errors.teacher_id }}</div>
              </div>
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.department }} <span class="text-danger">*</span></label>
                <select v-model="form.department_id" class="form-control" :class="err('department_id')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option v-for="d in dicts.departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
                <div class="invalid-feedback">{{ errors.department_id }}</div>
              </div>
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.academicYear }} <span class="text-danger">*</span></label>
                <select v-model="form.academic_year_id" class="form-control" :class="err('academic_year_id')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option v-for="y in dicts.academicYears" :key="y.id" :value="y.id">{{ y.label }}</option>
                </select>
                <div class="invalid-feedback">{{ errors.academic_year_id }}</div>
              </div>
            </div>

            <div class="form-row mb-3">
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.discipline }} <span class="text-danger">*</span></label>
                <select v-model="form.discipline_id" class="form-control" :class="err('discipline_id')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option v-for="d in dicts.disciplines" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
                <div class="invalid-feedback">{{ errors.discipline_id }}</div>
              </div>
              <div class="col-md-2 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.course }}</label>
                <input v-model.number="form.course" type="number" min="1" max="6" class="form-control" placeholder="1-6" />
              </div>
              <div class="col-md-2 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.studentsCount }}</label>
                <input v-model.number="form.students_count" type="number" min="0" class="form-control" />
              </div>
              <div class="col-md-2 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.code }}</label>
                <input v-model="form.specialty_code" type="text" class="form-control" placeholder="09.03.01" maxlength="20" />
              </div>
              <div class="col-md-2 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.groupsCount }}</label>
                <input v-model.number="form.groups_count" type="number" min="0" step="0.5" class="form-control" />
              </div>
            </div>

            <div class="form-row mb-4">
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.educationForm }}</label>
                <select v-model="form.education_form" class="form-control">
                  <option value="">{{ labels.choose }}</option>
                  <option :value="labels.fullTime">{{ labels.fullTime }}</option>
                  <option :value="labels.partTime">{{ labels.partTime }}</option>
                </select>
              </div>
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.semester }} <span class="text-danger">*</span></label>
                <select v-model.number="form.semester" class="form-control" :class="err('semester')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option :value="1">{{ labels.sem1 }}</option>
                  <option :value="2">{{ labels.sem2 }}</option>
                </select>
                <div class="invalid-feedback">{{ errors.semester }}</div>
              </div>
              <div class="col-md-4 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.financing }} <span class="text-danger">*</span></label>
                <select v-model="form.financing" class="form-control" :class="err('financing')" required>
                  <option value="">{{ labels.choose }}</option>
                  <option :value="labels.budget">{{ labels.budget }}</option>
                  <option :value="labels.contract">{{ labels.contract }}</option>
                </select>
              </div>
            </div>

            <p class="font-weight-bold text-muted mb-2">
              <i class="bi bi-clock mr-1"></i>{{ labels.hoursTitle }}
            </p>
            <div class="form-row mb-3">
              <div v-for="field in hourFields" :key="field.key" class="col-6 col-md-3 mb-2">
                <label class="small mb-1">{{ field.label }}</label>
                <input
                  v-model.number="form[field.key]"
                  type="number" min="0" step="0.01"
                  class="form-control form-control-sm"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="col-md-3 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.total }}</label>
                <input v-model.number="form.total" type="number" min="0" step="0.01" class="form-control" />
              </div>
              <div class="col-md-9 mb-2">
                <label class="font-weight-bold mb-1">{{ labels.notes }}</label>
                <input v-model="form.notes" type="text" class="form-control" maxlength="500" />
              </div>
            </div>

          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            {{ labels.cancel }}
          </button>
          <button
            type="submit"
            form="workload-form"
            class="btn btn-primary"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm mr-2"></span>
            {{ isEdit ? labels.saveChanges : labels.addRecord }}
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const EMPTY_FORM = {
  teacher_id:                '',
  department_id:             '',
  academic_year_id:          '',
  discipline_id:             '',
  course:                    null,
  students_count:            null,
  specialty_code:            '',
  groups_count:              null,
  education_form:            '',
  semester:                  '',
  financing:                 '',
  lectures:                  0,
  practical:                 0,
  laboratory:                0,
  module_control:            0,
  consultations_semester:    0,
  consultations_before_exam: 0,
  credits:                   0,
  exams:                     0,
  course_works:              0,
  vkr_bachelor:              0,
  diploma_master:            0,
  practice_management:       0,
  gek:                       0,
  vkr_review:                0,
  vkr_defense:               0,
  phd_management:            0,
  other:                     0,
  total:                     0,
  notes:                     '',
}

export default {
  name: 'WorkloadModal',

  props: {
    record: {
      type:    Object,
      default: null,
    },
    dicts: {
      type:     Object,
      required: true,
    },
  },

  emits: ['close', 'saved'],

  data() {
    return {
      form:        { ...EMPTY_FORM },
      errors:      {},
      isSubmitting: false,
      labels: {
        editTitle: 'Редактировать запись',
        addTitle: 'Добавить запись',
        teacher: 'Преподаватель',
        department: 'Кафедра',
        academicYear: 'Учебный год',
        discipline: 'Дисциплина',
        course: 'Курс',
        studentsCount: 'Кол-во студ.',
        code: 'Шифр',
        groupsCount: 'Кол-во групп',
        educationForm: 'Форма обучения',
        fullTime: 'очная',
        partTime: 'заочная',
        semester: 'Семестр',
        sem1: 'I семестр',
        sem2: 'II семестр',
        financing: 'Финансирование',
        budget: 'бюджет',
        contract: 'контракт',
        choose: '— выберите —',
        hoursTitle: 'Часы по видам работ',
        total: 'ИТОГО',
        notes: 'Примечание',
        cancel: 'Отмена',
        saveChanges: 'Сохранить изменения',
        addRecord: 'Добавить запись',
      },
    }
  },

  computed: {
    isEdit() {
      return !!this.record
    },
    hourFields() {
      return [
        { key: 'lectures',                  label: 'Лекции' },
        { key: 'practical',                 label: 'Практические' },
        { key: 'laboratory',                label: 'Лабораторные' },
        { key: 'module_control',            label: 'Модульный контроль' },
        { key: 'consultations_semester',    label: 'Конс. (сем.)' },
        { key: 'consultations_before_exam', label: 'Конс. (перед экз.)' },
        { key: 'credits',                   label: 'Зачёты' },
        { key: 'exams',                     label: 'Экзамены' },
        { key: 'course_works',              label: 'Курсовые работы' },
        { key: 'vkr_bachelor',              label: 'ВКР бакалавр' },
        { key: 'diploma_master',            label: 'Дипломные/маг.' },
        { key: 'practice_management',       label: 'Рук-во практикой' },
        { key: 'gek',                       label: 'ГЭК' },
        { key: 'vkr_review',                label: 'Рецензирование ВКР' },
        { key: 'vkr_defense',               label: 'Защита ВКР' },
        { key: 'phd_management',            label: 'Рук-во аспир.' },
        { key: 'other',                     label: 'Другие виды' },
      ]
    },
  },

  mounted() {
    if (this.record) {
      this.form = {
        ...EMPTY_FORM,
        ...this.record,
        teacher_id:       this.record.teacher_id       ?? this.record.teacher?.id       ?? '',
        department_id:    this.record.department_id    ?? this.record.department?.id    ?? '',
        academic_year_id: this.record.academic_year_id ?? this.record.academicYear?.id  ?? '',
        discipline_id:    this.record.discipline_id    ?? this.record.discipline?.id    ?? '',
      }
    }
  },

  methods: {
    async submit() {
      this.errors      = {}
      this.isSubmitting = true

      const url    = this.isEdit ? `/api/workload/${this.record.id}` : '/api/workload'
      const method = this.isEdit ? 'put' : 'post'

      try {
        const { data } = await axios[method](url, this.form)
        this.$emit('saved', data)
      } catch (error) {
        if (error.response?.status === 422) {
          const serverErrors = error.response.data.errors ?? {}
          Object.keys(serverErrors).forEach(k => {
            this.errors[k] = serverErrors[k][0]
          })
        }
      } finally {
        this.isSubmitting = false
      }
    },

    err(field) {
      return this.errors[field] ? 'is-invalid' : ''
    },
  },
}
</script>

<style scoped>
.modal-body label {
  white-space: nowrap;
}
.form-row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -8px;
  margin-left: -8px;
}
.form-row > [class*="col-"] {
  padding-right: 8px;
  padding-left: 8px;
}
</style>
