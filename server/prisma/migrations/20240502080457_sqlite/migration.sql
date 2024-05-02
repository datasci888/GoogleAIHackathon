-- CreateTable
CREATE TABLE "ERVisit" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "userId" TEXT,
    CONSTRAINT "ERVisit_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "ERPatientRecord" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "age" TEXT,
    "arrivalMode" TEXT,
    "injury" TEXT,
    "chiefComplaint" TEXT,
    "mentalState" TEXT,
    "painIntensity" TEXT,
    "bloodPressure" TEXT,
    "heartRate" TEXT,
    "respiratoryRate" TEXT,
    "bodyTemperature" TEXT,
    "oxygenSaturation" TEXT,
    "erVisitId" TEXT NOT NULL,
    "triageColour" TEXT,
    CONSTRAINT "ERPatientRecord_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "ChatMessage" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "raw" TEXT NOT NULL,
    "erVisitId" TEXT,
    "userId" TEXT,
    CONSTRAINT "ChatMessage_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "ChatMessage_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "name" TEXT,
    "patientId" TEXT,
    "triageScore" INTEGER
);

-- CreateIndex
CREATE UNIQUE INDEX "ERPatientRecord_erVisitId_key" ON "ERPatientRecord"("erVisitId");

-- CreateIndex
CREATE INDEX "ERPatientRecord_erVisitId_idx" ON "ERPatientRecord"("erVisitId");

-- CreateIndex
CREATE INDEX "ChatMessage_erVisitId_idx" ON "ChatMessage"("erVisitId");

-- CreateIndex
CREATE UNIQUE INDEX "User_patientId_key" ON "User"("patientId");
