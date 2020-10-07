from faker import Faker
from random import choice
from RPA.Excel.Files import Files

good_feedback = [
    "Item was of good quality! Fantastic delivery. Notably magnificent packaging. A++!",
    "Item was of first-class quality. Great delivery. Packaging was high-standard. A++",
    "Item was of the most superb quality. Good packaging. Ever so swift delivery. A+++",
    "Item is of splendid quality! Delivery was very, very fast. Superior packaging. A+",
    "The item was first-rate and first-class! Superb packaging. Delivery was good. A+!",
    "Item superior. Quality of the wrapping was fantastic. Speedy to send. Thanks. A++",
    "Item is of excellent quality! Very wonderful packaging. First-class delivery. A++",
    "The item was great and good. Outstanding packaging. Very excellent delivery. A++!",
    "Quality of item was super! Wonderful packaging. Very, very splendid delivery. A++",
    "Good quality! Immensely lovely packaging. Quick delivery. Excellent service. A+++",
]
bad_feedback = [
    "Bad quality. Plain packaging. Delivery was remarkably sluggish. Shoddy seller. D-",
    "Item terrible! Delivery was appalling. Packaging was dreadful. Shoddy service. E-",
    "Item shoddy! Appalling packaging. Late to send. Seller is terrible and awful. F-!",
    "Item horrendous! Slow to send. Awful packaging. Seller is bad and horrendous. D-!",
    "Item horrible! Terrible packaging. Immensely slow dispatch. Horrendous seller. F-",
    "Item was of terrible quality! The packaging was very appalling. Late to send. F-!",
    "Item was of bad quality! Very, very sluggish dispatch. Packaging was terrible. F-",
    "The item was appalling and horrendous! Ever so late delivery. Awful packaging. D-",
    "Item horrible. Exceptionally awful delivery. Quality of the wrapping was bad. D-!",
    "Item was of the most shoddy quality. Packaging was dreadful. Delivery was bad. F-",
]

neutral_feedback = [
    "The item was middling and passable. Unremarkable packaging. Middling delivery. C-",
    "Item fairish. Packaging was moderate. Middling delivery. Might buy from again. C-",
    "The item was middling and acceptable. Typical to send. Packaging was passable. C-",
    "Quality of item was passable. Tolerable delivery. Immensely artless packaging. B-",
    "The item was fairish. Very, very typical delivery. Packaging was ordinary. Eh. B-",
    "Quality of item was reasonable. Unremarkable packaging. Very fairish delivery. B-",
    "Item was of the most middling quality. Tolerable delivery. Passable packaging. B-",
    "Reasonable quality. Fair packaging. Typical delivery. Everyone is so ordinary. C+",
    "Item fairish. Packaging was moderate. Passable delivery. Might buy from again. C+",
    "Average quality. Simple packaging. Very tolerable delivery. Seller is fairish. D+",
]


def generate_data(user_count=100, feedback_count=5):
    fake = Faker()
    files = Files()

    files.create_workbook("userdata.xlsx")
    files.create_worksheet("profile", exist_ok=True)
    files.create_worksheet("feedback", exist_ok=True)

    users = []
    names = []
    for i in range(user_count):
        userprofile = fake.profile()
        if userprofile["name"] in names:
            print("name %s already exists", userprofile["name"])
            continue
        userprofile.pop("website")
        userprofile.pop("current_location")
        files.append_rows_to_worksheet(userprofile, "profile", header=True)
        users.append(userprofile)

    for i in range(1, 16):
        selected_user = users[i]
        feedback = {"name": selected_user["name"], "feedback": choice(good_feedback)}
        print(feedback)
        files.append_rows_to_worksheet(feedback, "feedback", header=True)

    for i in range(17, 22):
        selected_user = users[i]
        feedback = {"name": selected_user["name"], "feedback": choice(neutral_feedback)}
        print(feedback)
        files.append_rows_to_worksheet(feedback, "feedback", header=True)

    for i in range(23, 28):
        selected_user = users[i]
        feedback = {"name": selected_user["name"], "feedback": choice(bad_feedback)}
        print(feedback)
        files.append_rows_to_worksheet(feedback, "feedback", header=True)

    files.remove_worksheet("Sheet")
    files.save_workbook()


if __name__ == "__main__":
    generate_data()
