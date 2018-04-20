create user hcs_mgr_rw with password 'hcs_mgr_rw';
alter role hcs_mgr_rw set client_encoding to 'utf8';
alter role hcs_mgr_rw set default_transaction_isolation to 'read committed';
alter role hcs_mgr_rw set timezone to 'UTC';
create database hcsmgrdb owner hcs_mgr_rw;
