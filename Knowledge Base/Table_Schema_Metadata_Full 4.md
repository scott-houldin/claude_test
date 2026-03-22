# Knowledge Base: `anbc-hcb-dev.provider_ds_hcb_dev.2mn_metrics`

This document provides a detailed overview and data dictionary for the BigQuery table `anbc-hcb-dev.provider_ds_hcb_dev.2mn_metrics`.

## Data Dictionary

Below is the detailed breakdown of all columns in the table, categorized based on the provided data dictionary.

### Case Details

| Column Name | Data Type | Description |
|---|---|---|
| `pme_reference_no` | `INTEGER` | PME reference number for the case |
| `lnitm_sequence_no` | `INTEGER` | Line item number from the TUM Event table corresponding to the case |
| `business_ln_cd` | `STRING` | Line of Business (ME / CP) |
| `business_ln_group_type` | `STRING` | Group type (Medicare DSNP, Medicare SNP - C, Commercial Non-Core - FI, Medicare Group, Commercial Core - SI) for the line of business |
| `funding_type` | `STRING` | Type of Funding - Fully Insured / Self Insured / Unknown |
| `admission_type_desc` | `STRING` | Nature of Admission categorization - Emergent/Urgent, Elective |
| `acute_ind` | `INTEGER` | Indicator for case being acute |
| `stay_srv_type_desc` | `STRING` | Stay service type - Acute / SNF / Rehab / LTAC |
| `aaol_ind` | `INTEGER` | Indicator for AAOL (Avoidable Admission Opportunity List), with two possible values: `0` (No) and `1` (Yes) |
| `cms_ip_only_ind` | `INTEGER` | Indicator for prcoedure on CMS Inpatient Only list |
| `tat` | `INTEGER` | Turn Around Time as the number of days between case creation and initial decision |
| `act_los_day_cnt` | `INTEGER` | For approved cases: Number of days between discharge and admission dates<br>For approved cases without a discharge date: Length of Stay (LOS) authorized |
| `act_los_category` | `STRING` | Length of Stay (LOS) categorization - Short (<=2) and Long |
| `act_los_category_granular` | `STRING` | Length of Stay (LOS) categorization - Medium, Open, Long, Short, Denied, NULL |
| `dschrg_dspstn_cd` | `STRING` | Discharge status code |
| `dschrg_dspstn_short_dscrptn` | `STRING` | Discharge status description - Transfer to SNF, Transfer to Rehab, Home, Benefit Expired, Patient Expired, etc |

### Enrollment Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `enrollment` | `STRING` | Categorization of member enrollment period - New in 2024 / New in 2023/ Existing ) |
| `enrollment_start_mmyy` | `INTEGER` | Month & Year when member became effective as Aetna member |
| `enrollment_latest_mmyy` | `INTEGER` | Latest month and year for member's active Aetna membership |

### Member Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `member_id` | `INTEGER` | Member ID |
| `src_member_id` | `STRING` | Source Member ID |
| `mem_age_nbr` | `INTEGER` | Age of the member |
| `mem_gender_cd` | `STRING` | Gender of the member |
| `cms_cntrct_nbr` | `STRING` | H-number for the CMS contract |
| `mem_grp_nbr` | `STRING` | Member group number |
| `mem_grp_nm` | `STRING` | Member group name |
| `mem_local_mkt_cd` | `STRING` | Code for local market |
| `mem_local_mkt_short_nm` | `STRING` | Local market name |
| `mem_lm_reg_dsply_nm` | `STRING` | Region name |
| `mem_state_postal_cd` | `STRING` | Abbreviation for State |

### Provider Metrics (from Auth)

| Column Name | Data Type | Description |
|---|---|---|
| `src_prvdr_id` | `INTEGER` | EPDB Provider ID |
| `prim_fac_prvdr_id` | `INTEGER` | Primary facility provider id |
| `prim_fac_prvdr_nm` | `STRING` | Primary provider facility name |
| `prvdr_system_nm` | `STRING` | Provider system |
| `readm_prvdr_deviation_ind` | `INTEGER` | Indicator for provider in readmission provider deviation list |
| `prvdr_um_exempt_ind` | `INTEGER` | Indicator for provider in UM exempt list, provider with 1 means they always get approved. |

### Case Journey Timeline Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `orig_create_dt` | `DATE` | Case creation date |
| `year` | `INTEGER` | Year based on the case creation date |
| `month` | `INTEGER` | Month based on the case creation date |
| `week` | `INTEGER` | Week based on the case creation date |
| `actual_admit_dt` | `DATE` | Actual admission date |
| `first_clinical_recd_dt` | `DATE` | Date of receiving the first piece of clinical information |
| `first_adm_rev_dt` | `DATE` | Date of Nurse admission review |
| `first_adm_md_ref_dt` | `DATE` | Date when case referred to MD |
| `first_md_rev_dt` | `DATE` | Date of MD review |
| `decision_eff_dt` | `DATE` | Date of Initial Decision (by Nurse or MD) |
| `last_decision_dt` | `DATE` | Date of Last Decision (after incorporating overturns) |
| `actual_dischg_dt` | `DATE` | Actual discharge date |

### Reviewer Information

| Column Name | Data Type | Description |
|---|---|---|
| `reviewer_all` | `STRING` | Reviewer or Decision Maker - Auto-Approved, Nurse, MD, Other Staff (CMA) |
| `Note_AdmissionReview` | `INTEGER` | Flag for admission review note attached |
| `Note_AdmissionReviewMD` | `INTEGER` | Flag for admission review by MD note attached |

### Decision Reason Metrics (Initial)

| Column Name | Data Type | Description |
|---|---|---|
| `first_dcsn_rsn_ctg_cd` | `STRING` | Code for decision reason category |
| `first_decision_reason_cd` | `STRING` | Code for decision reason |
| `first_decision_rsn_desc` | `STRING` | Decision reason description |
| `first_dcsn_rsn_grp_cd` | `STRING` | Code for decision reason group |
| `first_dcsn_rsn_grp_cd_desc` | `STRING` | Decision reason group description |

### Decision Reason Metrics (Final)

| Column Name | Data Type | Description |
|---|---|---|
| `last_rsn_ctg_cd` | `STRING` | Code for decision reason category |
| `last_reason_cd` | `STRING` | Code for decision reason |
| `last_dcsn_rsn_grp_cd_desc` | `STRING` | Decision reason description |
| `last_rsn_grp_cd` | `STRING` | Code for decision reason group |
| `last_rsn_desc` | `STRING` | Decision reason group description |

### Geographical Metrics (Facility Derived)

| Column Name | Data Type | Description |
|---|---|---|
| `fac_local_mkt_cd` | `STRING` | Code for local market |
| `fac_plan_mkt_short_nm` | `STRING` | Plan market name |
| `fac_emis_reg_long_nm` | `STRING` | Region name |
| `fac_zip_cd` | `STRING` | ZIP code |
| `provider_state_postal_cd` | `STRING` | Abbreviation for State |

### Peer to Peer (P2P) Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `p2p_intake` | `INTEGER` | Indicator for P2P offered |
| `p2p_followed_ind` | `INTEGER` | Indicator for P2P followed upon |
| `p2p_start_dt` | `DATE` | Start Date |
| `p2p_full_denial_ind` | `INTEGER` | Indicator for Full Denial |
| `p2p_partial_denial_ind` | `INTEGER` | Indicator for Partial Denial |
| `p2p_reverse_ind` | `INTEGER` | Indicator for Reversal in decision |
| `p2p_close_dt` | `DATE` | Close Date |
| `p2p_tat` | `INTEGER` | Turn Around Time for P2P |

### Appeal Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `app_intake` | `INTEGER` | Indicator for Appeal received |
| `app_followed_ind` | `INTEGER` | Indicator for Appeal followed upon |
| `app_start_dt` | `DATE` | Start Date |
| `app_full_denial_ind` | `INTEGER` | Indicator for Full Denial |
| `app_partial_denial_ind` | `INTEGER` | Indicator for Partial Denial |
| `app_reverse_ind` | `INTEGER` | Indicator for Reversal in decision |
| `app_close_dt` | `DATE` | Close Date |
| `app_tat` | `INTEGER` | Turn Around Time for Appeal |

### Reconsideration Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `rec_intake` | `INTEGER` | Indicator for Reconsideration received |
| `rec_followed_ind` | `INTEGER` | Indicator for Reconsideration followed upon |
| `rec_start_dt` | `DATE` | Start Date |
| `rec_full_denial_ind` | `INTEGER` | Indicator for Full Denial |
| `rec_partial_denial_ind` | `INTEGER` | Indicator for Partial Denial |
| `rec_reverse_ind` | `INTEGER` | Indicator for Reversal in decision |
| `rec_close_dt` | `DATE` | Close Date |
| `rec_tat` | `INTEGER` | Turn Around Time for Reconsideration |

### Overturn Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `any_p2p_app_rec_ind` | `INTEGER` | Indicator for P2P/Appeal/Reconsideration followed upon |
| `overturned_ind` | `INTEGER` | Indicator for decision overturned (denial to approval) |
| `overturned_p2p_ind` | `INTEGER` | Indicator for P2P overturned |
| `overturned_app_ind` | `INTEGER` | Indicator for Appeal overturned |
| `overturned_rec_ind` | `INTEGER` | Indicator for Reconsideration overturned |

### Diagnosis Metrics (Initial)

| Column Name | Data Type | Description |
|---|---|---|
| `admit_dx_cd` | `STRING` | Diagnosis Code |
| `admit_dx_dscrptn` | `STRING` | Diagnosis Code description |
| `admit_icd9_dx_group_nbr` | `INTEGER` | Diagnosis Group number |
| `admit_icd9_dx_ctg` | `STRING` | Diagnosis Category |
| `admit_icd9dx_ctg_cd` | `INTEGER` | Diagnosis Category Code |
| `admit_icd9_dxgrp_dscrptn` | `STRING` | Diagnosis Group description |

### Diagnosis Metrics (Final)

| Column Name | Data Type | Description |
|---|---|---|
| `prncpl_dx_cd` | `STRING` | Diagnosis Code |
| `prncpl_dx_dscrptn` | `STRING` | Diagnosis Code description |
| `prncpl_icd9_dx_group_nbr` | `INTEGER` | Diagnosis Group number |
| `prncpl_icd9_dx_ctg` | `STRING` | Diagnosis Category |
| `prncpl_icd9dx_ctg_cd` | `INTEGER` | Diagnosis Category Code |
| `prncpl_icd9_dxgrp_dscrptn` | `STRING` | Diagnosis Group description |

### Decision Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `pending_auth_ind` | `INTEGER` | Indicator for a pended case in AUTH |
| `initial_approved_ind` | `INTEGER` | Indicator for case being initially approved |
| `initial_denied_ind` | `INTEGER` | Indicator for case being initially denied |
| `administrative_denial_ind` | `INTEGER` | Indicator for administrative denial (excluding DRG (Continuation of Recent Admission) reason) |
| `clinical_denial_ind` | `INTEGER` | Indicator for clinical denial (including DRG (Continuation of Recent Admission) reason) |
| `final_approved_ind` | `INTEGER` | Indicator for case being finally approved |
| `final_denied_ind` | `INTEGER` | Indicator for case being finally denied |

### Readmission Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `readmission_ind` | `INTEGER` | Indicator for Readmission of the member within 30 days of a prior approved inpatient case (index case) |
| `readmission_linked_um_ind` | `INTEGER` | Indicator for readmission linked by UM Nurse |
| `readmission_linked_pin_dx_ind` | `INTEGER` | Indicator for readmission with matching provider PIN and diagnosis group from index case |
| `index_pme` | `INTEGER` | PME Number for the index case |
| `index_prncpl_icd9_dxgrp_dscrptn` | `STRING` | Diagnosis group (final) for the index case |
| `index_prim_fac_prvdr_id` | `INTEGER` | Primary facility provider ID for index case |
| `index_final_approved_ind` | `INTEGER` | Indicator for initial approval for the index case |

### Avg Cost per Case

| Column Name | Data Type | Description |
|---|---|---|
| `avg_paid_per_case` | `INTEGER` | 2023 Average paid amount for the diagnosis group |

### Claim Metrics

| Column Name | Data Type | Description |
|---|---|---|
| `claim_p_x_ind` | `INTEGER` | Indicator for paid or partially paid claim mapped to the case |
| `medical_case_id` | `INTEGER` | Case ID for the claim |
| `clm_member_id` | `INTEGER` | Member ID in claims data |
| `med_cs_admit_ty_desc` | `STRING` | Admit type for the medical case - Outpatient / Emergency / Urgent / Elective / Newborn / Others |
| `med_case_start_dt` | `DATE` | Case start date from claims data |
| `med_case_stop_dt` | `DATE` | Case end date from claims data |
| `drg_cd_auth` | `STRING` | Diagnosis Related Group code from auth. Very likely, it is differnt from the `clm_drg_cd` value.|
| `clm_icd9_dx_cd` | `STRING` | Diagnosis Code |
| `clm_icd9_dx_group_nbr` | `INTEGER` | Diagnosis Group Number |
| `med_case_pmnt_cd` | `STRING` | Code for claim payment status - `P` Paid, `X` Partial, `D` Deny |
| `med_case_pmnt_desc` | `STRING` | Description for claim payment status - Paid / Partial / Deny|
| `total_billed_amt` | `NUMERIC` | Total billed amount |
| `total_allowed_amt` | `NUMERIC` | Total allowed amount |
| `total_paid_amt` | `NUMERIC` | Total paid amount |

### Provider Metrics (from Claims)

| Column Name | Data Type | Description |
|---|---|---|
| `clm_provider_id` | `INTEGER` | EPDB Provider ID |
| `clm_prim_fac_prvdr_id` | `INTEGER` | Primary facility' provider id |
| `clm_prim_fac_prvdr_nm` | `STRING` | Primary provider facility name |
| `clm_prvdr_system_nm` | `STRING` | Provider system |
| `clm_fac_local_mkt_cd` | `STRING` | Code for local market |
| `clm_fac_plan_mkt_short_nm` | `STRING` | Plan market name |
| `clm_fac_emis_reg_long_nm` | `STRING` | Region name |
| `clm_fac_zip_cd` | `STRING` | ZIP code |
| `clm_provider_state_postal_cd` | `STRING` | Abbreviation for State |

### Other Columns (Not in Provided Dictionary)

This section lists columns present in the BigQuery table schema but not found in the provided CSV data dictionary.

| Column Name | Data Type | Description |
|---|---|---|
| `request_type` | `STRING` | The timing of the authorization request relative to when the service is delivered. Values include 'Pre-Service' (before care), 'Concurrent' (during ongoing care, like a hospital stay), and 'Post-Service' (after care, typically for emergencies). |
| `sa_intake_typ_desc` | `STRING` | Describes the method or channel for the authorization intake (e.g., Fax, EDI, Phone). |
| `admission_type_cd` | `STRING` | Code representing the nature of the admission. Corresponds to `admission_type_desc`. Possible values include: `001`, `002`, `003`, `006`, `007`, `NA`, `U`. |
| `admit_class_cd` | `STRING` | A classification code for the admission, based on acuity. A: Acute, N: Non-Acute, U: Unknown. |
| `nme_ind` | `INTEGER` | Binary indicator; likely flags a specific condition or status for the case. Possible values: `0`, `1`. |
| `stay_srv_type_cd` | `STRING` | Code representing the type of service for the stay. Corresponds to `stay_srv_type_desc`. |
| `stay_srv_type_desc_long` | `STRING` | A more detailed description for the stay service type. |
| `acuity` | `STRING` | Categorizes the clinical acuity level of the case. Possible values: `Acute`, `Non-Acute`, `Behavioural Health`. |
| `admit_subclass` | `STRING` | Sub-classification for the admission type, providing more detail. Possible values include: `ltc` (Long Term Care), `snf` (Skilled Nursing Facility), `reh` (Rehabilitation), `nicu` (Neonatal Intensive Care Unit), `ment` (Mental Health), `subst` (Substance Abuse), `xplnt` (Transplant), `other`. |
| `snp_ind` | `STRING` | Indicator for Special Needs Plan (SNP) enrollment. Possible values: `D` (Dual-Eligible), `I` (Institutional), `C` (Chronic Condition), `N` (Not a SNP member). |
| `case_days_approved` | `INTEGER` | The number of approved days for the case. |
| `case_days_denied` | `INTEGER` | The number of denied days for the case. |
| `case_days` | `INTEGER` | The total number of days requested for the case. |
| `case_admits_approved` | `INTEGER` | Whether the case got the approved admissions. only two values: `0` (No) and `1` (Yes)|
| `case_admits_denied` | `INTEGER` | Whether the case got the denied admissions. only two values: `0` (No) and `1` (Yes)|
| `case_admits` | `INTEGER` | Whether the case got the admissions decisions (case closed or case still open). only two values: `0` (open) and `1` (closed)|
| `min_bed_dt` | `DATE` | The earliest bed date associated with the case. |
| `avoidable_shortstay_los` | `INTEGER` | The length of stay for cases considered an avoidable short stay. |
| `cust_subseg_cd` | `STRING` | Code identifying the member's customer sub-segment or line of business. Usually we don't need to use it as for line of business, we mainly refer to column `business_ln_cd`|
| `pbp_id` | `STRING` | Plan Benefit Package ID, a unique identifier for a specific set of benefits under a Medicare Advantage plan. |
| `plan_id` | `STRING` | Identifier for the member's health insurance plan. |
| `cfo_cd` | `STRING` | Code related to financial organization or cost center. |
| `prod_ctg_cd` | `STRING` | Code for the product category. can be mapped to column `product`|
| `product` | `STRING` | Name or identifier of the insurance product. only two values: `ppo` (Preferred Provider Organization)and `hmo` (Helath Maintenance Organization)|
| `metallic_level_cd` | `STRING` | The metallic tier level of the member's health plan, as defined by the ACA. Possible values: `P` (Platinum), `G` (Gold), `S` (Silver), `B` (Bronze), `C` (Catastrophic), `U` (Unknown). We should avoid use this column as more than 50% of the data has null value in this column. |
| `src` | `STRING` | Data source system. Possible value: `aet`. |
| `dg_cd` | `STRING` | Diagnosis group code. |
| `mdc_cd` | `STRING` | Major Diagnostic Category code. |
| `fund_ctg_cd` | `STRING` | A code representing the funding category of the plan. Corresponds to `funding_type`. |
| `aa_ind` | `INTEGER` | Indicator for whether the case was auto-approved. `1` for yes, `0` for no. |
| `l0_count` | `INTEGER` | A count related to a Level 0 process or review. l0 means the if the request is sent from the provider who is in the gold card list (which shows in each procedure, which provider can be directly auto-approved). |
| `l1_count` | `INTEGER` | A count related to a Level 1 process or review. If the provider failes on both l0 and l2, then the request will go through the l1 predictive model to see whehter the case can be auto-approved or not.|
| `l2_count` | `INTEGER` | A count related to a Level 2 process or review. l2 means if the provider is not the gold card list for that procedure, if he can fill a questionire, we may also auto-approve it based on the questionair.|
| `sr_route_flag` | `STRING` | Flag indicating the outcome of a smart routing process. Possible values: `T1`, `T2`, `T3` , (the 3 tiers are corresponding to if the case can not be approved, how complicated it is, `T1` is the most simple one while `T3` is the most complicated one so for most `T3` cases, we may different rount it to MD and skip the nurse review) `Auto-Approved`, `No Smart Routing`. |
| `sr_denial_probability_rating` | `FLOAT` | A score or rating indicating the probability of denial from the smart routing system. |
| `sr_recommendation` | `STRING` | The recommendation provided by the smart routing system. Possible values: `Approved`, `Review`. |
| `sr_stage` | `STRING` | The authorization stage when smart routing was applied. Possible values: `precert` (Pre-certification), `concurrent` (Concurrent). |
| `not_incurred_ind` | `INTEGER` | Binary indicator, possibly flagging cases where the authorized service was not ultimately incurred. `1` for yes, `0` for no. |
| `mercy_excl_ind` | `INTEGER` | Binary indicator for a 'Mercy' exclusion rule. `1` for excluded, `0` for not. |
| `ca_cap_excl_ind` | `INTEGER` | Binary indicator for a 'CA Capitation' exclusion rule. `1` for excluded, `0` for not. |
| `esrd_mem_ind` | `INTEGER` | Indicator for members with End-Stage Renal Disease (ESRD). `1` for yes, `0` for no. |
| `mbr_identifier_value_id` | `STRING` | An identifier for the member. |
| `dummy_mbr_id_ind` | `STRING` | Indicator for whether the member ID is a dummy or test identifier. `N` means No. |
| `individual_id` | `INTEGER` | A unique identifier for the individual member. |
| `ps_unique_id_orig` | `INTEGER` | Original unique ID from a source system. |
| `ps_unique_id` | `STRING` | Unique ID from a source system. |
| `um_business_program` | `STRING` | The specific Utilization Management (UM) business program associated with the case. Possible values: `UM Markets`, `CCSO`, `CCS`, `A1A`. |
| `mem_zip_cd` | `STRING` | The ZIP code of the member's address. |
| `mem_lm_plan_mkt_cd` | `STRING` | Code for the member's local market plan. |
| `mem_plan_mkt_cd` | `STRING` | Code for the member's plan market. |
| `specialty_ctg_cd` | `STRING` | Code for the provider's specialty category. |
| `dischg_recd_dt` | `DATE` | The date the discharge record was received. |
| `dischg_ind` | `INTEGER` | Indicator for whether the patient has been discharged. `1` for yes, `0` for no. |
| `proxy_completed_ind` | `INTEGER` | Binary indicator for whether a 'proxy' action or task has been completed. `1` for yes, `0` for no. |
| `reviewer` | `STRING` | The clinical role of the person who reviewed the case. This is a simplified version of `reviewer_all`. Possible values: `MD` (Medical Doctor), `Nurse`. |
| `reviewer_ir` | `STRING` | Identifier for the reviewer. |
| `first_md_note` | `DATE` | The date of the first note made by a Medical Doctor. |
| `rvr_tmp` | `STRING` | A temporary field related to the reviewer. |
| `admin_denials_before_md_note` | `INTEGER` | Count of administrative denials before an MD note was added. |
| `adm_review_task_ind` | `INTEGER` | Indicator that an admission review task exists. `1` for yes, `0` for no. |
| `adm_review_nt_ind` | `INTEGER` | Indicator that an admission review note exists. `1` for yes, `0` for no. |
| `first_clinician_task_ind` | `INTEGER` | Indicator that a task was assigned to the first clinician. `1` for yes, `0` for no. |
| `first_cln_user_nm` | `STRING` | Username of the first clinician. |
| `first_cln_first_nm` | `STRING` | First name of the first clinician. |
| `first_cln_last_nm` | `STRING` | Last name of the first clinician. |
| `first_cln_license_txt` | `STRING` | License information for the first clinician. |
| `adm_rev_user_nm` | `STRING` | Username of the admission reviewer. |
| `adm_rev_first_nm` | `STRING` | First name of the admission reviewer. |
| `adm_rev_last_nm` | `STRING` | Last name of the admission reviewer. |
| `adm_rev_license_txt` | `STRING` | License information for the admission reviewer. |
| `md_rev_user_nm` | `STRING` | Username of the MD reviewer. |
| `md_rev_first_nm` | `STRING` | First name of the MD reviewer. |
| `md_rev_last_nm` | `STRING` | Last name of the MD reviewer. |
| `md_rev_license_txt` | `STRING` | License information for the MD reviewer. |
| `plan_mkt_cd` | `STRING` | Code for the plan market. |
| `retro_ind` | `INTEGER` | Indicator for whether the review was conducted retrospectively (after the service was provided). `1` for yes, `0` for no. |
| `event_ind` | `INTEGER` | Event indicator, likely used for counting cases. Appears to be a constant value of `1`. |
| `cob_ind` | `INTEGER` | Indicator for Coordination of Benefits (COB), which applies when a member has coverage from more than one health plan. `1` for yes, `0` for no. |
| `final_administrative_denial_ind` | `INTEGER` | Indicator for whether the case was denied for administrative reasons in the final decision. `1` for yes, `0` for no. |
| `final_clinical_denial_ind` | `INTEGER` | Indicator for whether the case was denied for clinical reasons in the final decision. `1` for yes, `0` for no. |
| `decision_cd` | `STRING` | Code for the initial decision. |
| `last_decision_cd` | `STRING` | Code for the final decision. |
| `approved_drg_readm_ind` | `INTEGER` | Indicator for an approved DRG-related readmission. |
| `med_cs_admit_ty_desc` | `STRING` | Description of the admission type from the medical case (claims) data. |
| `clm_drg_cd` | `STRING` | The DRG code from the claim data. |
| `fac_billed_amt` | `NUMERIC` | The amount billed by the facility. |
| `fac_allowed_amt` | `NUMERIC` | The amount allowed for the facility charges. |
| `fac_paid_amt` | `NUMERIC` | The amount paid to the facility. |
| `file_id` | `STRING` | Identifier for the source file. |
| `admit_yrmo` | `STRING` | The year and month of admission. |
| `jv_org_cd` | `STRING` | Code for a joint venture organization. |
| `deal_org_cd` | `STRING` | Code for a deal-related organization. |
| `deal_org_cd2` | `STRING` | Another code for a deal-related organization. |
| `mkt1_org_cd` | `STRING` | Code for a market organization. |
| `jv_rollup` | `STRING` | A rollup category for joint ventures. |
| `jv_cd` | `STRING` | Code for a joint venture. |
| `newbus_status` | `STRING` | Status of the case related to new business. |
| `pm_note_cat` | `STRING` | Category for provider message notes. |
| `customer` | `STRING` | Name of the customer or group. |
| `ps_cat` | `STRING` | Provider system category. |
| `bed_type_cd_on_admission` | `STRING` | Code for the type of bed on admission. |
| `orig_business_ln_cd` | `STRING` | The original business line code for the member. |
| `orig_cust_subseg_cd` | `STRING` | The original customer sub-segment for the member. |
| `orig_fund_ctg_cd` | `STRING` | The original funding category for the member. |
| `orig_plan_id` | `STRING` | The original plan ID for the member. |
| `orig_mem_lm_plan_mkt_cd` | `STRING` | The original local market plan code for the member. |
| `final_info_denial_ind` | `INTEGER` | Indicator for a final denial due to insufficient information. `1` for yes, `0` for no. |
| `rolling_30_year` | `INTEGER` | The year for a 30-day rolling metric. |
| `rolling_30_lagged_year` | `INTEGER` | The lagged year for a 30-day rolling metric. |
| `rolling_30_fdr_lagged_year` | `INTEGER` | The lagged year for a 30-day rolling FDR metric. |
| `rolling_30_readm_lagged_year` | `INTEGER` | The lagged year for a 30-day rolling readmission metric. |
| `ytd_flag` | `INTEGER` | Flag for Year-To-Date calculations. |
| `ytd_lagged_flag` | `INTEGER` | Flag for lagged Year-To-Date calculations. |
| `ytd_fdr_lagged_flag` | `INTEGER` | Flag for lagged Year-To-Date FDR calculations. |
| `ytd_readm_lagged_flag` | `INTEGER` | Flag for lagged Year-To-Date readmission calculations. |
| `rolling_30_flag` | `INTEGER` | Flag for 30-day rolling calculations. |
| `rolling_30_lagged_flag` | `INTEGER` | Flag for lagged 30-day rolling calculations. |
| `rolling_30_fdr_lagged_flag` | `INTEGER` | Flag for lagged 30-day rolling FDR calculations. |
| `rolling_30_readm_lagged_flag` | `INTEGER` | Flag for lagged 30-day rolling readmission calculations. |
| `onMEU` | `INTEGER` | An indicator related to MEU (Membership Eligibility Unit). |
| `potential_readmission_ind` | `INTEGER` | Indicator for a potential readmission. `1` for yes, `0` for no. |
| `medcompass_potential_readmission_ind` | `INTEGER` | Indicator for a potential readmission identified by the MedCompass system. |
| `readmission_linked_pin_ind` | `INTEGER` | Indicator that a readmission was linked by a provider PIN. |
| `readmission_linked_dx_ind` | `INTEGER` | Indicator that a readmission was linked by diagnosis. |
| `index_orig_create_dt` | `DATE` | The original creation date of the index admission. |
| `index_create_year` | `INTEGER` | The creation year of the index admission. |
| `index_create_month` | `INTEGER` | The creation month of the index admission. |
| `index_actual_admit_dt` | `DATE` | The actual admission date of the index admission. |
| `index_actual_dischg_dt` | `DATE` | The actual discharge date of the index admission. |
| `readm_interval_days` | `INTEGER` | The number of days between the index discharge and the readmission. |
| `index_acute_ind` | `INTEGER` | Indicator for whether the index admission was acute. |
| `index_admission_type_desc` | `STRING` | The admission type description for the index admission. |
| `index_prncpl_dx_cd` | `STRING` | The principal diagnosis code for the index admission. |
| `index_final_denied_ind` | `INTEGER` | Indicator for whether the index admission was finally denied. |


