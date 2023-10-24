```
[
  {
    "logon": "EDXX_XXX_CTR",
    "frequency": "199.999",
    "abbreviation": "abbr.",
    "description": "Bremen/Langen/Muenchen Radar SectorX",
    "schedule_minstation": ["EDXX"],
    "schedule_groups": ["EDXX"],
    "relevant_airports": ["EDXX"]
  }
]
```

- `schedule_minstation` (optional) in which booking overview this station should appear. Station will always be shown in the overview. If
- `schedule_groups` (optional) in which booking overview this station should appear. Station will only be shown in the overview if it is booked.
- If a station is listed in `schedule_minstation` it should not be listed in `schedule_groups` for the same overview and vice versa as `schedule_minstation` overwrites `schedule_group` making the entry redudant.
- `relevant_airports` (optional) which airports are covered by the station. If the station starts with the ICAO code of an airport, this does not have to be specified here.
