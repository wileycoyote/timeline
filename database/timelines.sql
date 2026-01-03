PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "meta" (
"timeline" TEXT NOT NULL, 
"requested_order" INTEGER,
"line_type" TEXT,
"colour" TEXT,
PRIMARY KEY ("timeline")
);

CREATE TABLE IF NOT EXISTS "timelines"(
"timeline" TEXT, 
"label" TEXT,
"start" TEXT,
"end" TEXT,
"notes" TEXT,
FOREIGN KEY("timeline") 
REFERENCES meta("timeline")
);
