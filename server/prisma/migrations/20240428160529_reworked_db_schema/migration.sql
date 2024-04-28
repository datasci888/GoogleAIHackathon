/*
  Warnings:

  - You are about to drop the `Message` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `PatientRecord` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "ERVisit" DROP CONSTRAINT "ERVisit_userId_fkey";

-- DropForeignKey
ALTER TABLE "Message" DROP CONSTRAINT "Message_erVisit_fkey";

-- DropForeignKey
ALTER TABLE "Message" DROP CONSTRAINT "Message_userId_fkey";

-- DropForeignKey
ALTER TABLE "PatientRecord" DROP CONSTRAINT "PatientRecord_userId_fkey";

-- AlterTable
ALTER TABLE "ERVisit" ALTER COLUMN "userId" DROP NOT NULL;

-- DropTable
DROP TABLE "Message";

-- DropTable
DROP TABLE "PatientRecord";

-- CreateTable
CREATE TABLE "ERPatientRecord" (
    "id" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "age" TEXT,
    "arrivalMode" TEXT,
    "injury" TEXT,
    "cliefComplaint" TEXT,
    "mentalState" TEXT,
    "painIntensity" TEXT,
    "bloodPressure" TEXT,
    "heartRate" TEXT,
    "respiratoryRate" TEXT,
    "bodyTemperature" TEXT,
    "oxygenSaturation" TEXT,
    "erVisitId" TEXT NOT NULL,

    CONSTRAINT "ERPatientRecord_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ChatMessage" (
    "id" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "content" TEXT NOT NULL,
    "metadata" TEXT,
    "role" TEXT NOT NULL DEFAULT 'AI',
    "erVisit" TEXT,
    "userId" TEXT,

    CONSTRAINT "ChatMessage_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "ERPatientRecord_erVisitId_key" ON "ERPatientRecord"("erVisitId");

-- AddForeignKey
ALTER TABLE "ERVisit" ADD CONSTRAINT "ERVisit_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ERPatientRecord" ADD CONSTRAINT "ERPatientRecord_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_erVisit_fkey" FOREIGN KEY ("erVisit") REFERENCES "ERVisit"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
