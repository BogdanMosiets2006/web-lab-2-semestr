@extends('layouts.app')
@section('title', 'Workload')
@section('content')
<div class="card shadow-sm mb-3">
    <div class="card-body">
        <div id="vue-file-upload"></div>
    </div>
</div>
<div class="card shadow-sm">
    <div class="card-body">
        <div
            id="vue-workload-table"
            data-is-auth="{{ auth()->check() ? 'true' : 'false' }}"
        ></div>
    </div>
</div>
@endsection
