/*
  Warnings:

  - You are about to drop the column `erVisit` on the `ChatMessage` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "ChatMessage" DROP CONSTRAINT "ChatMessage_erVisit_fkey";

-- DropIndex
DROP INDEX "ChatMessage_erVisit_idx";

-- AlterTable
ALTER TABLE "ChatMessage" DROP COLUMN "erVisit",
ADD COLUMN     "erVisitId" TEXT;

-- CreateIndex
CREATE INDEX "ChatMessage_erVisitId_idx" ON "ChatMessage"("erVisitId");

-- AddForeignKey
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_erVisitId_fkey" FOREIGN KEY ("erVisitId") REFERENCES "ERVisit"("id") ON DELETE SET NULL ON UPDATE CASCADE;
