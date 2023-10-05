# Allgemeines

... TODO ...


# Beispiel JSON File:

```
[
  {
    "day": "5",
    "booking": [
      "EDDF",
      "EDGG_GIN",
      "EDGG_DKB",
      "EDUU_WUR",
      "EDDS_STG_APP"
    ]
  },
  {
    "rule": "every_X_days",
    "one_date": "2023-08-11",
    "days": "14",
    "booking": [
      "EDDF",
      "EDGG_GIN",
      "EDGG_DKB",
      "EDUU_FUL",
      "EDUU_SLN"
    ]
  },
  {
      "rule": "every_X_day_in_month",
      "day_of_week": 3,
      "number_day_in_month": 1,
      "booking": [
        "EDDK"
      ]
    },

]
```
- Regel 1: Jede Woche den 5 Tag (also Freitag)
- Regel 2: Alle 14 Tage vor/nach/am 11.08.23 (also alle zwei Wochen)
- Regel 1: Jeden zweiten (`number_day_in_month=1`) Mittwoch (`day_of_week=3`) im Monat
