create table todo
(
    id   serial  not null
        constraint todo_pkey
            primary key,
    task varchar not null
);
