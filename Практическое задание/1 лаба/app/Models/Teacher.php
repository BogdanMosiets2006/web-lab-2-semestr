<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Teacher extends Model
{
    protected $fillable = ['name', 'position'];

    public function workloadRecords(): HasMany
    {
        return $this->hasMany(WorkloadRecord::class);
    }
}
