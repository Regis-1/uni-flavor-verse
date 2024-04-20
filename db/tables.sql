-- UZYTKOWNIK
create table Uzytkownik(
    id serial PRIMARY KEY, -- primary key
    nazwa_uzytkownika varchar(64) not null,
    haslo varchar(64) not null -- SHA256 hashed password
);

-- PRZEPIS
create table Przepis(
    id serial PRIMARY KEY, -- primary key
    nazwa varchar(128) not null,
    opis varchar(1024),
    poziom_trudnosci integer not null,
    procedura_wykonania varchar(1024) not null,
    kalorycznosc integer
);

-- SKLADNIK
create table Skladnik(
    id serial PRIMARY KEY, -- primary key
    nazwa varchar(128) not null
);

-- UZYTKOWNIK_PRZEPISY
create table Uzytkownik_przepisy(
    id serial PRIMARY KEY, -- primary key
    uzytkownik integer not null, -- foreign key
    przepis integer not null -- foreign key
);

alter table Uzytkownik_przepisy add constraint uzytkownik_fk
    foreign key (uzytkownik) references Uzytkownik(id) on delete cascade;

alter table Uzytkownik_przepisy add constraint przepis_fk
    foreign key (przepis) references Przepis(id) on delete cascade;

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
copy Uzytkownik from '/db_data/uzytkownicy.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Skladnik from '/db_data/skladniki.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Przepis from '/db_data/przepisy.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Uzytkownik_przepisy from '/db_data/uzytkownik_przepisy.csv' with (format CSV, delimiter ',', quote '"', header true);
copy Przepis_skladniki from '/db_data/przepis_skladniki.csv' with (format CSV, delimiter ',', quote '"', header true);
