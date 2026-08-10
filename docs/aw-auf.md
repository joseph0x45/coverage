---
layout: default
title: aw-auf
---

# aw-auf

Aufenthaltskarte — residence card for EU/EEA citizens and their family members (persons entitled to freedom of movement).

**Edge coverage:** 0/33 (0%) — solid arrow = covered, dashed = not covered

```mermaid
flowchart TD
    application_type{"Please select your request"}
    nationality_group{"I have the nationality..."}
    blocked_switzerland["Service blocked — Swiss nationality"]
    blocked_non_eu_eea["Service blocked — nationality outside the EU/EEA"]
    stay_duration{"How long have you been staying in Germany?"}
    currently_employed{"(less than five years in Germany) Are you currently employed?"}
    previously_employed{"Have you previously been employed in Germany or another EU/EEC country?"}
    blocked_never_employed["Service blocked — never employed in Germany or another EU/EEC country"]
    retirement_reason{"Why have you retired from working life?"}
    disability_pension{"Are you entitled to a disability pension within German federal territory?"}
    blocked_no_disability_pension["Service blocked — not entitled to a disability pension within German federal territory"]
    stays_and_absences_via_disability_pension["Reach the 'Stays and absences' page — not yet built further"]
    retirement_reason_reduced_capacity_not_built["Retired due to a full reduction in earning capacity — not yet built"]
    blocked_no_retirement_reason_applies["Service blocked — none of the retirement-reason statements apply"]
    resident_three_years{"Have you been continuously resident in German federal territory for at least three years?"}
    employed_last_12_months{"Have you engaged in any employment in German federal territory in the last twelve months?"}
    spouse_is_german_national{"Is your spouse or civil partner a German national?"}
    spouse_lost_german_citizenship{"Did your spouse or partner lose German citizenship by marrying you before 31 March 1953?"}
    blocked_spouse_citizenship["Service blocked — spouse/partner did not lose German citizenship by marrying before 31 March 1953"]
    employment_location{"Are you employed in Germany or another country?"}
    blocked_employed_germany["Service blocked — employed in Germany"]
    blocked_employed_other_country["Service blocked — employed outside the EU/EEA"]
    prior_work_duration{"How long have you previously worked in Germany without interruption?"}
    blocked_short_prior_work["Service blocked — less than three years of prior uninterrupted work"]
    residence_in_germany{"Do you still have a residence in Germany?"}
    blocked_residence_no_weekly_return["Service blocked — residence kept but no weekly return to Germany"]
    blocked_no_residence["Service blocked — no residence kept in Germany"]
    stays_and_absences_via_five_years["Reach the 'Stays and absences' page — not yet built further"]
    stays_and_absences_via_residence["Reach the 'Stays and absences' page — not yet built further"]
    stays_and_absences_via_recent_employment["Reach the 'Stays and absences' page — not yet built further"]
    stays_and_absences_via_german_spouse["Reach the 'Stays and absences' page — not yet built further"]
    stays_and_absences_via_former_german_spouse["Reach the 'Stays and absences' page — not yet built further"]
    ak_not_built["Family member of an EU/EEA citizen requesting a residence card — branch not yet built"]
    application_type -.->|"DAB"| nationality_group
    application_type -.->|"AK"| ak_not_built
    nationality_group -.->|"eu"| stay_duration
    nationality_group -.->|"schweiz"| blocked_switzerland
    nationality_group -.->|"not_eu"| blocked_non_eu_eea
    stay_duration -.->|"more_than_five"| stays_and_absences_via_five_years
    stay_duration -.->|"less_than_five"| currently_employed
    currently_employed -.->|"yes"| employment_location
    currently_employed -.->|"no"| previously_employed
    previously_employed -.->|"yes"| retirement_reason
    previously_employed -.->|"no"| blocked_never_employed
    retirement_reason -.->|"ruhestand"| resident_three_years
    retirement_reason -.->|"unfall"| disability_pension
    retirement_reason -.->|"erwerbsminderung"| retirement_reason_reduced_capacity_not_built
    retirement_reason -.->|"andere"| blocked_no_retirement_reason_applies
    disability_pension -.->|"yes"| stays_and_absences_via_disability_pension
    disability_pension -.->|"no"| blocked_no_disability_pension
    resident_three_years -.->|"yes"| employed_last_12_months
    resident_three_years -.->|"no"| spouse_is_german_national
    employed_last_12_months -.->|"yes"| stays_and_absences_via_recent_employment
    employed_last_12_months -.->|"no"| spouse_is_german_national
    spouse_is_german_national -.->|"yes"| stays_and_absences_via_german_spouse
    spouse_is_german_national -.->|"no"| spouse_lost_german_citizenship
    spouse_lost_german_citizenship -.->|"yes"| stays_and_absences_via_former_german_spouse
    spouse_lost_german_citizenship -.->|"no"| blocked_spouse_citizenship
    employment_location -.->|"germany"| blocked_employed_germany
    employment_location -.->|"eu_country"| prior_work_duration
    employment_location -.->|"other_country"| blocked_employed_other_country
    prior_work_duration -.->|"more_than_three"| residence_in_germany
    prior_work_duration -.->|"less_than_three"| blocked_short_prior_work
    residence_in_germany -.->|"yes_mit_rueckkehr"| stays_and_absences_via_residence
    residence_in_germany -.->|"yes_ohne_rueckkehr"| blocked_residence_no_weekly_return
    residence_in_germany -.->|"no"| blocked_no_residence
```

## Branch gaps

- `application_type` (0/2 covered): missing DAB, AK
- `nationality_group` (0/3 covered): missing eu, schweiz, not_eu
- `stay_duration` (0/2 covered): missing more_than_five, less_than_five
- `currently_employed` (0/2 covered): missing yes, no
- `previously_employed` (0/2 covered): missing yes, no
- `retirement_reason` (0/4 covered): missing ruhestand, unfall, erwerbsminderung, andere
- `disability_pension` (0/2 covered): missing yes, no
- `resident_three_years` (0/2 covered): missing yes, no
- `employed_last_12_months` (0/2 covered): missing yes, no
- `spouse_is_german_national` (0/2 covered): missing yes, no
- `spouse_lost_german_citizenship` (0/2 covered): missing yes, no
- `employment_location` (0/3 covered): missing germany, eu_country, other_country
- `prior_work_duration` (0/2 covered): missing more_than_three, less_than_three
- `residence_in_germany` (0/3 covered): missing yes_mit_rueckkehr, yes_ohne_rueckkehr, no
