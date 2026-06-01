<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class WorkloadRecord extends Model
{
    protected $fillable = [
        'teacher_id', 'department_id', 'academic_year_id', 'discipline_id',
        'course', 'students_count', 'specialty_code', 'groups_count',
        'education_form', 'semester', 'financing',
        'lectures', 'practical', 'laboratory', 'module_control',
        'consultations_semester', 'consultations_before_exam',
        'credits', 'exams', 'course_works', 'vkr_bachelor',
        'diploma_master', 'practice_management', 'gek',
        'vkr_review', 'vkr_defense', 'phd_management', 'other',
        'total', 'notes',
    ];

    protected $casts = [
        'course' => 'integer',
        'students_count' => 'integer',
        'groups_count' => 'decimal:2',
        'semester' => 'integer',
        'lectures' => 'decimal:2',
        'practical' => 'decimal:2',
        'laboratory' => 'decimal:2',
        'module_control' => 'decimal:2',
        'consultations_semester' => 'decimal:2',
        'consultations_before_exam' => 'decimal:2',
        'credits' => 'decimal:2',
        'exams' => 'decimal:2',
        'course_works' => 'decimal:2',
        'vkr_bachelor' => 'decimal:2',
        'diploma_master' => 'decimal:2',
        'practice_management' => 'decimal:2',
        'gek' => 'decimal:2',
        'vkr_review' => 'decimal:2',
        'vkr_defense' => 'decimal:2',
        'phd_management' => 'decimal:2',
        'other' => 'decimal:2',
        'total' => 'decimal:2',
    ];

    public function teacher(): BelongsTo
    {
        return $this->belongsTo(Teacher::class);
    }

    public function department(): BelongsTo
    {
        return $this->belongsTo(Department::class);
    }

    public function academicYear(): BelongsTo
    {
        return $this->belongsTo(AcademicYear::class);
    }

    public function discipline(): BelongsTo
    {
        return $this->belongsTo(Discipline::class);
    }
}
