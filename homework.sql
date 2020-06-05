PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS task ;
CREATE TABLE task(
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    name TEXT NOT NULL,
    status INTEGER DEFAULT 0 NOT NULL CHECK(status in(0,1))
);
INSERT INTO task VALUES(1,'走路',0);
INSERT INTO task VALUES(2,'shopping',1);
INSERT INTO task VALUES(3,'surf',0);
INSERT INTO task VALUES(4,'搭車',0);
INSERT INTO task VALUES(5,'play ball',0);
INSERT INTO task VALUES(6,'跑步',0);
INSERT INTO task VALUES(7,'買中餐',0);
INSERT INTO task VALUES(8,'WORK_TIME',1);
INSERT INTO task VALUES(9,'sleep',1);
INSERT INTO task VALUES(10,'run',0);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('task',11);
COMMIT;
