# at-neb

Nebenbestimmungen — request a change to a condition (Nebenbestimmung) on an existing residence document.

**Edge coverage:** 0/2 (0%) — solid arrow = covered, dashed = not covered

```mermaid
flowchart TD
    residence_document{"What is your current residence document?"}
    upload_residence_title["Upload copy of residence title + supplementary sheet, describe the additional provision to be changed"]
    upload_letter_of_recognition["Upload copy of BAMF letter of recognition, describe the additional provision to be changed"]
    residence_document -.->|"residence_title"| upload_residence_title
    residence_document -.->|"letter_of_recognition"| upload_letter_of_recognition
```

## Branch gaps

- `residence_document` (0/2 covered): missing residence_title, letter_of_recognition
