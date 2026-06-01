<?php

namespace App\Imports;

use App\Models\AcademicYear;
use App\Models\Department;
use App\Models\Discipline;
use App\Models\Teacher;
use App\Models\WorkloadRecord;
use Illuminate\Support\Collection;
use Maatwebsite\Excel\Concerns\ToCollection;

class WorkloadImport implements ToCollection
{
    // индексы колонок в Excel файле
    private const COL_NUM = 0;
    private const COL_DISCIPLINE = 1;
    private const COL_COURSE = 2;
    private const COL_STUDENTS = 3;
    private const COL_SPECIALTY = 4;
    private const COL_GROUPS = 5;
    private const COL_EDU_FORM = 6;
    private const COL_LECTURES = 7;
    private const COL_PRACTICAL = 8;
    private const COL_LABORATORY = 9;
    private const COL_MODULE_CTRL = 10;
    private const COL_CONSULT_SEM = 11;
    private const COL_CONSULT_EXAM = 12;
    private const COL_CREDITS = 13;
    private const COL_EXAMS = 14;
    private const COL_COURSE_WORKS = 15;
    private const COL_VKR_BACHELOR = 16;
    private const COL_DIPLOMA_MASTER = 17;
    private const COL_PRACTICE_MGMT = 18;
    private const COL_GEK = 19;
    private const COL_VKR_REVIEW = 20;
    private const COL_VKR_DEFENSE = 21;
    private const COL_PHD = 22;
    private const COL_OTHER = 23;
    private const COL_TOTAL = 24;
    private const COL_NOTES = 25;

    public function collection(Collection $rows): void
    {
        $headerLine = $rows->get(1)?->filter()->first() ?? '';
        [$teacher, $department] = $this->parseHeader((string) $headerLine);

        $yearLine = $rows->get(2)?->filter()->first() ?? '';
        $academicYear = $this->parseAcademicYear((string) $yearLine);

        $currentSemester  = 1;
        $currentFinancing = "\xD0\xB1\xD1\x8E\xD0\xB4\xD0\xB6\xD0\xB5\xD1\x82";

        $semesterMarkers = [
            "i \xD1\x81\xD0\xB5\xD0\xBC\xD0\xB5\xD1\x81\xD1\x82\xD1\x80"  => 1,
            "ii \xD1\x81\xD0\xB5\xD0\xBC\xD0\xB5\xD1\x81\xD1\x82\xD1\x80" => 2,
        ];

        $financingMarkers = [
            "\xD0\xB1\xD1\x8E\xD0\xB4\xD0\xB6\xD0\xB5\xD1\x82"       => "\xD0\xB1\xD1\x8E\xD0\xB4\xD0\xB6\xD0\xB5\xD1\x82",
            "\xD0\xBA\xD0\xBE\xD0\xBD\xD1\x82\xD1\x80\xD0\xB0\xD0\xBA\xD1\x82" => "\xD0\xBA\xD0\xBE\xD0\xBD\xD1\x82\xD1\x80\xD0\xB0\xD0\xBA\xD1\x82",
        ];

        $skipKeywords = [
            "\xD0\xB8\xD1\x82\xD0\xBE\xD0\xB3\xD0\xBE",
            "\xD1\x83\xD1\x87\xD0\xB5\xD0\xB1\xD0\xBD\xD0\xB0\xD1\x8F \xD0\xBD\xD0\xB0\xD0\xB3\xD1\x80\xD1\x83\xD0\xB7\xD0\xBA\xD0\xB0",
            "\xD0\xB7\xD0\xB0\xD0\xB2\xD0\xB5\xD0\xB4\xD1\x83\xD1\x8E\xD1\x89\xD0\xB8\xD0\xB9",
            "\xD0\xBA\xD0\xB0\xD1\x80\xD1\x82\xD0\xBE\xD1\x87\xD0\xBA\xD0\xB0",
            "\xD0\xBA\xD0\xB0\xD1\x84\xD0\xB5\xD0\xB4\xD1\x80\xD0\xB0",
            "\xD0\xBD\xD0\xB0\xD0\xB3\xD1\x80\xD1\x83\xD0\xB7\xD0\xBA\xD0\xB0 \xD0\xBD\xD0\xB0",
            "\xe2\x84\x96 \xD0\xBF/\xD0\xBF",
        ];

        foreach ($rows as $index => $row) {
            if ($index < 3) continue;

            $firstCell = mb_strtolower(trim((string) ($row[0] ?? '')));
            $secondCell = mb_strtolower(trim((string) ($row[1] ?? '')));
            $combined = $firstCell . ' ' . $secondCell;

            foreach ($semesterMarkers as $marker => $num) {
                if (str_contains($combined, $marker)) {
                    $currentSemester = $num;
                }
            }

            foreach ($financingMarkers as $marker => $type) {
                if (str_contains($combined, $marker)) {
                    $currentFinancing = $type;
                }
            }

            $shouldSkip = false;
            $rowText = mb_strtolower(collect($row)->map(fn ($v) => (string) $v)->implode(' '));
            foreach ($skipKeywords as $kw) {
                if (str_contains($rowText, $kw)) {
                    $shouldSkip = true;
                    break;
                }
            }
            if ($shouldSkip) continue;

            if (! is_numeric($row[self::COL_NUM] ?? '') || (int) ($row[self::COL_NUM] ?? 0) === 0) {
                continue;
            }

            $disciplineName = trim((string) ($row[self::COL_DISCIPLINE] ?? ''));
            if (empty($disciplineName)) continue;

            $discipline = Discipline::firstOrCreate(['name' => $disciplineName]);

            WorkloadRecord::create([
                'teacher_id' => $teacher->id,
                'department_id' => $department->id,
                'academic_year_id' => $academicYear->id,
                'discipline_id' => $discipline->id,
                'course' => (int) ($row[self::COL_COURSE] ?? 0) ?: null,
                'students_count' => (int) ($row[self::COL_STUDENTS] ?? 0) ?: null,
                'specialty_code' => trim((string) ($row[self::COL_SPECIALTY] ?? '')) ?: null,
                'groups_count' => $this->decimal($row[self::COL_GROUPS] ?? null),
                'education_form' => trim((string) ($row[self::COL_EDU_FORM] ?? '')) ?: null,
                'semester' => $currentSemester,
                'financing' => $currentFinancing,
                'lectures' => $this->decimal($row[self::COL_LECTURES] ?? null),
                'practical' => $this->decimal($row[self::COL_PRACTICAL] ?? null),
                'laboratory' => $this->decimal($row[self::COL_LABORATORY] ?? null),
                'module_control' => $this->decimal($row[self::COL_MODULE_CTRL] ?? null),
                'consultations_semester' => $this->decimal($row[self::COL_CONSULT_SEM] ?? null),
                'consultations_before_exam' => $this->decimal($row[self::COL_CONSULT_EXAM] ?? null),
                'credits' => $this->decimal($row[self::COL_CREDITS] ?? null),
                'exams' => $this->decimal($row[self::COL_EXAMS] ?? null),
                'course_works' => $this->decimal($row[self::COL_COURSE_WORKS] ?? null),
                'vkr_bachelor' => $this->decimal($row[self::COL_VKR_BACHELOR] ?? null),
                'diploma_master' => $this->decimal($row[self::COL_DIPLOMA_MASTER] ?? null),
                'practice_management' => $this->decimal($row[self::COL_PRACTICE_MGMT] ?? null),
                'gek' => $this->decimal($row[self::COL_GEK] ?? null),
                'vkr_review' => $this->decimal($row[self::COL_VKR_REVIEW] ?? null),
                'vkr_defense' => $this->decimal($row[self::COL_VKR_DEFENSE] ?? null),
                'phd_management' => $this->decimal($row[self::COL_PHD] ?? null),
                'other' => $this->decimal($row[self::COL_OTHER] ?? null),
                'total' => $this->decimal($row[self::COL_TOTAL] ?? null),
                'notes' => trim((string) ($row[self::COL_NOTES] ?? '')) ?: null,
            ]);
        }
    }

    private function parseHeader(string $line): array
    {
        $parts = array_map('trim', explode(',', $line));
        $departmentName = $parts[0] ?? 'Unknown';
        $teacherName    = $parts[1] ?? 'Unknown';
        $position       = $parts[2] ?? null;

        $department = Department::firstOrCreate(['name' => $departmentName]);
        $teacher    = Teacher::firstOrCreate(
            ['name' => $teacherName],
            ['position' => $position]
        );

        return [$teacher, $department];
    }

    private function parseAcademicYear(string $line): AcademicYear
    {
        preg_match('/(\d{4}\/\d{4})/', $line, $matches);
        $label = $matches[1] ?? date('Y') . '/' . (date('Y') + 1);
        return AcademicYear::firstOrCreate(['label' => $label]);
    }

    private function decimal(mixed $value): float
    {
        if (is_null($value) || $value === '') {
            return 0;
        }
        return round((float) str_replace(',', '.', (string) $value), 2);
    }
}
