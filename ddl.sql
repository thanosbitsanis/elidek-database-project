SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS ELIDEK;
CREATE SCHEMA ELIDEK;
USE ELIDEK;

CREATE TABLE Elidek_program (
    program_name VARCHAR(50) NOT NULL,
    program_address VARCHAR(50) NOT NULL,
    PRIMARY KEY (program_name)
);

CREATE TABLE Scientific_field (
    field_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(field_name)
);

CREATE TABLE Staff (
    staff_id INT UNSIGNED NOT NULL,
    staff_name VARCHAR(50),
    PRIMARY KEY (staff_id)
);

CREATE TABLE Organization (
    org_name VARCHAR(50) NOT NULL,
    org_zip VARCHAR(50) NOT NULL,
    org_address VARCHAR(50) NOT NULL,
    org_city VARCHAR(50) NOT NULL,
    org_abbreviation VARCHAR(50) NOT NULL,
    PRIMARY KEY (org_name)
);

CREATE TABLE Evaluation (
    evaluation_id INT UNSIGNED NOT NULL,
    evaluation_grade INT UNSIGNED NOT NULL,
    evaluation_date  DATE NOT NULL,
    PRIMARY KEY (evaluation_id)
);

CREATE TABLE Researcher (
    researcher_id VARCHAR(50) NOT NULL,
    researcher_name VARCHAR(50) NOT NULL,
    researcher_lastname VARCHAR(50) NOT NULL,
    researcher_birthdate  DATE NOT NULL,
    researcher_gender VARCHAR(50) NOT NULL,
    org_name VARCHAR(50) NOT NULL,
    hire_date  DATE NOT NULL,
    PRIMARY KEY (researcher_id, org_name),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE
);

    CREATE INDEX org_name_idx ON Researcher(org_name);
    CREATE INDEX researcher_id_idx ON Researcher(researcher_id);

CREATE TABLE Project (
    project_title VARCHAR(50) NOT NULL,
    project_start  DATE NOT NULL,
    project_end  DATE NOT NULL,
    project_budget INT UNSIGNED NOT NULL,
    staff_id INT UNSIGNED NOT NULL,
    program_name VARCHAR(50) NOT NULL,
    evaluation_id INT UNSIGNED NOT NULL,
    researcher_id VARCHAR(50) NOT NULL,
    org_name VARCHAR(50) NOT NULL,
    head_researcher VARCHAR(50) NOT NULL,
    project_summary VARCHAR(500) NOT NULL,
    duration SMALLINT AS (TIMESTAMPDIFF(YEAR, project_start, project_end)),
    PRIMARY KEY (project_title),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (program_name) REFERENCES Elidek_program(program_name) ON DELETE RESTRICT ON UPDATE CASCADE, 
    FOREIGN KEY (evaluation_id) REFERENCES Evaluation(evaluation_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
    FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (head_researcher) REFERENCES Researcher(researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
    CREATE INDEX staff_id_idx ON Project(staff_id);
    CREATE INDEX researcher_id_idx ON Project(researcher_id);
    CREATE INDEX org_name_idx ON Project(org_name);


CREATE TABLE Manages (
    org_name VARCHAR(50) NOT NULL,
    project_title VARCHAR(50) NOT NULL,
    PRIMARY KEY (org_name, project_title),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (project_title) REFERENCES Project(project_title) ON DELETE RESTRICT ON UPDATE CASCADE
);

    CREATE INDEX org_name_idx ON Manages(org_name);
    CREATE INDEX project_title_idx ON Manages(project_title);

CREATE TABLE Field_of_project (
    field_name VARCHAR(50) NOT NULL,
    project_title VARCHAR(50) NOT NULL,
    PRIMARY KEY (field_name, project_title),
    FOREIGN KEY (field_name) REFERENCES Scientific_field(field_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (project_title) REFERENCES Project(project_title) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX field_name_idx ON Field_of_project(field_name);
    CREATE INDEX project_title_idx ON Field_of_project(project_title);


CREATE TABLE Deliverables (
    project_title VARCHAR(50) NOT NULL,
    deliverable_title VARCHAR(50) NOT NULL,
    summary VARCHAR(500) NOT NULL,
    delivery_date  DATE NOT NULL,
    PRIMARY KEY (deliverable_title, project_title),
    FOREIGN KEY (project_title) REFERENCES Project(project_title) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX project_title_idx ON Deliverables(project_title);



CREATE TABLE Evaluates (
    evaluation_id INT UNSIGNED NOT NULL,
    researcher_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (evaluation_id, researcher_id),
    FOREIGN KEY (evaluation_id) REFERENCES Evaluation(evaluation_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

    CREATE INDEX researcher_id_idx ON Evaluates(researcher_id);

CREATE TABLE Works_for (
    project_title VARCHAR(50) NOT NULL,
    researcher_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (project_title, researcher_id),
    FOREIGN KEY (project_title) REFERENCES Project(project_title) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX project_title_idx ON Works_for(project_title);
    CREATE INDEX researcher_id_idx ON Works_for(researcher_id);


CREATE TABLE Telephones (
    org_name VARCHAR(50) NOT NULL,
    telephone_numbers VARCHAR(50) NOT NULL,
    PRIMARY KEY (org_name, telephone_numbers),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX org_name_idx ON Telephones(org_name);


CREATE TABLE Company (
    company_funds INT UNSIGNED NOT NULL,
    org_name VARCHAR(50),
    PRIMARY KEY (org_name),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE
);

    CREATE INDEX org_name_idx ON Company(org_name);


CREATE TABLE University (
    university_funds INT UNSIGNED NOT NULL,
    org_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (org_name),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX org_name_idx ON University(org_name);


CREATE TABLE Research_Center (
    center_publicfunds INT UNSIGNED NOT NULL,
    center_privatefunds INT UNSIGNED NOT NULL,
    org_name VARCHAR(50),
    PRIMARY KEY (org_name),
    FOREIGN KEY (org_name) REFERENCES Organization(org_name) ON DELETE RESTRICT ON UPDATE CASCADE
);


    CREATE INDEX org_name_idx ON Research_Center(org_name);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;