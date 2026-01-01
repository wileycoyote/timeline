PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "meta" (
"timeline" TEXT primary_key NOT NULL, 
"requested_order" integer,
"line_type" TEXT);

CREATE TABLE IF NOT EXISTS "timelines"(
"timeline" TEXT, 
"label" TEXT,
"start" TEXT,
"end" TEXT,
"notes" TEXT,
FOREIGN KEY("timeline") REFERENCES meta("timeline")
);
