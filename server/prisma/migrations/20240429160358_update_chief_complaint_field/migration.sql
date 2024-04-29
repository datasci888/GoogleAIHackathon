/*
  Warnings:

  - You are about to drop the column `cliefComplaint` on the `ERPatientRecord` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "ERPatientRecord" DROP COLUMN "cliefComplaint",
ADD COLUMN     "chiefComplaint" TEXT;
