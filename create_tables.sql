create table base(
id mediumint(11) primary key AUTO_INCREMENT,
bug_id mediumint(6)  not null,
bug_status varchar(64) default null,
changeddate datetime default null,
deadline datetime default null,
summary varchar(500) not null,
ipr_value int(255),
regression varchar(64) not null,
created_date datetime default null,
verified_sw_date datetime default null,
closed_date datetime default null,
val_refuse varchar(64) not null,
priority varchar(64) default null,
function_id int(2) default null,
project_name varchar(50) NOT NULL,
branch varchar(64) not null,
version varchar(64) not null,
homologation varchar(64) not null,
type varchar(30) default null,
resolution varchar(64) default null,
comment_from_cea varchar(255) default null,
reporter_email mediumint(5) default null,
assigner mediumint(5) default null,
swd_assigner mediumint(5) default null,
time_bugstatus datetime default null,
bug_commenttime datetime default null,
refused_date datetime default null,
regression_date datetime default null,
new_date datetime default null,
assigned_date datetime default NULL,
resolver mediumint(5) default null,
long_text_read_only mediumint(5) default null,
comments varchar(10000) default null
)ENGINE=InnoDB;

create table project_static(
project_name varchar(50) NOT NULL,
date date not null,
total int(4) DEFAULT NULL,
open int(4) DEFAULT NULL,
fixed int(4) DEFAULT NULL,
regression int(4) DEFAULT NULL,
id mediumint(11) NOT NULL primary key AUTO_INCREMENT
)ENGINE=InnoDB;

create table function_static(
function_id int(2) not null,
date date not null,
total mediumint(3) not null,
open int(4) DEFAULT NULL,
fixed int(4) DEFAULT NULL,
regression int(4) DEFAULT NULL,
project_name varchar(50) NOT NULL
)ENGINE=InnoDB;

create table team_static(
team_id int(2) not null,
date date not null,
P0_open int(4) DEFAULT NULL,
P0_fixed int(4) DEFAULT NULL,
P0_regression int(4) DEFAULT NULL,
P1_open int(4) DEFAULT NULL,
P1_fixed int(4) DEFAULT NULL,
P1_regression int(4) DEFAULT NULL,
project_name varchar(50) NOT NULL
)ENGINE=InnoDB;

create table bugusers(
id mediumint(5) primary key AUTO_INCREMENT,
email varchar(50) not null,
name varchar(20) not null,
site varchar(2) not null,
section varchar(20) not null,
team_id int(3) not null,
department varchar(20) not null
)ENGINE=InnoDB;

create table team(
team_id int(3) primary key AUTO_INCREMENT,
team varchar(20) not null
)ENGINE=InnoDB;

create table special(
bug_id mediumint(6) primary key,
special_id smallint(6),
delay varchar(20) not null,
regression char(1) not null,
refuse char(1) not null,
today_noresponse char(1)
)ENGINE=InnoDB;

create table project_list(
project_id smallint(6) primary key AUTO_INCREMENT,
branch varchar(40) not null,
project varchar(10) not null,
down char(1) not null default "N"
)ENGINE=InnoDB;

create table function(
function_id int(3) primary key AUTO_INCREMENT,
function_name varchar(50) not null
)ENGINE=InnoDB;

create table old_base like base;

create table project_status(
`project_name` varchar(50) not null,
dr0 date DEFAULT NULL,
dr1 date DEFAULT NULL,
dr2 date DEFAULT NULL,
dr3 date DEFAULT NULL,
fsr date DEFAULT NULL,
dr4 date not null
)ENGINE=InnoDB;

create table person_static(
id mediumint(11) primary key AUTO_INCREMENT,
user_id mediumint(5) not null,
section varchar(20) not null,
P0_open int(4) DEFAULT NULL,
P1_open int(4) DEFAULT NULL,
P0_fixed int(4) DEFAULT NULL,
P1_fixed int(4) DEFAULT NULL,
P0_regression int(4) DEFAULT NULL,
P1_regression int(4) DEFAULT NULL,
project_name varchar(50) NOT NULL,
date date not null,
daily_open int(4) DEFAULT NULL,
daily_fix int(4) DEFAULT NULL
)ENGINE=InnoDB;


'''This is dep_teamstatic table, person\'s static record in this table'''
create table dep_weekly_person(
id mediumint(5) primary key AUTO_INCREMENT,
user_id mediumint(5) not null,
section varchar(20) not null,
open_total int(4) DEFAULT NULL,
saturday_open_total int(4) DEFAULT NULL,
open int(4) DEFAULT NULL,
fix int(4) DEFAULT NULL,
ref_reg int(4) DEFAULT NULL,
project_name varchar(50) NOT NULL,
date date not null,
weeks varchar(10) not null
)ENGINE=InnoDB;


'''This is task_FR_relationship table'''
create table task_FR_relationship(
task_number int(20) not null unique,
FR_number int(20) default NULL
)ENGINE=InnoDB;


DELIMITER //
DROP PROCEDURE IF EXISTS import_buginfo;
CREATE PROCEDURE import_buginfo(IN closed_date datetime, IN bug_id mediumint(6), IN comment_from_cea varchar(255), 
IN type varchar(30), IN assigner_email varchar(30), IN bug_status varchar(64), IN changeddate datetime, IN summary varchar(500), 
IN ipr_value int(255), IN deadline datetime, IN branch varchar(64), IN created_date datetime, IN verified_sw_date datetime, IN reporter_email varchar(30), 
IN function varchar(30), IN resolution varchar(64), IN regression varchar(64), IN val_refuse varchar(64), 
IN priority varchar(64), IN version varchar(64), IN homologation varchar(64),IN refused_date datetime, 
IN regression_date datetime, IN new_date datetime, IN project_name varchar(50), IN assigned_date datetime, 
IN resolver varchar(30), IN long_text_read_only varchar(30), IN comments varchar(10000), IN isCR varchar(10))
BEGIN
declare functions_id int(3) DEFAULT 1;
declare reporter_id mediumint(5) DEFAULT 199;
declare assigner_id mediumint(5) DEFAULT 199;
declare resolver_id mediumint(5) DEFAULT 199;
declare long_text_read_only_id mediumint(5) DEFAULT 199;

select function_id into functions_id from function where function_name=function;
select id into reporter_id from bugusers where email=reporter_email;
select id into assigner_id from bugusers where email=assigner_email;
select id into resolver_id from bugusers where email=resolver;
select id into long_text_read_only_id from bugusers where email=long_text_read_only;

replace into base(closed_date,bug_id,comment_from_cea,type,assigner,bug_status,changeddate,summary,
ipr_value,deadline,branch,created_date,verified_sw_date,reporter_email,function_id,resolution,regression,
val_refuse,priority,version,homologation,refused_date,regression_date,new_date,project_name,assigned_date,
resolver,long_text_read_only,comments,isCR) 
values(closed_date,bug_id,comment_from_cea,type,
assigner_id,bug_status,changeddate,summary,ipr_value,deadline,branch,created_date,verified_sw_date,
reporter_id,functions_id,resolution,regression,val_refuse,priority,version,homologation,refused_date,
regression_date,new_date,project_name,assigned_date,resolver_id,long_text_read_only_id,comments,isCR);
commit;
END //  
DELIMITER ;
