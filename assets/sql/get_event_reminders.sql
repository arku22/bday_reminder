SELECT
	to_char(er.event_date, 'MM-DD') AS event_date,
	et.event_type,
	er.associated_person_first_name AS first_name,
	er.associated_person_last_name AS last_name,
	er.addnt_identifier,
	er.event_country_iso_alpha3_code AS country_code
FROM event_reminders AS er
LEFT JOIN event_types AS et
ON er.event_type_id = et.event_type_id
ORDER BY event_date