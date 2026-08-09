---
layout: default
title: aw-auf
---

# aw-auf

Aufenthaltskarte — residence card for EU/EEA citizens and their family members (persons entitled to freedom of movement).

**Edge coverage:** 0/17 (0%) — solid arrow = covered, dashed = not covered

```mermaid
flowchart TD
    application_type{"Please select your request"}
    nationality_group{"I have the nationality..."}
    blocked_switzerland["Service blocked — Swiss nationality"]
    blocked_non_eu_eea["Service blocked — nationality outside the EU/EEA"]
    stay_duration{"How long have you been staying in Germany?"}
    currently_employed{"(less than five years in Germany) Are you currently employed?"}
    employed_no["Not employed — separate question tree, not yet built"]
    employment_location{"Are you employed in Germany or another country?"}
    blocked_employed_germany["Service blocked — employed in Germany"]
    blocked_employed_other_country["Service blocked — employed outside the EU/EEA"]
    prior_work_duration{"How long have you previously worked in Germany without interruption?"}
    blocked_short_prior_work["Service blocked — less than three years of prior uninterrupted work"]
    residence_in_germany{"Do you still have a residence in Germany?"}
    blocked_residence_no_weekly_return["Service blocked — residence kept but no weekly return to Germany"]
    blocked_no_residence["Service blocked — no residence kept in Germany"]
    stays_and_absences_page["Reach the 'Stays and absences' page — not yet built further"]
    ak_not_built["Family member of an EU/EEA citizen requesting a residence card — branch not yet built"]
    application_type -.->|"DAB"| nationality_group
    application_type -.->|"AK"| ak_not_built
    nationality_group -.->|"eu"| stay_duration
    nationality_group -.->|"schweiz"| blocked_switzerland
    nationality_group -.->|"not_eu"| blocked_non_eu_eea
    stay_duration -.->|"more_than_five"| stays_and_absences_page
    stay_duration -.->|"less_than_five"| currently_employed
    currently_employed -.->|"yes"| employment_location
    currently_employed -.->|"no"| employed_no
    employment_location -.->|"germany"| blocked_employed_germany
    employment_location -.->|"eu_country"| prior_work_duration
    employment_location -.->|"other_country"| blocked_employed_other_country
    prior_work_duration -.->|"more_than_three"| residence_in_germany
    prior_work_duration -.->|"less_than_three"| blocked_short_prior_work
    residence_in_germany -.->|"yes_mit_rueckkehr"| stays_and_absences_page
    residence_in_germany -.->|"yes_ohne_rueckkehr"| blocked_residence_no_weekly_return
    residence_in_germany -.->|"no"| blocked_no_residence
```

## Branch gaps

- `application_type` (0/2 covered): missing DAB, AK
- `nationality_group` (0/3 covered): missing eu, schweiz, not_eu
- `stay_duration` (0/2 covered): missing more_than_five, less_than_five
- `currently_employed` (0/2 covered): missing yes, no
- `employment_location` (0/3 covered): missing germany, eu_country, other_country
- `prior_work_duration` (0/2 covered): missing more_than_three, less_than_three
- `residence_in_germany` (0/3 covered): missing yes_mit_rueckkehr, yes_ohne_rueckkehr, no
