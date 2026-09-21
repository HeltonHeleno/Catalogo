import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"C:\Users\helton.helano\Documents\Catalogo"
CORES_DIR = os.path.join(BASE_DIR, "Cores")
OUTPUT_INDIV_DIR = os.path.join(BASE_DIR, "Cores_Com_Nome")
os.makedirs(OUTPUT_INDIV_DIR, exist_ok=True)

# Data definition
COLORS = [
    {"id": "1", "code": "01", "name": "Café com Leite / Areia", "category": "Linha Tradicional", "is_neon": False, "file": "1.jpeg"},
    {"id": "2", "code": "02", "name": "Rosa Bebê", "category": "Linha Tradicional", "is_neon": False, "file": "2.jpeg"},
    {"id": "3", "code": "03", "name": "Salmão", "category": "Linha Tradicional", "is_neon": False, "file": "3.jpeg"},
    {"id": "4", "code": "04", "name": "Amarelo Ouro", "category": "Linha Tradicional", "is_neon": False, "file": "4.jpeg"},
    {"id": "5", "code": "05", "name": "Vermelho", "category": "Linha Tradicional", "is_neon": False, "file": "5.jpeg"},
    {"id": "6", "code": "06", "name": "Cru", "category": "Linha Tradicional", "is_neon": False, "file": "6.jpeg"},
    {"id": "7", "code": "07", "name": "Terra Cota", "category": "Linha Tradicional", "is_neon": False, "file": "7.jpeg"},
    {"id": "8", "code": "08", "name": "Telha", "category": "Linha Tradicional", "is_neon": False, "file": "8.jpeg"},
    {"id": "9", "code": "09", "name": "Caramelo Escuro", "category": "Linha Tradicional", "is_neon": False, "file": "9.jpeg"},
    {"id": "10", "code": "10", "name": "Preto", "category": "Linha Tradicional", "is_neon": False, "file": "10.jpeg"},
    {"id": "11", "code": "11", "name": "Laranja", "category": "Linha Tradicional", "is_neon": False, "file": "11.jpeg"},
    {"id": "12", "code": "12", "name": "Turquesa", "category": "Linha Tradicional", "is_neon": False, "file": "12.jpeg"},
    {"id": "13", "code": "13", "name": "Verde Musgo", "category": "Linha Tradicional", "is_neon": False, "file": "13.jpeg"},
    {"id": "14", "code": "14", "name": "Lilás", "category": "Linha Tradicional", "is_neon": False, "file": "14.jpeg"},
    {"id": "15", "code": "15", "name": "Pink", "category": "Linha Tradicional", "is_neon": False, "file": "15.jpeg"},
    {"id": "16", "code": "16", "name": "Verde Bandeira", "category": "Linha Tradicional", "is_neon": False, "file": "16.jpeg"},
    {"id": "17", "code": "17", "name": "Chocolate", "category": "Linha Tradicional", "is_neon": False, "file": "17.jpeg"},
    {"id": "1E", "code": "1E", "name": "Laranja Neon", "category": "Cores Especiais • Neon", "is_neon": True, "file": "1E.jpeg"},
    {"id": "2E", "code": "2E", "name": "Amarelo Neon", "category": "Cores Especiais • Neon", "is_neon": True, "file": "2E.jpeg"},
]

# Fonts
FONT_DIR = r"C:\Windows\Fonts"
FONT_SEGOE_REG = os.path.join(FONT_DIR, "segoeui.ttf")
FONT_SEGOE_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")
FONT_SEGOE_SEMIBOLD = os.path.join(FONT_DIR, "segoeuisl.ttf") if os.path.exists(os.path.join(FONT_DIR, "segoeuisl.ttf")) else FONT_SEGOE_REG
FONT_ARIAL_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# -------------------------------------------------------------
# 1. GENERATE INDIVIDUAL LABELED IMAGES
# -------------------------------------------------------------
def generate_individual_images():
    print("Gerando imagens individuais com identificação...")
    font_badge = get_font(FONT_SEGOE_BOLD, 46)
    font_title = get_font(FONT_SEGOE_BOLD, 50)
    font_sub = get_font(FONT_SEGOE_REG, 28)
    font_tag = get_font(FONT_SEGOE_BOLD, 22)

    for item in COLORS:
        src_path = os.path.join(CORES_DIR, item["file"])
        im = Image.open(src_path).convert("RGBA")
        w, h = im.size # 1200, 1600

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        card_margin_x = 45
        card_margin_b = 55
        card_h = 230
        card_top = h - card_margin_b - card_h

        # Card shadow
        shadow_rect = [card_margin_x + 5, card_top + 8, w - card_margin_x + 5, h - card_margin_b + 8]
        draw.rounded_rectangle(shadow_rect, radius=26, fill=(0, 0, 0, 45))

        # Main Card background (subtle acrylic translucent white)
        draw.rounded_rectangle(
            [card_margin_x, card_top, w - card_margin_x, h - card_margin_b],
            radius=26,
            fill=(255, 255, 255, 246),
            outline=(220, 215, 205, 255) if not item["is_neon"] else (255, 120, 30, 255),
            width=3 if not item["is_neon"] else 4
        )

        badge_w = 110
        badge_h = 96
        badge_x = card_margin_x + 35
        badge_y = card_top + (card_h - badge_h) // 2

        if item["is_neon"]:
            # Vibrant Neon Badge
            badge_color = (255, 102, 0, 255) if item["id"] == "1E" else (190, 215, 0, 255)
            badge_text_color = (255, 255, 255, 255) if item["id"] == "1E" else (30, 40, 10, 255)
            draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=badge_color)
        else:
            badge_color = (42, 36, 32, 255)
            badge_text_color = (255, 255, 255, 255)
            draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=badge_color)

        # Center badge text
        bbox = draw.textbbox((0, 0), item["code"], font=font_badge)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((badge_x + (badge_w - tw) // 2, badge_y + (badge_h - th) // 2 - 4), item["code"], fill=badge_text_color, font=font_badge)

        # Text area
        text_x = badge_x + badge_w + 35
        title_y = card_top + 48
        draw.text((text_x, title_y), item["name"], fill=(30, 26, 22), font=font_title)

        sub_y = title_y + 68
        if item["is_neon"]:
            # Special neon tag
            tag_text = "✦ COR ESPECIAL NEON ✦"
            draw.text((text_x, sub_y), tag_text, fill=(230, 80, 0), font=get_font(FONT_SEGOE_BOLD, 30))
        else:
            sub_text = "Catálogo de Barbantes • Linha Tradicional"
            draw.text((text_x, sub_y), sub_text, fill=(135, 120, 108), font=font_sub)

        # Top corner badge
        top_tag_h = 60
        top_tag_w = 340 if item["is_neon"] else 300
        draw.rounded_rectangle(
            [45, 45, 45 + top_tag_w, 45 + top_tag_h],
            radius=16,
            fill=(255, 255, 255, 220),
            outline=(200, 195, 185, 200),
            width=2
        )
        tag_caption = "★ LINHA NEON" if item["is_neon"] else "BARBANTE PREMIUM"
        tbbox = draw.textbbox((0, 0), tag_caption, font=font_tag)
        draw.text((45 + (top_tag_w - (tbbox[2] - tbbox[0])) // 2, 45 + (top_tag_h - (tbbox[3] - tbbox[1])) // 2 - 2), tag_caption, fill=(60, 50, 40), font=font_tag)

        # Merge
        result = Image.alpha_composite(im, overlay).convert("RGB")
        safe_name = item["name"].replace("/", "-").replace(" ", "_")
        filename = f"{item['code']}_{safe_name}.jpg"
        out_file = os.path.join(OUTPUT_INDIV_DIR, filename)
        result.save(out_file, quality=95)
        print(f"Salvo: {filename}")

if __name__ == "__main__":
    generate_individual_images()
