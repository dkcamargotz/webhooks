CREATE TABLE "users" (
  "uuid" TEXT PRIMARY KEY,
  "name" TEXT,
  "mail" TEXT,
  "confirmed" INTEGER
);

CREATE TABLE "confirmations" (
  "uuid" TEXT PRIMARY KEY,
  "user_id" TEXT,
  "confirmation_code" TEXT,
  "status" TEXT
);
  