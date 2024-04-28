/*
  Warnings:

  - You are about to drop the column `content` on the `ChatMessage` table. All the data in the column will be lost.
  - You are about to drop the column `metadata` on the `ChatMessage` table. All the data in the column will be lost.
  - You are about to drop the column `role` on the `ChatMessage` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "ChatMessage" DROP COLUMN "content",
DROP COLUMN "metadata",
DROP COLUMN "role",
ADD COLUMN     "raw" TEXT;
