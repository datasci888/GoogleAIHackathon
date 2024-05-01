-- CreateEnum
CREATE TYPE "TriageColour" AS ENUM ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE');

-- AlterTable
ALTER TABLE "ERPatientRecord" ADD COLUMN     "triageColour" "TriageColour";
