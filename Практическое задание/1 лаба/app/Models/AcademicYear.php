<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class AcademicYear extends Model
{
    protected $fillable = ['label'];

    public function workloadRecords(): HasMany
    {
        return $this->hasMany(WorkloadRecord::class);
    }
}
