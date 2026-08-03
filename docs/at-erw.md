---
layout: default
title: at-erw
---

# at-erw

Erwerbstätigkeit — extend or newly apply for a residence permit for the purpose of gainful employment.

**Edge coverage:** 0/23 (0%) — solid arrow = covered, dashed = not covered

```mermaid
flowchart TD
    application_type{"What type of application are you making?"}
    interruptions_new{"(new application) Have there been any interruptions in the stay in Germany of more than 6 months?"}
    has_residence_permit{"Do you already have a residence permit from a German Foreigners' Registration Office?"}
    has_diplomatic_visa{"Have you received a visa from a German diplomatic mission abroad?"}
    has_schengen_permit{"Do you have a residence permit issued to you in another Schengen State?"}
    has_temp_residence{"Do you have a 'certificate of temporary residence permit'?"}
    has_suspension{"Do you have a 'certificate of suspension of deportation (tolerated stay)'?"}
    has_vocational_qualification{"Have you completed a university degree, qualified vocational training, or state-recognised vocational training in a care assistant role?"}
    country_group{"Which country do you belong to?"}
    interruptions_renew{"(renewal) Have there been any interruptions in the stay in Germany of more than 6 months?"}
    has_existing_permit{"Do you already have a residence permit?"}
    periods_abroad_new["Enter periods spent abroad (date range + reason each), then handle maintenance obligations + statutory violations components"]
    periods_abroad_renew["Enter periods spent abroad (date range + reason each), then handle maintenance obligations + statutory violations components"]
    upload_residence_permit["Upload copy of current residence permit, then handle maintenance obligations + statutory violations components"]
    upload_diplomatic_visa["Upload copy of current visa, then handle maintenance obligations + statutory violations components"]
    upload_schengen_permit["Upload copy of foreign residence permit, then handle maintenance obligations + statutory violations components"]
    blocked_temp_residence["Service blocked — asylum procedure in progress, apply for a work permit at the Foreigners' Office instead"]
    upload_duldung["Upload copy of certificate of suspension of deportation (tolerated stay), then handle maintenance obligations + statutory violations components"]
    blocked_no_qualification["Service blocked — tolerated stay without a qualifying degree, contact the Foreigners' Registration Office directly"]
    continue_europe["No additional upload required, handle maintenance obligations + statutory violations components"]
    upload_entry_stamp["Upload copy of entry stamp, then handle maintenance obligations + statutory violations components"]
    blocked_different_country["Service blocked — a visa from a German embassy is required before applying"]
    upload_existing_permit["Upload copy of existing residence permit, then handle maintenance obligations + statutory violations components"]
    blocked_no_existing_permit["Service blocked — cannot renew without an existing permit"]
    application_type -.->|"new"| interruptions_new
    application_type -.->|"renew"| interruptions_renew
    interruptions_new -.->|"yes"| periods_abroad_new
    interruptions_new -.->|"no"| has_residence_permit
    has_residence_permit -.->|"yes"| upload_residence_permit
    has_residence_permit -.->|"no"| has_diplomatic_visa
    has_diplomatic_visa -.->|"yes"| upload_diplomatic_visa
    has_diplomatic_visa -.->|"no"| has_schengen_permit
    has_schengen_permit -.->|"yes"| upload_schengen_permit
    has_schengen_permit -.->|"no"| has_temp_residence
    has_temp_residence -.->|"yes"| blocked_temp_residence
    has_temp_residence -.->|"no"| has_suspension
    has_suspension -.->|"yes"| has_vocational_qualification
    has_suspension -.->|"no"| country_group
    has_vocational_qualification -.->|"yes"| upload_duldung
    has_vocational_qualification -.->|"no"| blocked_no_qualification
    country_group -.->|"europe"| continue_europe
    country_group -.->|"offshore"| upload_entry_stamp
    country_group -.->|"different"| blocked_different_country
    interruptions_renew -.->|"yes"| periods_abroad_renew
    interruptions_renew -.->|"no"| has_existing_permit
    has_existing_permit -.->|"yes"| upload_existing_permit
    has_existing_permit -.->|"no"| blocked_no_existing_permit
```

## Branch gaps

- `application_type` (0/2 covered): missing new, renew
- `interruptions_new` (0/2 covered): missing yes, no
- `has_residence_permit` (0/2 covered): missing yes, no
- `has_diplomatic_visa` (0/2 covered): missing yes, no
- `has_schengen_permit` (0/2 covered): missing yes, no
- `has_temp_residence` (0/2 covered): missing yes, no
- `has_suspension` (0/2 covered): missing yes, no
- `has_vocational_qualification` (0/2 covered): missing yes, no
- `country_group` (0/3 covered): missing europe, offshore, different
- `interruptions_renew` (0/2 covered): missing yes, no
- `has_existing_permit` (0/2 covered): missing yes, no
