import sqlite3
import logging

def createDatabase(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE "Matchs" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `timestamp`	INTEGER NOT NULL,
        `babyfoot` NOT NULL REFERENCES Babyfoots(id),
        `duration`	INTEGER NOT NULL,
        `team1`	INTEGER NOT NULL REFERENCES Teams(id),
        `score1` INTEGER NOT NULL,
        `team2`	INTEGER NOT NULL REFERENCES Teams(id),
        `score2` INTEGER NOT NULL
    )''')

    c.execute('''CREATE TABLE "Players" (
        `login` TEXT PRIMARY KEY,
        `fname`	TEXT NOT NULL,
        `lname`	TEXT NOT NULL,
        `elo` INTEGER,
        `private`	INTEGER NOT NULL CHECK(private == 0 or private == 1)
    )''')

    c.execute('''CREATE TABLE "Teams" (
        `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT,
        `player1`	TEXT REFERENCES Players(login),
        `player2`	TEXT REFERENCES Players(login)
    )''')

    c.execute('''CREATE TABLE "Babyfoots" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `location` TEXT
    )
    
    ''')

    c.execute('''CREATE TABLE "Tournaments" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `status` INTEGER NOT NULL CHECK (status>=0 AND status<4),
        `type` INTEGER NOT NULL CHECK (type>=0 AND  type<5)

    )
    
    ''')
    c.execute('''CREATE TABLE "TournamentMatchs" (
        `id` INTEGER PRIMARY KEY REFERENCES Matchs(id),
        `tournament` INTEGER NOT NULL REFERENCES Tournaments(id),
        `round` INTEGER NOT NULL
    )
    
    ''')

    c.execute('''CREATE TABLE "TreeMatchs" (
        `id` INTEGER PRIMARY KEY REFERENCES TournamentMatchs(id),
        `KOType` CHAR(1) NOT NULL CHECK (KOType == 'W' OR KOType=='L'),
        `parent1` INTEGER NOT NULL REFERENCES TreeMatchs(id),
        `parent2` INTEGER NOT NULL REFERENCES TreeMatchs(id)
    )
    
    ''')

    c.execute('''CREATE TABLE "Participate" (
        `team` INTEGER REFERENCES Teams(id),
        `tournament` INTEGER NOT NULL REFERENCES Tournament(id),
        `group` INTEGER
    )
    
    ''')

    c.execute('''CREATE VIEW viewMatchs AS
    SELECT *, CASE WHEN score1>score2 THEN team1 
    WHEN score1<score2 THEN team2 ELSE -1 END AS winningTeam
    FROM Matchs
    ''')

    c.execute("INSERT INTO Babyfoots (location) VALUES ('Fablab')")
    
    
    conn.commit()
    c.close()