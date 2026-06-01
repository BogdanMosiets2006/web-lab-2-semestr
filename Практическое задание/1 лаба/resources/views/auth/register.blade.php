@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row justify-content-center" style="margin-top: 80px;">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <h4 class="text-center mb-4">
                        <i class="bi bi-person-plus"></i> &#1056;&#1077;&#1075;&#1080;&#1089;&#1090;&#1088;&#1072;&#1094;&#1080;&#1103;
                    </h4>

                    <form method="POST" action="{{ route('register') }}">
                        @csrf

                        <div class="form-group mb-3">
                            <label class="font-weight-bold">&#1048;&#1084;&#1103;</label>
                            <input type="text" name="name" value="{{ old('name') }}"
                                   class="form-control @error('name') is-invalid @enderror"
                                   required autofocus />
                            @error('name')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Email</label>
                            <input type="email" name="email" value="{{ old('email') }}"
                                   class="form-control @error('email') is-invalid @enderror"
                                   required />
                            @error('email')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="form-group mb-3">
                            <label class="font-weight-bold">&#1055;&#1072;&#1088;&#1086;&#1083;&#1100;</label>
                            <input type="password" name="password"
                                   class="form-control @error('password') is-invalid @enderror"
                                   required />
                            @error('password')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>

                        <div class="form-group mb-4">
                            <label class="font-weight-bold">&#1055;&#1086;&#1076;&#1090;&#1074;&#1077;&#1088;&#1076;&#1080;&#1090;&#1077; &#1087;&#1072;&#1088;&#1086;&#1083;&#1100;</label>
                            <input type="password" name="password_confirmation"
                                   class="form-control" required />
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">
                            &#1047;&#1072;&#1088;&#1077;&#1075;&#1080;&#1089;&#1090;&#1088;&#1080;&#1088;&#1086;&#1074;&#1072;&#1090;&#1100;&#1089;&#1103;
                        </button>

                        <p class="text-center mt-3 mb-0">
                            &#1059;&#1078;&#1077; &#1077;&#1089;&#1090;&#1100; &#1072;&#1082;&#1082;&#1072;&#1091;&#1085;&#1090;?
                            <a href="{{ route('login') }}">&#1042;&#1086;&#1081;&#1090;&#1080;</a>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
