insert into employees (
  first_name, last_name, contact_info, organization, company, department, position, location, status
)
select
  concat('first_name-', left(md5(floor(random()*10)::text), 5)) as first_name,
  concat('last_name-', left(md5(floor(random()*10)::text), 5)) as last_name,
  concat('contact_info-', left(md5(floor(random()*10)::text), 5)) as contact_info,
  (array['org-a', 'org-b', 'org-c'])[floor(random() * 3 + 1)],
  concat('company-', left(md5(floor(random()*10)::text), 5)) as company,
  concat('department-', left(md5(random()::text), 1)) as department,
  concat('position-', left(md5(random()::text), 2)) as position,
  concat('location-', left(md5(random()::text), 2)) as location,
  floor(random()*3)+1 as status
  from generate_series(1, 1000) s(i);