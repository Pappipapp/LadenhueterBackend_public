\connect safebuy

CREATE TABLE safebuy.public.markets
(
    market_id character(64) COLLATE pg_catalog."default" NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    latitude float(8) NOT NULL,
    longitude float(8) NOT NULL,
    address character varying(512) NOT NULL,
    CONSTRAINT markets_pkey PRIMARY KEY (market_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.markets
    OWNER to postgres;


CREATE TABLE safebuy.public.reservations
(
    reservation_id character(36) COLLATE pg_catalog."default" NOT NULL,
    market_id character(64) COLLATE pg_catalog."default" NOT NULL,
    user_id character(36) COLLATE pg_catalog."default" NOT NULL,
    start_time timestamp NOT NULL,
    CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id),
    CONSTRAINT markets_fkey FOREIGN KEY (market_id) REFERENCES markets(market_id)

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.reservations
    OWNER to postgres;
