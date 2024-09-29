# Example JSON File:

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

Show the stations listed under `booking` as `wanted` as specified by the following rules.

| Rule | rule specifier / parameter                                                   | explanation                                                                                      |
| :--: | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
|  1   | `day: X`                                                                     | Every Xth `day` of every week                                                                    |
|  2   | `"rule": "every_X_days", "one_date": "2023-08-11","days": "14"`              | Every X `days` before, after and on the specified `one_date`                                     |
|  3   | `"rule": "every_X_day_in_month", "day_of_week": 3, "number_day_in_month": 1` | See example above: Every second (`number_day_in_month=1`) Wednesday (`day_of_week=3`) each month |

Stations in the booking property do not need to be specified by their full logons. Instead all matching stations will be shown (i.e. entry "EDDF" will show all stations beginning with "EDDF").
