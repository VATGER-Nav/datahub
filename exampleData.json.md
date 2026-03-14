```
[
  {
    "logon": "EDXX_XXX_CTR",
    "frequency": "199.999",
    "abbreviation": "abbr.",
    "description": "Bremen/Langen/Muenchen Radar SectorX",
    "schedule_show_always": ["EDXX"],
    "schedule_show_booked": ["EDXX"],
    "relevant_airports": ["EDDY"],
    "gcap_status": "AFIS" | "1" | "2",
    "gcap_training_airport": true | false,
    "s1_twr": true | false,
    "cpdlc_login": "EDXX",
    "s1_theory": true
  }
]
```
- `description` (optional)
- `schedule_show_always` (optional) in which booking overview this station should appear. Station will always be shown in the overview.
- `schedule_show_booked` (optional) in which booking overview this station should appear. Station will only be shown in the overview if it is booked.
- If a station is listed in `schedule_show_always` it should not be listed in `schedule_show_booked` for the same overview and vice versa as `schedule_show_always` overwrites `schedule_show_booked` making the entry redudant.
- `relevant_airports` (optional) which airports are covered by the station. If the station starts with the ICAO code of an airport, this does not need to be specified.
- `gcap_status` (optional) represents the status of the station as defined in the Global Controller Administration Policy (GCAP). `"AFIS"` unrestricted station, `"1"` tier 1 station or `"2"` tier 2 station
- `gcap_training_airport` (optional) true if the station is used for solo endorsements of trainees (see VATGER training policy). `false` as default if the key does not exist
- `s1_twr` (optional) true if station is part of towers that can be controlled with S1 rating
- `s1_theory` (optional) true if station can be controlled with only theory training and S1 rating
