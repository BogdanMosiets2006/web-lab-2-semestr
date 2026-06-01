<?php

namespace App\Filament\Resources\WorkloadRecords\Pages;

use App\Filament\Resources\WorkloadRecords\WorkloadRecordResource;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListWorkloadRecords extends ListRecords
{
    protected static string $resource = WorkloadRecordResource::class;

    protected function getHeaderActions(): array
    {
        return [
            CreateAction::make(),
        ];
    }
}
