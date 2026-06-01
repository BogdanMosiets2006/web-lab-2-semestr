{{-- resources/views/pages/home.blade.php --}}
@extends('layouts.app')

@section('title', 'Главная — Загрузка файла')

@section('content')
<div class="row justify-content-center">
    <div class="col-md-8">

        <div class="card shadow-sm">
            <div class="card-header bg-white">
                <h5 class="mb-0">
                    <i class="bi bi-file-earmark-arrow-up me-2 text-success"></i>
                    Загрузка Excel-файла с нагрузкой
                </h5>
            </div>
            <div class="card-body">
                {{-- Vue-компонент загрузки файла --}}
                <div id="vue-file-upload"></div>
            </div>
        </div>

        @auth
        <div class="mt-4 text-center">
            <a href="{{ route('workload') }}" class="btn btn-primary">
                <i class="bi bi-table me-2"></i>Перейти к таблице данных
            </a>
        </div>
        @endauth

    </div>
</div>
@endsection
