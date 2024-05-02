-- DropForeignKey
ALTER TABLE "ChatMessage" DROP CONSTRAINT "ChatMessage_erVisitId_fkey";

-- DropForeignKey
ALTER TABLE "ChatMessage" DROP CONSTRAINT "ChatMessage_userId_fkey";

-- DropForeignKey
ALTER TABLE "ERPatientRecord" DROP CONSTRAINT "ERPatientRecord_erVisitId_fkey";

-- DropForeignKey
ALTER TABLE "ERVisit" DROP CONSTRAINT "ERVisit_userId_fkey";

-- AddForeignKey
ALTER TABLE "ERVisit" ADD CONSTRAINT "ERVisit_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ERPatientRecord" ADD CONSTRAINT "ERPatientRecord_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
