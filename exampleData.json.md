```
[
  {
    "logon": "EDXX_XXX_CTR",
    "frequency": "199.999",
    "abbreviation": "abbr.",
    "description": "Bremen/Langen/Muenchen Radar SectorX",
    "schedule_minstation": ["EDXX"],
    "schedule_groups": ["EDXX"],
    "relevant_airports": ["EDDY"],
    "gcap_status": "0" | "1" | "AFIS" | "MIL TWR" | "MIL APP",
    "gcap_training_aiport": true | false,
    "cpdlc_login": "EDXX"
  }
]
```

- `schedule_minstation` (optional) in which booking overview this station should appear. Station will always be shown in the overview. If
- `schedule_groups` (optional) in which booking overview this station should appear. Station will only be shown in the overview if it is booked.
- If a station is listed in `schedule_minstation` it should not be listed in `schedule_groups` for the same overview and vice versa as `schedule_minstation` overwrites `schedule_group` making the entry redudant.
- `relevant_airports` (optional) which airports are covered by the station. If the station starts with the ICAO code of an airport, this does not need to be specified.
- `gcap_status` represents the status of the station as defined in the Global Controller Administration Policy (GCAP) with `"0"` being the default if the `gcap_class` key does not exist. `"0"` unrestricted station, `"1"` tier 1 station, `"AFIS" | "MIL TWR" | "MIL APP"` tier 2 station requiring the respective endorsement
- `gcap_training_aiport` true if the station is used for solo endorsements of trainees (see VATGER training policy). `false` as default if the key does not exist
