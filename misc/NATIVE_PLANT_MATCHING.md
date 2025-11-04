# Native Plant Matching Feature

## Overview
The GBIF data collection job now automatically identifies which observations are native California plants by cross-referencing against the `native_plants` database.

## Changes Made

### 1. Database Schema
Added `native` boolean column to `gbif_data` table:
```sql
ALTER TABLE gbif_data ADD COLUMN native BOOLEAN DEFAULT FALSE;
CREATE INDEX idx_gbif_native ON gbif_data(native);
```

### 2. Model Updates
Updated `GbifData` model (`/speciestrack/models/gbif_data.py`):
- Added `native` Boolean column
- Updated `to_dict()` method to include native status

### 3. Matching Logic
The job uses intelligent matching to handle differences between GBIF and native_plants naming:

**Problem:** GBIF includes author names (e.g., "Artemisia californica Less.") while native_plants table has just species names (e.g., "Artemisia californica")

**Solution:** Two-step matching process:
1. First tries exact match
2. If no exact match, extracts genus and species (first two words) from GBIF name and does a LIKE match

**Code location:** `/speciestrack/jobs/gbif_job.py` lines 121-138

```python
# First try exact match
is_native = NativePlant.query.filter_by(botanical_name=scientific_name).first() is not None

# If no exact match, check with genus + species only
if not is_native:
    words = scientific_name.split()
    if len(words) >= 2:
        genus_species = f"{words[0]} {words[1]}"
        is_native = NativePlant.query.filter(
            NativePlant.botanical_name.like(f"{genus_species}%")
        ).first() is not None
```

## Results

### Test Results
From latest test run:
- **Total observations**: 436
- **Native plants**: 112 (25.7%)
- **Non-native**: 324 (74.3%)

### Most Observed Native Plants
1. Hemizonia congesta (6 observations)
2. Lupinus microcarpus (5 observations)
3. Marah fabacea (4 observations)
4. Ribes sanguineum (4 observations)
5. Trillium chloropetalum (4 observations)

### Example Matches
| GBIF Scientific Name | Matched Native Plant | Common Name |
|---------------------|---------------------|--------------|
| Artemisia californica Less. | Artemisia californica | California Sagebrush |
| Umbellularia californica (Hook. & Arn.) Nutt. | Umbellularia californica | California Laurel |
| Eschscholzia californica Cham. | Eschscholzia californica | California Poppy |
| Quercus agrifolia Née | Quercus agrifolia | Coast Live Oak |

## Querying Native Plant Data

### Get all native plant observations
```python
from speciestrack.models import GbifData

native_plants = GbifData.query.filter_by(native=True).all()
```

### Count native vs non-native
```sql
SELECT
  native,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM gbif_data
GROUP BY native;
```

### Find most observed native plants
```sql
SELECT
  scientific_name,
  COUNT(*) as observations
FROM gbif_data
WHERE native = true
GROUP BY scientific_name
ORDER BY observations DESC
LIMIT 10;
```

### Get native plants observed on a specific date
```sql
SELECT DISTINCT scientific_name
FROM gbif_data
WHERE native = true
AND DATE(fetch_date) = '2025-11-03'
ORDER BY scientific_name;
```

## Benefits

1. **Ecological Insights**: Easily identify which native species are present in the observation area
2. **Conservation Tracking**: Monitor native plant populations over time
3. **Biodiversity Analysis**: Calculate ratios of native vs invasive species
4. **Educational**: Help users learn about California native plants

## Future Enhancements

Potential improvements:
1. Add `endemic` field for California endemic species
2. Add `invasive` field to flag invasive species
3. Add `conservation_status` (endangered, threatened, etc.)
4. Link to additional native plant metadata (bloom time, habitat, etc.)
