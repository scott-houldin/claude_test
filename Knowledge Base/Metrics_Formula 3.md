# Standardized Metric Formulas for 2mn_metrics Table

This document contains the official, standardized BigQuery SQL formulas for calculating key metrics from the `anbc-hcb-dev.provider_ds_hcb_dev.2mn_metrics` table, based on the logic in [Weekly Reporting - Initial Review](https://cvshealth.thoughtspot.cloud/?utm_source=welcome-email&utm_medium=email#/insights/pinboard/abe0850a-c2da-44b5-9013-886ed39ec186?view=d2ccf277-3c04-4344-843c-45fa718e9bd9) and other validated reporting scripts.

**IMPORTANT:** These formulas are designed for a general analysis of non-pending cases. The SQL Agent must apply the following `WHERE` clause to any query using these metrics:

```sql
WHERE
    pending_auth_ind = 0
    AND LOWER(admission_type_desc) IN ('elective', 'emergency/urgent')
```

---

## I. Base Metrics

These are foundational counts and aggregations.

---

### **1. `num_pmes`**
- **Description:** The total number of unique cases.
- **Formula:**
  ```sql
  COUNT(DISTINCT pme_reference_no)
  ```

### **2. `total_los_cnt`**
- **Description:** The sum of the actual length of stay days for all cases.
- **Formula:**
  ```sql
  SUM(act_los_day_cnt)
  ```

### **3. `avg_tat`**
- **Description:** The average turn-around time for cases.
- **Formula:**
  ```sql
  AVG(tat)
  ```

### **4. `denied_pmes`**
- **Description:** The total number of cases that were finally denied.
- **Formula:**
  ```sql
  SUM(final_denied_ind)
  ```

### **5. `admin_denied_pmes`**
- **Description:** The count of cases that were finally denied for administrative reasons.
- **Formula:**
  ```sql
  SUM(CASE WHEN final_denied_ind = 1 AND final_administrative_denial_ind = 1 THEN 1 ELSE 0 END)
  ```

### **6. `medicalnecessity_denied_pmes`**
- **Description:** The count of cases finally denied for clinical reasons.
- **Formula:**
  ```sql
  SUM(CASE WHEN final_denied_ind = 1 AND final_clinical_denial_ind = 1 THEN 1 ELSE 0 END)
  ```

### **7. `other_denied_pmes`**
- **Description:** The count of cases finally denied for reasons other than administrative or clinical.
- **Formula:**
  ```sql
  SUM(CASE WHEN final_denied_ind = 1 AND final_clinical_denial_ind = 0 AND final_administrative_denial_ind = 0 THEN 1 ELSE 0 END)
  ```

### **8. `um_exempt`**
- **Description:** The count of cases associated with a provider on the UM exempt list.
- **Formula:**
  ```sql
  SUM(prvdr_um_exempt_ind)
  ```

### **9. `auto_approvals`**
- **Description:** The count of cases reviewed by 'auto-approved', regardless of the final outcome. **Note:** This logic differs from previous versions which required the case to be approved.
- **Formula:**
  ```sql
  SUM(CASE WHEN LOWER(reviewer_ir) = 'auto-approved' THEN 1 ELSE 0 END)
  ```

### **10. `auto_approvals_um_exempt`**
- **Description:** The count of auto-reviewed cases for providers on the UM exempt list.
- **Formula:**
  ```sql
  SUM(CASE WHEN LOWER(reviewer_ir) = 'auto-approved' AND prvdr_um_exempt_ind = 1 THEN 1 ELSE 0 END)
  ```

### **11. `auto_approvals_all_other`**
- **Description:** The count of auto-reviewed cases for providers not on the UM exempt list.
- **Formula:**
  ```sql
  SUM(CASE WHEN LOWER(reviewer_ir) = 'auto-approved' AND COALESCE(prvdr_um_exempt_ind, 0) <> 1 THEN 1 ELSE 0 END)
  ```

### **12. `nurse_approvals`**
- **Description:** The count of approved cases not reviewed by 'Auto-Approved' or 'MD'. Logic is based on the `reviewer_ir` column.
- **Formula:**
  ```sql
  SUM(CASE WHEN final_denied_ind = 0 AND NOT(LOWER(reviewer_ir) IN ('auto-approved', 'md')) THEN 1 ELSE 0 END)
  ```

### **13. `md_referred`**
- **Description:** The count of cases where the reviewer was 'MD', based on the `reviewer_ir` column.
- **Formula:**
  ```sql
  SUM(CASE WHEN LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END)
  ```

### **14. `md_approvals`**
- **Description:** The count of approved cases where the reviewer was 'MD', based on the `reviewer_ir` column.
- **Formula:**
  ```sql
  SUM(CASE WHEN final_denied_ind = 0 AND LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END)
  ```

### **15. `overturned`**
- **Description:** The count of cases that were overturned on appeal.
- **Formula:**
  ```sql
  SUM(CASE WHEN overturned_ind = 1 AND app_reverse_ind = 1 THEN 1 ELSE 0 END)
  ```

### **16. `l2_count_raw`**
- **Description:** The total raw count from the L2 auto-approval process.
- **Formula:**
  ```sql
  SUM(l2_count)
  ```

---

## II. Derived Metrics & KPIs (Rates)

These metrics calculate the rate of an event by dividing a base metric by a denominator (usually the total number of cases).

---

### **1. `Average_LOS_per_PME`**
- **Description:** The average length of stay per unique case.
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(act_los_day_cnt), COUNT(DISTINCT pme_reference_no))
  ```

### **2. `overall_denial_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(final_denied_ind), COUNT(DISTINCT pme_reference_no))
  ```

### **3. `admin_denial_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN final_denied_ind = 1 AND final_administrative_denial_ind = 1 THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **4. `medical_necessity_denial_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN final_denied_ind = 1 AND final_clinical_denial_ind = 1 THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **5. `auto_approval_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN LOWER(reviewer_ir) = 'auto-approved' THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **6. `nurse_approval_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN final_denied_ind = 0 AND NOT(LOWER(reviewer_ir) IN ('auto-approved', 'md')) THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **7. `md_approval_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN final_denied_ind = 0 AND LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **8. `md_referral_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **9. `overturn_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN overturned_ind = 1 AND app_reverse_ind = 1 THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **10. `md_denial_rate_of_total`**
- **Description:** The rate of MD denials as a percentage of all cases in the cohort.
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(CASE WHEN final_denied_ind = 1 AND LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END), COUNT(DISTINCT pme_reference_no))
  ```

### **11. `md_denial_plus_overturn_rate`**
- **Description:** A combined rate of cases that were either denied by an MD or were later overturned on appeal.
- **Formula:**
  ```sql
  SAFE_DIVIDE(
      (SUM(CASE WHEN final_denied_ind = 1 AND LOWER(reviewer_ir) = 'md' THEN 1 ELSE 0 END) + 
       SUM(CASE WHEN overturned_ind = 1 AND app_reverse_ind = 1 THEN 1 ELSE 0 END)),
      COUNT(DISTINCT pme_reference_no)
  )
  ```

### **12. `um_exempt_admit_rate`**
- **Formula:**
  ```sql
  SAFE_DIVIDE(SUM(prvdr_um_exempt_ind), COUNT(DISTINCT pme_reference_no))
  ```

---


