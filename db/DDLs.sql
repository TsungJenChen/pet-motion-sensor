create schema cat;


DROP TABLE IF EXISTS cat.toilet;
create table cat.toilet (
id SERIAL PRIMARY KEY,
in_time timestamp,
out_time timestamp,
duration interval,
pee_or_poop varchar(255),
litter_box_id integer,
record_type varchar(2), -- 1 for a normal record, 2 for false triggering
notes varchar(255),
update_time timestamp NOT NULL,
update_user_id varchar(255) NOT NULL,
create_time timestamp NOT NULL,
create_user_id varchar(255) NOT NULL
);