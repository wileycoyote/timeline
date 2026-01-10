PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "timelines" (
"timeline" TEXT NOT NULL, 
"requested_order" INTEGER,
"line_type" TEXT,
"colour" TEXT,
"label" TEXT,
PRIMARY KEY ("timeline")
);
-- start and end are ISODATE formats
CREATE TABLE IF NOT EXISTS "events"(
"timeline" TEXT, 
"label" TEXT,
"start" TEXT,
"end" TEXT,
"notes" TEXT,
FOREIGN KEY("timeline") 
REFERENCES timelines("timeline")
);
