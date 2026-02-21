# config_engine.py

def suggest_config(answers):
    job = answers.get("job")
    software = answers.get("software")
    strategy = answers.get("strategy")

    level = 1  # 1 low | 2 medium | 3 high

    # 🔥 HARD FILTER — تعیین حداقل سطح لازم

    if job == "مهندسی" or software in ["رندر", "AI"]:
        level = 3
    elif job in ["دانشجویی", "اداری"]:
        level = 2
    else:
        level = 1

    # 🔥 اثر استراتژی خرید
    if strategy == "اقتصادی":
        level = max(1, level - 1)
    elif strategy == "آینده‌نگر":
        level = min(3, level + 1)

    # 🔥 CPU (بدون گزینه نامناسب)

    if level == 1:
        cpu = "Intel i3 / Ryzen 3 (سری U)"
    elif level == 2:
        cpu = "Intel i5 / Ryzen 5 (سری U/G)"
    else:
        cpu = "Intel i7 / Ryzen 7 (سری H)"

    # 🔥 GPU

    if level == 3:
        gpu = "گرافیک مجزا (RTX)"
    elif software in ["رندر", "AI", "گرافیک"]:
        gpu = "گرافیک مجزا (MX / RTX)"
    else:
        gpu = "گرافیک مجتمع (Iris Xe / Radeon)"

    # 🔥 RAM

    ram_map = {
        1: "8GB",
        2: "16GB",
        3: "32GB"
    }

    # 🔥 Storage

    storage_map = {
        1: "256GB SSD",
        2: "512GB SSD",
        3: "1TB SSD"
    }

    return {
        "cpu": cpu,
        "ram": ram_map[level],
        "storage": storage_map[level],
        "gpu": gpu
    }
