<?php
use App\Http\Controllers\DictionaryController;
use App\Http\Controllers\FileUploadController;
use App\Http\Controllers\WorkloadController;
use Illuminate\Support\Facades\Route;

Route::middleware("web")->group(function () {
    Route::post("/upload", [FileUploadController::class, "upload"]);
    Route::get("/files", [FileUploadController::class, "index"]);
    Route::get("/workload", [WorkloadController::class, "index"]);
    Route::post("/workload", [WorkloadController::class, "store"]);
    Route::put("/workload/{workload}", [WorkloadController::class, "update"]);
    Route::delete("/workload/{workload}", [WorkloadController::class, "destroy"]);
    Route::delete("/workload-all", [WorkloadController::class, "destroyAll"]);
    Route::get("/dict/teachers", [DictionaryController::class, "teachers"]);
    Route::get("/dict/departments", [DictionaryController::class, "departments"]);
    Route::get("/dict/disciplines", [DictionaryController::class, "disciplines"]);
    Route::get("/dict/academic-years", [DictionaryController::class, "academicYears"]);
});
