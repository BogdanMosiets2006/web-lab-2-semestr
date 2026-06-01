<?php

namespace App\Http\Controllers;

use App\Models\AcademicYear;
use App\Models\Department;
use App\Models\Discipline;
use App\Models\Teacher;
use Illuminate\Http\JsonResponse;

class DictionaryController extends Controller
{
    public function teachers(): JsonResponse
    {
        return response()->json(Teacher::orderBy('name')->get(['id', 'name', 'position']));
    }

    public function departments(): JsonResponse
    {
        return response()->json(Department::orderBy('name')->get(['id', 'name']));
    }

    public function disciplines(): JsonResponse
    {
        return response()->json(Discipline::orderBy('name')->get(['id', 'name']));
    }

    public function academicYears(): JsonResponse
    {
        return response()->json(AcademicYear::orderByDesc('label')->get(['id', 'label']));
    }
}
