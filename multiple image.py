

import os
from PIL import Image

# === Define your chart folder ===
chart_folder = r"C:\Users\ty10b\Dropbox\CRAFT\7.24.2025 - Finance Forecast\charts"

# === List of chart file names ===
chart_files = [
    "regression_SPY_vs_10Y.png",
    "regression_SPY_vs_ConsumerSentiment.png",
    "regression_SPY_vs_CPI.png",
    "regression_SPY_vs_FedFunds.png",
    "regression_SPY_vs_GDP.png",
    "regression_SPY_vs_M2.png",
    "regression_SPY_vs_Unemployment.png"
]

# === Load images and resize ===
images = [Image.open(os.path.join(chart_folder, f)).resize((500, 350)) for f in chart_files]

# === Arrange into grid ===
cols = 4
rows = (len(images) + cols - 1) // cols
composite_width = cols * 500
composite_height = rows * 350
composite_img = Image.new("RGB", (composite_width, composite_height), "white")

# === Paste images ===
for i, img in enumerate(images):
    x = (i % cols) * 500
    y = (i // cols) * 350
    composite_img.paste(img, (x, y))

# === Save output ===
output_path = os.path.join(chart_folder, "SPY_vs_Macro_Composite.png")
composite_img.save(output_path)
print(f"✅ Composite saved to: {output_path}")





