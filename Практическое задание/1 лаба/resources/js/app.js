import './bootstrap';
import { createApp } from 'vue';
import FileUpload from './components/FileUpload.vue';
import WorkloadTable from './components/WorkloadTable.vue';

const fileUploadEl = document.getElementById('vue-file-upload');
if (fileUploadEl) {
    const app = createApp(FileUpload);
    const vm = app.mount(fileUploadEl);
    vm.$watch('successMessage', (val) => {
        if (val) {
            window.dispatchEvent(new Event('workload-updated'));
        }
    });
}

const workloadEl = document.getElementById('vue-workload-table');
if (workloadEl) {
    const isAuth = workloadEl.dataset.isAuth === 'true';
    const app = createApp(WorkloadTable, { isAuth });
    const vm = app.mount(workloadEl);
    window.addEventListener('workload-updated', () => {
        vm.loadData(1);
    });
}
