-- PRZEPIS
create table Przepis(
    id serial PRIMARY KEY, -- primary key
    autor integer not null, -- foreign key
    nazwa varchar(128) not null,
    opis varchar(1024),
    poziom_trudnosci integer not null,
    procedura_wykonania varchar(1024) not null,
    kalorycznosc integer,
    obraz text
);

-- SKLADNIK
create table Skladnik(
    id serial PRIMARY KEY, -- primary key
    nazwa varchar(128) not null
);

-- PRZEPIS_SKLADNIKI
create table Przepis_skladniki(
    id serial PRIMARY KEY, -- primary key
    przepis integer not null, -- foreign key
    skladnik integer not null, -- foreign key
    ilosc integer not null,
    miara varchar(32) not null
);

alter table Przepis_skladniki add constraint przepis_fk
    foreign key (przepis) references Przepis(id) on delete cascade;

alter table Przepis_skladniki add constraint skladnik_fk
    foreign key (skladnik) references Skladnik(id) on delete cascade;

-- LOADING DATA
copy Skladnik(nazwa) from '/db_data/skladniki.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Przepis(autor,nazwa,opis,poziom_trudnosci,procedura_wykonania,kalorycznosc,obraz) from '/db_data/przepisy.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Przepis_skladniki(przepis,skladnik,ilosc,miara) from '/db_data/przepis_skladniki.csv' with (format CSV, delimiter ',', quote '"', header true);
