<?php

namespace App\Filament\Resources\WorkloadRecords;

use App\Filament\Resources\WorkloadRecords\Pages\CreateWorkloadRecord;
use App\Filament\Resources\WorkloadRecords\Pages\EditWorkloadRecord;
use App\Filament\Resources\WorkloadRecords\Pages\ListWorkloadRecords;
use App\Filament\Resources\WorkloadRecords\Schemas\WorkloadRecordForm;
use App\Filament\Resources\WorkloadRecords\Tables\WorkloadRecordsTable;
use App\Models\WorkloadRecord;
use BackedEnum;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Table;

class WorkloadRecordResource extends Resource
{
    protected static ?string $model = WorkloadRecord::class;

    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedRectangleStack;

    protected static ?string $recordTitleAttribute = 'id';

    public static function form(Schema $schema): Schema
    {
        return WorkloadRecordForm::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return WorkloadRecordsTable::configure($table);
    }

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => ListWorkloadRecords::route('/'),
            'create' => CreateWorkloadRecord::route('/create'),
            'edit' => EditWorkloadRecord::route('/{record}/edit'),
        ];
    }
}
