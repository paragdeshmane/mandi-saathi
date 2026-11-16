crops = ["Soybean", "Cotton", "Tur (Arhar)", "Onion", "Turmeric"]

print("Mandi Saathi mein shamil faslein:")

for crop in crops:
    print("-", crop)

chosen_crop = input("Fasal ka naam likho: ").strip().title()

if chosen_crop in crops:
    print("Tumne chuna:", chosen_crop)
else:
    print("Yeh fasal abhi list mein nahi hai.")