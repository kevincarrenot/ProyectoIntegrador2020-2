create database liniodb;
use liniodb;

create table producto(
	id_producto int primary key,
    titulo text(100),
    precio text(20)
);


create table reseña (
	id_reseña int primary key,
    reseña text(300),
    estrellas int,
    autor text(100),
    fecha date,
	sentimiento int,
    id_producto int references producto(id_producto)
);

alter table reseña add foreign key(id_producto) references producto(id_producto);
