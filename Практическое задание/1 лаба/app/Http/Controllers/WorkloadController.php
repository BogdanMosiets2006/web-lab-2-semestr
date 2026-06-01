<?php

namespace App\Http\Controllers;

use App\Models\WorkloadRecord;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class WorkloadController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $perPage = min((int) $request->get('per_page', 10), 100);

        $query = WorkloadRecord::with(['teacher', 'department', 'discipline', 'academicYear'])
            ->orderByDesc('created_at');

        if ($request->filled('semester')) {
            $query->where('semester', $request->semester);
        }
        if ($request->filled('financing')) {
            $query->where('financing', $request->financing);
        }
        if ($request->filled('teacher_id')) {
            $query->where('teacher_id', $request->teacher_id);
        }
        if ($request->filled('discipline_id')) {
            $query->where('discipline_id', $request->discipline_id);
        }

        $paginated = $query->paginate($perPage);

        return response()->json([
            'data' => $paginated->items(),
            'total' => $paginated->total(),
            'per_page' => $paginated->perPage(),
            'current_page' => $paginated->currentPage(),
            'last_page' => $paginated->lastPage(),
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $data = $this->validated($request);
        $record = WorkloadRecord::create($data);
        $record->load(['teacher', 'department', 'discipline', 'academicYear']);
        return response()->json($record, 201);
    }

    public function update(Request $request, WorkloadRecord $workload): JsonResponse
    {
        $data = $this->validated($request);
        $workload->update($data);
        $workload->load(['teacher', 'department', 'discipline', 'academicYear']);
        return response()->json($workload);
    }

    public function destroy(WorkloadRecord $workload): JsonResponse
    {
        $workload->delete();
        return response()->json(['message' => 'deleted']);
    }

    public function destroyAll(): JsonResponse
    {
        $count = WorkloadRecord::count();
        WorkloadRecord::truncate();
        return response()->json(['message' => "deleted {$count} records"]);
    }

    private function validated(Request $request): array
    {
        return $request->validate([
            'teacher_id' => 'required|exists:teachers,id',
            'department_id' => 'required|exists:departments,id',
            'academic_year_id' => 'required|exists:academic_years,id',
            'discipline_id' => 'required|exists:disciplines,id',
            'course' => 'nullable|integer|min:1|max:6',
            'students_count' => 'nullable|integer|min:0',
            'specialty_code' => 'nullable|string|max:20',
            'groups_count' => 'nullable|numeric|min:0',
            'education_form' => 'nullable|string|max:50',
            'semester' => 'required|in:1,2',
            'financing' => 'required|string|max:50',
            'lectures' => 'nullable|numeric|min:0',
            'practical' => 'nullable|numeric|min:0',
            'laboratory' => 'nullable|numeric|min:0',
            'module_control' => 'nullable|numeric|min:0',
            'consultations_semester' => 'nullable|numeric|min:0',
            'consultations_before_exam' => 'nullable|numeric|min:0',
            'credits' => 'nullable|numeric|min:0',
            'exams' => 'nullable|numeric|min:0',
            'course_works' => 'nullable|numeric|min:0',
            'vkr_bachelor' => 'nullable|numeric|min:0',
            'diploma_master' => 'nullable|numeric|min:0',
            'practice_management' => 'nullable|numeric|min:0',
            'gek' => 'nullable|numeric|min:0',
            'vkr_review' => 'nullable|numeric|min:0',
            'vkr_defense' => 'nullable|numeric|min:0',
            'phd_management' => 'nullable|numeric|min:0',
            'other' => 'nullable|numeric|min:0',
            'total' => 'nullable|numeric|min:0',
            'notes' => 'nullable|string|max:500',
        ]);
    }
}
