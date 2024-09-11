SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


-- Create table for secrets
CREATE TABLE IF NOT EXISTS public.secrets (
    id varchar(36) DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL,
    active_version int4 DEFAULT 1 NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT secrets_name_key UNIQUE (name),
    CONSTRAINT secrets_pkey PRIMARY KEY (id)
);

-- Create trigger function for secrets
CREATE OR REPLACE FUNCTION public.function_secrets_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$;

-- Create table for secret versions
CREATE TABLE IF NOT EXISTS public.secret_versions (
    id varchar(36) DEFAULT public.uuid_generate_v4() NOT NULL,
    secret_id varchar(36) NOT NULL,
    encrypted_value text NOT NULL,
    encrypted_key text NOT NULL,
    iv text NOT NULL,
    algorithm varchar(255) NOT NULL,
    version int4 DEFAULT 1 NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT secret_versions_pkey PRIMARY KEY (id),
    CONSTRAINT fk_secret_versions_secret_id FOREIGN KEY (secret_id) REFERENCES public.secrets(id)
);

-- Create trigger function for secret_versions
CREATE OR REPLACE FUNCTION public.function_secret_versions_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$;

-- Create trigger for secrets
CREATE TRIGGER trigger_secrets_updated_at
    BEFORE UPDATE ON public.secrets
    FOR EACH ROW
    EXECUTE FUNCTION public.function_secrets_updated_at();

-- Create trigger for secret_versions
CREATE TRIGGER trigger_secret_versions_updated_at
    BEFORE UPDATE ON public.secret_versions
    FOR EACH ROW
    EXECUTE FUNCTION public.function_secret_versions_updated_at();

--
-- PostgreSQL database dump complete
--

