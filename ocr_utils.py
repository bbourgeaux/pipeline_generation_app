import easyocr

def perform_ocr(image):
    # Create OCR Instance
    reader_en_fr = easyocr.Reader(['en', 'fr'])
    # reader_en_fr = easyocr.Reader(['en', 'fr'], gpu = False)

    def read_text(image_name, model_name, paragraph, canvas_size):
        text = model_name.readtext(image_name, detail=0, paragraph=paragraph, canvas_size=canvas_size)
        return '\n'.join(text)

    ## Extract Text
    texts = read_text(image, reader_en_fr, paragraph=True, canvas_size=2560) # Canvas size: largest size of image

    return texts