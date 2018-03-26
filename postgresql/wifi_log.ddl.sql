CREATE TABLE wifi_log (
    mac macaddr not null,
    last_time_seen timestamp with time zone not null,
    power integer,
    record_ts timestamp with time zone default now()
);
