
--postgresql 10

DROP TABLE IF EXISTS applied_filter;

DROP TABLE IF EXISTS picture;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS filter;



create table users (id int8 not null, created_date timestamp, email varchar(255), first_name varchar(255), last_name varchar(255), password varchar(255), phone varchar(255), updated_date timestamp, username varchar(255), primary key (id));

create table picture (id int8 not null, created_date timestamp, img bytea, name varchar(255), updated_date timestamp, user_id int8 not null, primary key (id));

alter table picture add constraint FKsm5vfwexx74npg3319l47fhdi foreign key (user_id) references users;

create table applied_filter (id int8 not null, date timestamp, filter_id int8 not null, picture_id int8 not null, primary key (id));
create table filter (id int8 not null, description text, is_leaner boolean, name varchar(255), primary key (id));
alter table applied_filter add constraint FK5es6qwhmkmgs10kpjika3klum foreign key (filter_id) references filter;
alter table applied_filter add constraint FK9nvi5qabomlnpa7c9hg1jpqip foreign key (picture_id) references picture;
