drop table if exists urls;
create table urls (
    id integer primary key autoincrement,
    url text not null,
    tiny text null
);
