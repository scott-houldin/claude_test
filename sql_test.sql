-- Volume and Denial Rate for Inpatient Admits by Acute vs Non-Acute
-- Source: Knowledge Base metric formulas (num_pmes, overall_denial_rate)
-- Required base filters applied: pending_auth_ind = 0, admission_type IN (elective, emergency/urgent)

SELECT
    acuity,
    COUNT(DISTINCT pme_reference_no)                                    AS num_pmes,
    SUM(final_denied_ind)                                               AS denied_pmes,
    SAFE_DIVIDE(SUM(final_denied_ind), COUNT(DISTINCT pme_reference_no)) AS denial_rate
FROM
    `anbc-hcb-dev.provider_ds_hcb_dev.2mn_metrics`
WHERE
    pending_auth_ind = 0
    AND LOWER(admission_type_desc) IN ('elective', 'emergency/urgent')
ORDER BY
    acuity
