class Thread:
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.thread = None
        pass

    async def load(self):
        from src.datasources.prisma import prisma

        self.thread = await prisma.thread.find_first(
            where={"User": {""}}
        )

    async def save(self):
        from src.datasources.prisma import prisma

        self.thread = await prisma.thread.update(
            where={"User": {"is": {"patientId": self.patient_id}}},
            data={"Messages":{"set":[]}},
        )

# no need since we use streamlit ?