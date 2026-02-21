def generate_config(answers):
    user_type = answers.get("user_type")
    software = answers.get("software")

    if user_type in ["دانشجویی", "اداری", "خانگی"]:
        return {
            "CPU": "Intel Core i5 U",
            "GPU": "Intel Iris Xe",
            "RAM": "16GB",
            "SSD": "512GB"
        }
    else:
        return {
            "CPU": "Intel Core i7 H",
            "GPU": "NVIDIA RTX",
            "RAM": "32GB",
            "SSD": "1TB"
        }