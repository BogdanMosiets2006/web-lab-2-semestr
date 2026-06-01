<?php

namespace App\Filament\Resources\WorkloadRecords\Tables;

use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\EditAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

class WorkloadRecordsTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('teacher.name')
                    ->searchable(),
                TextColumn::make('department.name')
                    ->searchable(),
                TextColumn::make('academicYear.id')
                    ->searchable(),
                TextColumn::make('discipline.name')
                    ->searchable(),
                TextColumn::make('course')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('students_count')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('specialty_code')
                    ->searchable(),
                TextColumn::make('groups_count')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('education_form')
                    ->searchable(),
                TextColumn::make('semester')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('financing')
                    ->searchable(),
                TextColumn::make('lectures')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('practical')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('laboratory')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('module_control')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('consultations_semester')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('consultations_before_exam')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('credits')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('exams')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('course_works')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('vkr_bachelor')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('diploma_master')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('practice_management')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('gek')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('vkr_review')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('vkr_defense')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('phd_management')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('other')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('total')
                    ->numeric()
                    ->sortable(),
                TextColumn::make('created_at')
                    ->dateTime()
                    ->sortable()
                    ->toggleable(isToggledHiddenByDefault: true),
                TextColumn::make('updated_at')
                    ->dateTime()
                    ->sortable()
                    ->toggleable(isToggledHiddenByDefault: true),
            ])
            ->filters([
                //
            ])
            ->recordActions([
                EditAction::make(),
            ])
            ->toolbarActions([
                BulkActionGroup::make([
                    DeleteBulkAction::make(),
                ]),
            ]);
    }
}
