<?php

namespace App\Filament\Resources\WorkloadRecords\Schemas;

use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;
use Filament\Schemas\Schema;

class WorkloadRecordForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema
            ->components([
                Select::make('teacher_id')
                    ->relationship('teacher', 'name')
                    ->required(),
                Select::make('department_id')
                    ->relationship('department', 'name')
                    ->required(),
                Select::make('academic_year_id')
                    ->relationship('academicYear', 'id')
                    ->required(),
                Select::make('discipline_id')
                    ->relationship('discipline', 'name')
                    ->required(),
                TextInput::make('course')
                    ->numeric()
                    ->default(null),
                TextInput::make('students_count')
                    ->numeric()
                    ->default(null),
                TextInput::make('specialty_code')
                    ->default(null),
                TextInput::make('groups_count')
                    ->numeric()
                    ->default(null),
                TextInput::make('education_form')
                    ->default(null),
                TextInput::make('semester')
                    ->required()
                    ->numeric(),
                TextInput::make('financing')
                    ->required()
                    ->default('бюджет'),
                TextInput::make('lectures')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('practical')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('laboratory')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('module_control')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('consultations_semester')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('consultations_before_exam')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('credits')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('exams')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('course_works')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('vkr_bachelor')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('diploma_master')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('practice_management')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('gek')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('vkr_review')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('vkr_defense')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('phd_management')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('other')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                TextInput::make('total')
                    ->required()
                    ->numeric()
                    ->default(0.0),
                Textarea::make('notes')
                    ->default(null)
                    ->columnSpanFull(),
            ]);
    }
}
