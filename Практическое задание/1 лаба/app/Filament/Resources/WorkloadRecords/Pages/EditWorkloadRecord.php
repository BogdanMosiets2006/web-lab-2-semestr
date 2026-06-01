<?php

namespace App\Filament\Resources\WorkloadRecords\Pages;

use App\Filament\Resources\WorkloadRecords\WorkloadRecordResource;
use Filament\Actions\DeleteAction;
use Filament\Resources\Pages\EditRecord;

class EditWorkloadRecord extends EditRecord
{
    protected static string $resource = WorkloadRecordResource::class;

    protected function getHeaderActions(): array
    {
        return [
            DeleteAction::make(),
        ];
    }
}
