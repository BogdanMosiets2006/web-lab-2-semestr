<?php

namespace App\Http\Controllers;

use App\Imports\WorkloadImport;
use App\Models\UploadedFile;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Maatwebsite\Excel\Facades\Excel;

class FileUploadController extends Controller
{
    public function upload(Request $request): JsonResponse
    {
        $request->validate([
            'file' => [
                'required',
                'file',
                'mimes:xlsx,xls',
                'max:20480', // 20 MB
            ],
        ], [
            'file.mimes' => 'Допустимые форматы файлов: .xlsx, .xls',
            'file.max'   => 'Размер файла не должен превышать 20 МБ',
        ]);

        $file = $request->file('file');

        // Сохранить файл в локальное хранилище
        $storedPath = $file->store('excel_uploads', 'local');

        // Сохранить запись о файле в БД
        $uploadedFile = UploadedFile::create([
            'user_id' => auth()->id(),
            'original_name' => $file->getClientOriginalName(),
            'stored_path' => $storedPath,
            'mime_type' => $file->getMimeType(),
            'file_size' => $file->getSize(),
        ]);

        // Распарсить Excel и занести данные в таблицы
        Excel::import(new WorkloadImport, $file);

        return response()->json([
            'message' => 'Файл успешно загружен и обработан',
            'file' => [
                'id' => $uploadedFile->id,
                'original_name' => $uploadedFile->original_name,
                'file_size' => $uploadedFile->file_size,
            ],
        ]);
    }

    public function index(): JsonResponse
    {
        $files = UploadedFile::with('user')
            ->orderByDesc('created_at')
            ->get()
            ->map(fn ($f) => [
                'id' => $f->id,
                'original_name' => $f->original_name,
                'file_size' => $f->file_size,
                'uploaded_by' => $f->user?->name,
                'created_at' => $f->created_at->format('d.m.Y H:i'),
            ]);

        return response()->json($files);
    }
}
