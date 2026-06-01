<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('workload_records', function (Blueprint $table) {
            $table->id();

            // Связи
            $table->foreignId('teacher_id')->constrained()->cascadeOnDelete();
            $table->foreignId('department_id')->constrained()->cascadeOnDelete();
            $table->foreignId('academic_year_id')->constrained()->cascadeOnDelete();
            $table->foreignId('discipline_id')->constrained()->cascadeOnDelete();

            // Основные поля записи
            $table->unsignedTinyInteger('course')->nullable();
            $table->unsignedSmallInteger('students_count')->nullable();
            $table->string('specialty_code', 20)->nullable(); // 09.03.01
            $table->decimal('groups_count', 5, 2)->nullable();
            $table->string('education_form', 20)->nullable(); // очная / заочная
            $table->unsignedTinyInteger('semester');          // 1 или 2
            $table->string('financing', 20)->default('бюджет'); // бюджет / контракт

            // Часы по видам работ
            $table->decimal('lectures', 8, 2)->default(0);
            $table->decimal('practical', 8, 2)->default(0);
            $table->decimal('laboratory', 8, 2)->default(0);
            $table->decimal('module_control', 8, 2)->default(0);
            $table->decimal('consultations_semester', 8, 2)->default(0);
            $table->decimal('consultations_before_exam', 8, 2)->default(0);
            $table->decimal('credits', 8, 2)->default(0);
            $table->decimal('exams', 8, 2)->default(0);
            $table->decimal('course_works', 8, 2)->default(0);
            $table->decimal('vkr_bachelor', 8, 2)->default(0);
            $table->decimal('diploma_master', 8, 2)->default(0);
            $table->decimal('practice_management', 8, 2)->default(0);
            $table->decimal('gek', 8, 2)->default(0);
            $table->decimal('vkr_review', 8, 2)->default(0);
            $table->decimal('vkr_defense', 8, 2)->default(0);
            $table->decimal('phd_management', 8, 2)->default(0);
            $table->decimal('other', 8, 2)->default(0);
            $table->decimal('total', 8, 2)->default(0);

            $table->text('notes')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('workload_records');
    }
};
