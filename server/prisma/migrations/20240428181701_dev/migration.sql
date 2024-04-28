/*
  Warnings:

  - Added the required column `raw` to the `ChatMessage` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "ChatMessage" DROP COLUMN "raw",
ADD COLUMN     "raw" BYTEA NOT NULL;
