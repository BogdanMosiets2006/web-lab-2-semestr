<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Discipline extends Model
{
    protected $fillable = ['name'];

    public function workloadRecords(): HasMany
    {
        return $this->hasMany(WorkloadRecord::class);
    }
}
