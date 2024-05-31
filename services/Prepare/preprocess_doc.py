# pylint: disable=missing-function-docstring
# 194 disease after counting from the pdf
import PyPDF2
import re

classes_dict = [
    "Apple__black_rot",
    "Apple__healthy",
    "Apple__rust",
    "Apple__scab",
    "Cassava__bacterial_blight",
    "Cassava__brown_streak_disease",
    "Cassava__green_mottle",
    "Cassava__healthy",
    "Cassava__mosaic_disease",
    "Cherry__healthy",
    "Cherry__powdery_mildew",
    "Chili__healthy",
    "Chili__leaf_curl",
    "Chili__leaf_spot",
    "Chili__whitefly",
    "Chili__yellowish",
    "Coffee__cercospora_leaf_spot",
    "Coffee__healthy",
    "Coffee__red_spider_mite",
    "Coffee__rust",
    "Corn__common_rust",
    "Corn__gray_leaf_spot",
    "Corn__healthy",
    "Corn__northern_leaf_blight",
    "Cucumber__diseased",
    "Cucumber__healthy",
    "Gauva__diseased",
    "Gauva__healthy",
    "Grape__black_measles",
    "Grape__black_rot",
    "Grape__healthy",
    "Grape__leaf_blight_(isariopsis_leaf_spot)",
    "Jamun__diseased",
    "Jamun__healthy",
    "Lemon__diseased",
    "Lemon__healthy",
    "Mango__diseased",
    "Mango__healthy",
    "Peach__bacterial_spot",
    "Peach__healthy",
    "Pepper_bell__bacterial_spot",
    "Pepper_bell__healthy",
    "Pomegranate__diseased",
    "Pomegranate__healthy",
    "Potato__early_blight",
    "Potato__healthy",
    "Potato__late_blight",
    "Rice__brown_spot",
    "Rice__healthy",
    "Rice__hispa",
    "Rice__leaf_blast",
    "Rice__neck_blast",
    "Soybean__bacterial_blight",
    "Soybean__caterpillar",
    "Soybean__diabrotica_speciosa",
    "Soybean__downy_mildew",
    "Soybean__healthy",
    "Soybean__mosaic_virus",
    "Soybean__powdery_mildew",
    "Soybean__rust",
    "Soybean__southern_blight",
    "Strawberry___leaf_scorch",
    "Strawberry__healthy",
    "Sugarcane__bacterial_blight",
    "Sugarcane__healthy",
    "Sugarcane__red_rot",
    "Sugarcane__red_stripe",
    "Sugarcane__rust",
    "Tea__algal_leaf",
    "Tea__anthracnose",
    "Tea__bird_eye_spot",
    "Tea__brown_blight",
    "Tea__healthy",
    "Tea__red_leaf_spot",
    "Tomato__bacterial_spot",
    "Tomato__early_blight",
    "Tomato__healthy",
    "Tomato__late_blight",
    "Tomato__leaf_mold",
    "Tomato__mosaic_virus",
    "Tomato__septoria_leaf_spot",
    "Tomato__spider_mites_(two_spotted_spider_mite)",
    "Tomato__target_spot",
    "Tomato__yellow_leaf_curl_virus",
    "Wheat__brown_rust",
    "Wheat__healthy",
    "Wheat__septoria",
    "Wheat__yellow_rust",
]

regex_list = [
    r'figure\s\d+\.\d+\s+.+',
    r'\d+\s+handbook\sof\splant\sdisease\sidentification\sand\smanagement'
]

# this function reades the book and returns the content from it
def read_pdf_text(pdf_path, start_ind, end_ind):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pages = []
        for i, page in enumerate(pdf_reader.pages):
            if i >= start_ind and i <= end_ind: # don't consider useless pages as context pages
                text = page.extract_text().lower()

                for regex in regex_list:
                    text = re.sub(regex, "", text)
            
                pages.append(text.strip())
    

    return pages

def preprocess_content(pdf_content):
    all_pdf = "\n".join(pdf_content)

    # Define the regex pattern for splitting
    disease_pattern = r'\n\d+\.\d+\s+.+\n'

    # Perform the split
    diseases_content = re.split(disease_pattern, all_pdf)
    diseases_title = re.findall(disease_pattern, all_pdf)


    for i in range(1, len(diseases_content)):
        diseases_content[i] = diseases_title[i-1] + diseases_content[i]

    return diseases_content

def get_docs():

    pdf_content = read_pdf_text('./assets/disease_book.pdf', 41, 609)

    diseases = preprocess_content(pdf_content)

    return diseases