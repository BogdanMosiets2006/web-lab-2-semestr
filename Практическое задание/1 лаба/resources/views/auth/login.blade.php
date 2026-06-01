@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row justify-content-center" style="margin-top: 80px;">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <h4 class="text-center mb-4">
                        <i class="bi bi-box-arrow-in-right"></i> &#1042;&#1093;&#1086;&#1076;
                    </h4>

                    @if (session('status'))
                        <div class="alert alert-success">{{ session('status') }}</div>
                    @endif

                    <form method="POST" action="{{ route('login') }}">
                        @csrf

                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Email</label>
                            <input type="email" name="email" value="{{ old('email') }}"
                                   class="form-control @error('email') is-invalid @enderror"
                                   required autofocus />
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

                        <div class="form-group mb-3">
                            <div class="custom-control custom-checkbox">
                                <input type="checkbox" name="remember" id="remember"
                                       class="custom-control-input" {{ old('remember') ? 'checked' : '' }}>
                                <label class="custom-control-label" for="remember">
                                    &#1047;&#1072;&#1087;&#1086;&#1084;&#1085;&#1080;&#1090;&#1100; &#1084;&#1077;&#1085;&#1103;
                                </label>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">
                            &#1042;&#1086;&#1081;&#1090;&#1080;
                        </button>

                        <p class="text-center mt-3 mb-0">
                            &#1053;&#1077;&#1090; &#1072;&#1082;&#1082;&#1072;&#1091;&#1085;&#1090;&#1072;?
                            <a href="{{ route('register') }}">&#1047;&#1072;&#1088;&#1077;&#1075;&#1080;&#1089;&#1090;&#1088;&#1080;&#1088;&#1086;&#1074;&#1072;&#1090;&#1100;&#1089;&#1103;</a>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
