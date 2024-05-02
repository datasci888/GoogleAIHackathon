import segno


async def arun(text:str):
    qrcode = segno.make_qr(text)
    # TODO qr for queue