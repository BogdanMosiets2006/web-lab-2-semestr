<template>
  <div class="file-upload-wrapper">

    <!-- Зона загрузки -->
    <div
      class="drop-zone"
      :class="{ 'drop-zone--active': isDragging, 'drop-zone--error': hasError }"
      @dragenter.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @dragover.prevent
      @drop.prevent="onDrop"
    >
      <div class="drop-zone__icon">
        <i class="bi bi-file-earmark-excel"></i>
      </div>

      <p class="drop-zone__title">
        Перетащите Excel-файл сюда
      </p>
      <p class="drop-zone__subtitle">или</p>

      <label class="btn btn-primary" for="file-input">
        <i class="bi bi-upload me-2"></i>Выбрать файл
      </label>
      <input
        id="file-input"
        type="file"
        accept=".xlsx,.xls"
        class="d-none"
        @change="onFileSelected"
      />

      <p class="drop-zone__hint mt-3 text-muted">
        Поддерживаются файлы .xlsx и .xls (до 20 МБ)
      </p>
    </div>

    <!-- Прогресс загрузки -->
    <div v-if="isUploading" class="upload-progress mt-3">
      <div class="d-flex align-items-center gap-2 mb-1">
        <span class="text-muted small">Загружается: {{ fileName }}</span>
        <span class="ms-auto text-muted small">{{ uploadProgress }}%</span>
      </div>
      <div class="progress">
        <div
          class="progress-bar progress-bar-striped progress-bar-animated"
          :style="{ width: uploadProgress + '%' }"
        ></div>
      </div>
    </div>

    <!-- Успех -->
    <div v-if="successMessage" class="alert alert-success mt-3 d-flex align-items-center gap-2">
      <i class="bi bi-check-circle-fill"></i>
      {{ successMessage }}
    </div>

    <!-- Модальное окно ошибки -->
    <div
      v-if="showErrorModal"
      class="modal d-block"
      tabindex="-1"
      style="background: rgba(0,0,0,0.5)"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="bi bi-exclamation-triangle me-2"></i>Ошибка загрузки
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeErrorModal"></button>
          </div>
          <div class="modal-body">
            <p>{{ errorMessage }}</p>
            <hr />
            <p class="text-muted mb-0 small">
              <strong>Допустимые форматы:</strong> .xlsx, .xls (Microsoft Excel)<br />
              Убедитесь, что файл является корректным Excel-документом.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeErrorModal">
              Понятно
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FileUpload',

  emits: ['uploaded'],

  data() {
    return {
      isDragging:     false,
      isUploading:    false,
      uploadProgress: 0,
      fileName:       '',
      successMessage: '',
      showErrorModal: false,
      errorMessage:   '',
      hasError:       false,
    }
  },

  methods: {
    onDrop(event) {
      this.isDragging = false
      const file = event.dataTransfer.files[0]
      if (file) this.handleFile(file)
    },

    onFileSelected(event) {
      const file = event.target.files[0]
      if (file) this.handleFile(file)
      // Сбросить input, чтобы можно было загрузить тот же файл повторно
      event.target.value = ''
    },

    handleFile(file) {
      this.hasError       = false
      this.successMessage = ''

      // Проверка расширения
      const allowed = ['xlsx', 'xls']
      const ext     = file.name.split('.').pop().toLowerCase()

      if (!allowed.includes(ext)) {
        this.showError(
          `Файл "${file.name}" имеет недопустимый формат (.${ext}). ` +
          'Пожалуйста, выберите файл формата .xlsx или .xls.'
        )
        return
      }

      this.uploadFile(file)
    },

    async uploadFile(file) {
      this.isUploading    = true
      this.uploadProgress = 0
      this.fileName       = file.name

      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post('/api/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (e) => {
            this.uploadProgress = Math.round((e.loaded / e.total) * 100)
          },
        })

        this.successMessage = `Файл "${file.name}" успешно загружен и обработан!`
        this.$emit('uploaded', response.data)

      } catch (error) {
        const msg = error.response?.data?.errors?.file?.[0]
          || error.response?.data?.message
          || 'Произошла ошибка при загрузке файла.'
        this.showError(msg)
      } finally {
        this.isUploading = false
      }
    },

    showError(message) {
      this.errorMessage   = message
      this.showErrorModal = true
      this.hasError       = true
    },

    closeErrorModal() {
      this.showErrorModal = false
    },
  },
}
</script>

<style scoped>
.drop-zone {
  border: 2px dashed #adb5bd;
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  cursor: default;
  transition: border-color 0.2s, background-color 0.2s;
  background-color: #f8f9fa;
}
.drop-zone--active {
  border-color: #0d6efd;
  background-color: #e8f0fe;
}
.drop-zone--error {
  border-color: #dc3545;
  background-color: #fff5f5;
}
.drop-zone__icon {
  font-size: 3rem;
  color: #198754;
  margin-bottom: 12px;
}
.drop-zone__title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 4px;
}
.drop-zone__subtitle {
  color: #6c757d;
  margin-bottom: 12px;
}
.drop-zone__hint {
  font-size: 0.85rem;
}
</style>
