CREATE DATABASE IF NOT EXISTS daily_tracker ;
USE daily_tracker;

CREATE TABLE habits(
    habit_id INT PRIMARY KEY AUTO_INCREMENT,
    habit_name varchar(50) NOT NULL,
    created_at DATE NOT NULL DEFAULT(CURDATE()),

    UNIQUE KEY uq_habit_name (habit_name)
);

CREATE TABLE notes(
    note_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL DEFAULT(CURDATE()),
    note TEXT NOT NULL
);

CREATE TABLE daily_log(
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL DEFAULT(CURDATE()),
    habit_id INT NOT NULL,
    completed TINYINT(1) NOT NULL,

    UNIQUE KEY uq_habit_date (habit_id,date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);