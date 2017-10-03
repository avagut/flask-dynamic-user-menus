--Schema to hold menus, users, roles and assignments thereof.
--This would need to be part of the Flask Migrate Deployment Script 
--Including the First User Data Insert Below
--This is to be created as we progress.

CREATE DATABASE my_database_name;
CREATE TABLE nav_menus
(
  menu_id serial NOT NULL,
  menu_url character varying(50) NOT NULL,
  menu_text text NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  created_datetime timestamp without time zone,
  created_by integer,
  last_modified_datetime timestamp without time zone,
  modified_by integer,
  menu_name character varying(80) NOT NULL,
  CONSTRAINT nav_menus_pkey PRIMARY KEY (menu_id),
  CONSTRAINT nav_menus_menu_name_key UNIQUE (menu_name),
  CONSTRAINT nav_menus_menu_url_key UNIQUE (menu_url)
);
CREATE TABLE nav_roles_menus
(
  role_menu_id serial NOT NULL,
  menu_id integer NOT NULL,
  role_id integer NOT NULL,
  can_view boolean NOT NULL DEFAULT true,
  can_create boolean NOT NULL DEFAULT false,
  can_edit boolean NOT NULL DEFAULT false,
  can_delete boolean NOT NULL DEFAULT false,
  is_active boolean NOT NULL DEFAULT true,
  created_by integer,
  created_datetime timestamp without time zone,
  modified_by integer,
  last_modified_datetime timestamp without time zone,
  CONSTRAINT nav_roles_menus_menu_id_fkey FOREIGN KEY (menu_id)
      REFERENCES nav_menus (menu_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT nav_roles_menus_role_id_fkey FOREIGN KEY (role_id)
      REFERENCES sec_roles (role_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE sec_roles
(
  role_id serial NOT NULL,
  role_name character varying(50) NOT NULL,
  role_description character varying(255) NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  created_by integer,
  created_datetime timestamp without time zone,
  modified_by integer,
  last_modified_datetime timestamp without time zone,
  is_default boolean,
  CONSTRAINT sec_roles_pkey PRIMARY KEY (role_id),
  CONSTRAINT sec_roles_role_name_key UNIQUE (role_name)
);
CREATE TABLE sec_users
(
  user_id serial NOT NULL,
  user_name character varying(50) NOT NULL,
  user_password bytea NOT NULL DEFAULT ''::bytea,
  first_name character varying(50) NOT NULL,
  last_name character varying(50) NOT NULL,
  email character varying(255) NOT NULL,
  confirmed_at timestamp without time zone,
  confirmation_sent_at timestamp without time zone,
  is_confirmed boolean NOT NULL DEFAULT false,
  is_active boolean NOT NULL DEFAULT false,
  is_deleted boolean,
  created_datetime timestamp with time zone,
  last_modified_datetime timestamp without time zone,
  has_ever_logged_in boolean NOT NULL DEFAULT false,
  login_datetime timestamp without time zone,
  is_authenticated boolean NOT NULL DEFAULT false,
  created_by integer,
  modified_by integer,
  password_last_change_datetime timestamp without time zone,
  CONSTRAINT sec_users_pkey PRIMARY KEY (user_id),
  CONSTRAINT sec_users_email_key UNIQUE (email),
  CONSTRAINT sec_users_user_name_key UNIQUE (user_name)
);
CREATE TABLE sec_users_roles
(
  user_role_id serial NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  created_by integer,
  created_datetime timestamp without time zone,
  modified_by integer,
  last_modified_datetime timestamp without time zone,
  role_id integer NOT NULL,
  user_id integer NOT NULL,
  CONSTRAINT sec_users_roles_pkey PRIMARY KEY (user_role_id),
  CONSTRAINT sec_users_roles_role_id_fkey FOREIGN KEY (role_id)
      REFERENCES sec_roles (role_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT sec_users_roles_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES sec_users (user_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "UK_state_user_role" UNIQUE (user_role_id)
);

--Your prefered placeHolder data for first time super admin login to 
--access the /users view to then create the users within the app ;
INSERT INTO sec_users(
            user_name, first_name, last_name, email, 
            is_active, created_by)
    VALUES ('start_user', 'Start', 'User', 
            'my_email_address@domain.com', True, 1);





