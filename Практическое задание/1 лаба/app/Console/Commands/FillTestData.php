<?php

namespace App\Console\Commands;

use App\Models\AcademicYear;
use App\Models\Department;
use App\Models\Discipline;
use App\Models\Teacher;
use App\Models\WorkloadRecord;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class FillTestData extends Command
{
    /**
     * Запуск:
     *   php artisan workload:fill          # заполняет 20 записей (по умолчанию)
     *   php artisan workload:fill --count=50
     *   php artisan workload:fill --count=100 --fresh   # очищает таблицы перед заполнением
     */
    protected $signature = 'workload:fill
                            {--count=20 : Количество записей нагрузки для создания}
                            {--fresh    : Очистить таблицы перед заполнением}';

    protected $description = 'Заполнить базу данных тестовыми данными учебной нагрузки';

    // ── Справочники ──────────────────────────────────────────────────────────

    private array $teacherNames = [
        'Гукай Алексей Евгеньевич',
        'Иванов Иван Иванович',
        'Петрова Мария Сергеевна',
        'Сидоров Константин Николаевич',
        'Козлова Елена Владимировна',
    ];

    private array $positions = [
        'ст.преподаватель', 'доцент', 'профессор', 'ассистент', 'зав.кафедрой',
    ];

    private array $departmentNames = [
        'Кафедра компьютерных технологий',
        'Кафедра прикладной математики',
        'Кафедра информационных систем',
    ];

    private array $disciplineNames = [
        'Web-программирование',
        'ООП',
        'Программирование мобильных устройств',
        'Базы данных',
        'Методы и средства расширенной реальности',
        'Технологии виртуальной и дополнительной реальности',
        'Программирование',
        'Операционные системы',
        'Компьютерные сети',
        'Алгоритмы и структуры данных',
    ];

    private array $specialtyCodes = ['09.03.01', '09.04.01', '09.03.02'];

    private array $educationForms = ['очная', 'заочная'];

    private array $financingTypes = ['бюджет', 'контракт'];

    // ─────────────────────────────────────────────────────────────────────────

    public function handle(): int
    {
        $count = (int) $this->option('count');

        if ($count <= 0) {
            $this->error('Параметр --count должен быть больше нуля.');
            return self::FAILURE;
        }

        if ($this->option('fresh')) {
            $this->warn('Очистка таблиц...');
            DB::statement('SET FOREIGN_KEY_CHECKS=0');
            WorkloadRecord::truncate();
            Teacher::truncate();
            Department::truncate();
            Discipline::truncate();
            AcademicYear::truncate();
            DB::statement('SET FOREIGN_KEY_CHECKS=1');
            $this->line('  Таблицы очищены.');
        }

        $this->info("Заполнение базы данных ({$count} записей нагрузки)...");

        // 1. Справочные таблицы
        $this->line('  Создание справочников...');
        $teachers      = $this->seedTeachers();
        $departments   = $this->seedDepartments();
        $disciplines   = $this->seedDisciplines();
        $academicYears = $this->seedAcademicYears();

        // 2. Записи нагрузки
        $this->line("  Создание {$count} записей нагрузки...");
        $bar = $this->output->createProgressBar($count);
        $bar->start();

        for ($i = 0; $i < $count; $i++) {
            WorkloadRecord::create($this->randomWorkloadRecord(
                $teachers, $departments, $disciplines, $academicYears
            ));
            $bar->advance();
        }

        $bar->finish();
        $this->newLine();

        $this->info('✓ Готово!');
        $this->table(
            ['Таблица', 'Записей'],
            [
                ['teachers',         Teacher::count()],
                ['departments',      Department::count()],
                ['disciplines',      Discipline::count()],
                ['academic_years',   AcademicYear::count()],
                ['workload_records', WorkloadRecord::count()],
            ]
        );

        return self::SUCCESS;
    }

    // ── Вспомогательные методы ───────────────────────────────────────────────

    /** @return \Illuminate\Support\Collection<Teacher> */
    private function seedTeachers()
    {
        return collect($this->teacherNames)->map(fn ($n, $i) =>
            Teacher::firstOrCreate(['name' => $n], ['position' => $this->positions[$i % count($this->positions)]])
        );
    }

    /** @return \Illuminate\Support\Collection<Department> */
    private function seedDepartments()
    {
        return collect($this->departmentNames)->map(fn ($n) =>
            Department::firstOrCreate(['name' => $n])
        );
    }

    /** @return \Illuminate\Support\Collection<Discipline> */
    private function seedDisciplines()
    {
        return collect($this->disciplineNames)->map(fn ($n) =>
            Discipline::firstOrCreate(['name' => $n])
        );
    }

    /** @return \Illuminate\Support\Collection<AcademicYear> */
    private function seedAcademicYears()
    {
        $years = ['2023/2024', '2024/2025', '2025/2026'];
        return collect($years)->map(fn ($y) =>
            AcademicYear::firstOrCreate(['label' => $y])
        );
    }

    private function randomWorkloadRecord($teachers, $departments, $disciplines, $academicYears): array
    {
        $lectures    = $this->rnd(0, 40);
        $practical   = $this->rnd(0, 20);
        $laboratory  = $this->rnd(0, 100);
        $consultSem  = round($this->rnd(0, 10), 2);
        $consultExam = round($this->rnd(0, 5), 2);
        $exams       = $this->rnd(0, 20);
        $credits     = $this->rnd(0, 15);
        $courseWorks = $this->rnd(0, 20);
        $other       = round($this->rnd(0, 5), 2);

        $total = $lectures + $practical + $laboratory + $consultSem
               + $consultExam + $exams + $credits + $courseWorks + $other;

        return [
            'teacher_id' => $teachers->random()->id,
            'department_id' => $departments->random()->id,
            'academic_year_id' => $academicYears->random()->id,
            'discipline_id' => $disciplines->random()->id,
            'course' => rand(1, 5),
            'students_count' => rand(5, 80),
            'specialty_code' => $this->specialtyCodes[array_rand($this->specialtyCodes)],
            'groups_count' => round(rand(1, 4) * 0.5, 1),
            'education_form' => $this->educationForms[array_rand($this->educationForms)],
            'semester' => rand(1, 2),
            'financing' => $this->financingTypes[array_rand($this->financingTypes)],
            'lectures' => $lectures,
            'practical' => $practical,
            'laboratory' => $laboratory,
            'module_control' => 0,
            'consultations_semester' => $consultSem,
            'consultations_before_exam' => $consultExam,
            'credits' => $credits,
            'exams' => $exams,
            'course_works' => $courseWorks,
            'vkr_bachelor' => 0,
            'diploma_master' => 0,
            'practice_management' => 0,
            'gek' => 0,
            'vkr_review' => 0,
            'vkr_defense' => 0,
            'phd_management' => 0,
            'other' => $other,
            'total' => round($total, 2),
        ];
    }

    /** Случайное decimal значение (0 или реальное число с вероятностью 70%) */
    private function rnd(float $min, float $max): float
    {
        if (rand(0, 9) < 3) {
            return 0; // 30% вероятность нулевого значения
        }
        return round($min + mt_rand() / mt_getrandmax() * ($max - $min), 2);
    }
}
