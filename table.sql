CREATE TABLE IF NOT EXISTS gorod (
    id_gorod SERIAL PRIMARY KEY,
    href TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS institutes (
    id_institutes SERIAL PRIMARY KEY,
    id_gorod INTEGER,
    full_name TEXT,
    name_small TEXT,
    href TEXT,
    FOREIGN KEY (id_gorod) REFERENCES gorod(id_gorod)
);

CREATE TABLE IF NOT EXISTS directions (
    id_directions SERIAL PRIMARY KEY,
    id_institutes INTEGER,
    fac text,
    direction text,
    level_program text,
    code_program text,
    profile_program text,
    form_study text,
    FOREIGN KEY (id_institutes) REFERENCES institutes(id_institutes)
);



CREATE TABLE IF NOT EXISTS ball (
    id_ball SERIAL PRIMARY KEY,
    ball TEXT,
    year INTEGER,
    id_directions INTEGER,
    FOREIGN KEY (id_directions) REFERENCES directions(id_directions)
);

CREATE TABLE IF NOT EXISTS exam (
    id_exam SERIAL PRIMARY KEY,
    id_directions INTEGER,
    exam TEXT,
    view TEXT,
    FOREIGN KEY (id_directions) REFERENCES directions(id_directions)
);


