# config_engine.py

def suggest_config(answers):
    level = 1  # 1=low, 2=medium, 3=high

    job = answers.get("job")
    software = answers.get("software")
    strategy = answers.get("strategy")

    # سطح بر اساس کاربری
    if job in ["مهندسی", "طراحی"]:
        level = 3
    elif job in ["دانشجویی", "اداری"]:
        level = 2
    else:
        level = 1

    # اثر نرم افزار
    if software in ["رندر", "AI"]:
        level = max(level, 3)

    # اثر استراتژی خرید
    if strategy == "اقتصادی":
        level = max(1, level - 1)
    elif strategy == "آینده‌نگر":
        level = min(3, level + 1)

    # CPU
    cpu_map = {
        1: "Intel i3 / Ryzen 3 (سری U)",
        2: "Intel i5 / Ryzen 5 (سری U/G)",
        3: "Intel i7 / Ryzen 7 (سری H)"
    }

    # RAM
    ram_map = {
        1: "8GB",
        2: "16GB",
        3: "32GB"
    }

    # Storage
    storage_map = {
        1: "256GB SSD",
        2: "512GB SSD",
        3: "1TB SSD"
    }

    # GPU
    if software in ["رندر", "AI", "گرافیک"]:
        gpu = "گرافیک مجزا (RTX / MX)"
    else:
        gpu = "گرافیک مجتمع (Iris Xe / Radeon)"

    return {
        "cpu": cpu_map[level],
        "ram": ram_map[level],
        "storage": storage_map[level],
        "gpu": gpu
    }