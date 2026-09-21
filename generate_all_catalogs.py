import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"C:\Users\helton.helano\Documents\Catalogo"
CORES_DIR = os.path.join(BASE_DIR, "Cores")
OUTPUT_INDIV_DIR = os.path.join(BASE_DIR, "Cores_Com_Nome")
os.makedirs(OUTPUT_INDIV_DIR, exist_ok=True)

# Cores e Metadados
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
    {"id": "1E", "code": "1E", "name": "Laranja Neon", "category": "Linha Especial Neon", "is_neon": True, "file": "1E.jpeg"},
    {"id": "2E", "code": "2E", "name": "Amarelo Neon", "category": "Linha Especial Neon", "is_neon": True, "file": "2E.jpeg"},
]

FONT_DIR = r"C:\Windows\Fonts"
FONT_SEGOE_REG = os.path.join(FONT_DIR, "segoeui.ttf")
FONT_SEGOE_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_fitted_text(draw, start_pos, text, max_w, max_size=26, min_size=17, fill=(25,25,25)):
    x, y = start_pos
    cur_size = max_size
    font = get_font(FONT_SEGOE_BOLD, cur_size)
    while cur_size > min_size and draw.textlength(text, font=font) > max_w:
        cur_size -= 1
        font = get_font(FONT_SEGOE_BOLD, cur_size)
    
    # If still too long, split or wrap
    if draw.textlength(text, font=font) > max_w and " / " in text:
        parts = text.split(" / ")
        p1 = parts[0]
        p2 = "/ " + parts[1]
        f_small = get_font(FONT_SEGOE_BOLD, 20)
        draw.text((x, y - 6), p1, fill=fill, font=f_small)
        draw.text((x, y + 16), p2, fill=fill, font=f_small)
        return True
    else:
        draw.text((x, y), text, fill=fill, font=font)
        return False

# -------------------------------------------------------------
# 1. INDIVIDUAL IMAGES WITH ENHANCED BADGE
# -------------------------------------------------------------
def generate_individual_images():
    print("-> Gerando fotos individuais com tarja profissional...")
    font_badge = get_font(FONT_SEGOE_BOLD, 46)
    font_title = get_font(FONT_SEGOE_BOLD, 48)
    font_sub = get_font(FONT_SEGOE_REG, 26)
    font_tag = get_font(FONT_SEGOE_BOLD, 22)

    for item in COLORS:
        src_path = os.path.join(CORES_DIR, item["file"])
        im = Image.open(src_path).convert("RGBA")
        w, h = im.size

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        card_margin_x = 45
        card_margin_b = 55
        card_h = 220
        card_top = h - card_margin_b - card_h

        # Shadow
        draw.rounded_rectangle([card_margin_x + 4, card_top + 6, w - card_margin_x + 4, h - card_margin_b + 6], radius=24, fill=(0, 0, 0, 50))

        # Bottom Card
        border_col = (255, 120, 20, 255) if item["is_neon"] else (220, 215, 205, 255)
        border_w = 4 if item["is_neon"] else 2
        draw.rounded_rectangle(
            [card_margin_x, card_top, w - card_margin_x, h - card_margin_b],
            radius=24,
            fill=(255, 255, 255, 248),
            outline=border_col,
            width=border_w
        )

        badge_w = 110
        badge_h = 96
        badge_x = card_margin_x + 35
        badge_y = card_top + (card_h - badge_h) // 2

        if item["is_neon"]:
            badge_color = (255, 105, 0, 255) if item["id"] == "1E" else (185, 210, 0, 255)
            badge_text_color = (255, 255, 255, 255) if item["id"] == "1E" else (25, 35, 10, 255)
        else:
            badge_color = (40, 35, 30, 255)
            badge_text_color = (255, 255, 255, 255)

        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=18, fill=badge_color)

        bbox = draw.textbbox((0, 0), item["code"], font=font_badge)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((badge_x + (badge_w - tw) // 2, badge_y + (badge_h - th) // 2 - 4), item["code"], fill=badge_text_color, font=font_badge)

        text_x = badge_x + badge_w + 35
        title_y = card_top + 46
        draw.text((text_x, title_y), item["name"], fill=(30, 26, 22), font=font_title)

        sub_y = title_y + 64
        if item["is_neon"]:
            draw.text((text_x, sub_y), "LINHA ESPECIAL NEON • ALTA LUMINOSIDADE", fill=(230, 80, 0), font=get_font(FONT_SEGOE_BOLD, 26))
        else:
            draw.text((text_x, sub_y), "Catálogo de Barbantes • Linha Tradicional", fill=(130, 115, 105), font=font_sub)

        # Top Tag
        top_tag_w = 320 if item["is_neon"] else 280
        top_tag_h = 56
        draw.rounded_rectangle([45, 45, 45 + top_tag_w, 45 + top_tag_h], radius=14, fill=(255, 255, 255, 230), outline=(210, 205, 195, 220), width=2)
        tag_caption = "LINHA NEON ESPECIAL" if item["is_neon"] else "BARBANTE PREMIUM"
        tbbox = draw.textbbox((0, 0), tag_caption, font=font_tag)
        draw.text((45 + (top_tag_w - (tbbox[2] - tbbox[0])) // 2, 45 + (top_tag_h - (tbbox[3] - tbbox[1])) // 2 - 2), tag_caption, fill=(50, 45, 40), font=font_tag)

        result = Image.alpha_composite(im, overlay).convert("RGB")
        safe_name = item["name"].replace("/", "-").replace(" ", "_")
        filename = f"{item['code']}_{safe_name}.jpg"
        result.save(os.path.join(OUTPUT_INDIV_DIR, filename), quality=95)

# -------------------------------------------------------------
# HELPER: DRAW A SINGLE PRODUCT CARD
# -------------------------------------------------------------
def render_product_card(item, card_w, card_h, img_h, is_mobile=False):
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    is_neon = item["is_neon"]
    bg_fill = (255, 255, 255, 255)
    border_color = (255, 120, 30, 255) if is_neon else (225, 220, 212, 255)
    border_width = 3 if is_neon else 2

    draw.rounded_rectangle([0, 0, card_w, card_h], radius=22, fill=bg_fill, outline=border_color, width=border_width)

    pad = 10 if is_mobile else 12
    iw = card_w - (pad * 2)
    ih = img_h

    src_path = os.path.join(CORES_DIR, item["file"])
    with Image.open(src_path) as orig:
        ow, oh = orig.size
        crop_box = (30, 40, ow - 30, oh - 30)
        cropped = orig.crop(crop_box)
        resized_img = cropped.resize((iw, ih), Image.Resampling.LANCZOS).convert("RGBA")

    mask = Image.new("L", (iw, ih), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, iw, ih], radius=16, fill=255)
    card.paste(resized_img, (pad, pad), mask)

    # Info area
    info_y = pad + ih + (8 if is_mobile else 12)

    badge_w = 54 if is_mobile else 64
    badge_h = 42 if is_mobile else 48
    badge_x = pad + 6
    badge_y = info_y + 4

    if is_neon:
        badge_bg = (255, 105, 0, 255) if item["id"] == "1E" else (180, 205, 0, 255)
        badge_fg = (255, 255, 255, 255) if item["id"] == "1E" else (25, 35, 10, 255)
    else:
        badge_bg = (42, 38, 34, 255)
        badge_fg = (255, 255, 255, 255)

    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=10, fill=badge_bg)

    font_badge = get_font(FONT_SEGOE_BOLD, 22 if is_mobile else 26)
    b_box = draw.textbbox((0, 0), item["code"], font=font_badge)
    bw = b_box[2] - b_box[0]
    bh = b_box[3] - b_box[1]
    draw.text((badge_x + (badge_w - bw) // 2, badge_y + (badge_h - bh) // 2 - 2), item["code"], fill=badge_fg, font=font_badge)

    text_x = badge_x + badge_w + (10 if is_mobile else 14)
    max_text_w = card_w - text_x - 10

    max_font_sz = 22 if is_mobile else 26
    min_font_sz = 16 if is_mobile else 18
    was_split = draw_fitted_text(draw, (text_x, badge_y - 2), item["name"], max_text_w, max_size=max_font_sz, min_size=min_font_sz)

    cat_label = "Linha Neon" if is_neon else "Tradicional"
    cat_color = (220, 80, 0) if is_neon else (130, 120, 110)
    font_cat = get_font(FONT_SEGOE_REG, 15 if is_mobile else 18)

    sub_y = badge_y + (38 if was_split else 26)
    if is_mobile:
        draw.text((text_x, badge_y + 24 if not was_split else badge_y + 36), cat_label, fill=cat_color, font=font_cat)
    else:
        draw.text((text_x, badge_y + 28), "Linha Especial Neon" if is_neon else "Linha Tradicional", fill=cat_color, font=font_cat)

    return card

# -------------------------------------------------------------
# 2. MASTER FULL CATALOG POSTER (2480 x 4300 px)
# -------------------------------------------------------------
def generate_master_poster():
    print("-> Gerando Catálogo Geral Completo em Altíssima Resolução...")
    W = 2480
    H = 4300

    canvas = Image.new("RGBA", (W, H), (249, 248, 245, 255))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([25, 25, W - 25, H - 25], outline=(228, 222, 214, 255), width=2)
    draw.rectangle([35, 35, W - 35, H - 35], outline=(238, 234, 228, 255), width=1)

    header_h = 360
    draw.rectangle([25, 25, W - 25, header_h], fill=(255, 255, 255, 255))
    draw.line([(60, header_h), (W - 60, header_h)], fill=(225, 218, 208, 255), width=2)

    font_top_tag = get_font(FONT_SEGOE_BOLD, 22)
    tag_text = "COLEÇÃO EXCLUSIVA • FIOS E BARBANTES SELECIONADOS"
    t_box = draw.textbbox((0, 0), tag_text, font=font_top_tag)
    tw = t_box[2] - t_box[0]
    tag_bg_w = tw + 48
    draw.rounded_rectangle([(W - tag_bg_w) // 2, 55, (W + tag_bg_w) // 2, 95], radius=20, fill=(244, 240, 232, 255), outline=(215, 205, 195, 255), width=1)
    draw.text(((W - tw) // 2, 64), tag_text, fill=(110, 95, 80), font=font_top_tag)

    font_title = get_font(FONT_SEGOE_BOLD, 74)
    title_text = "CATÁLOGO DE CORES"
    tb = draw.textbbox((0, 0), title_text, font=font_title)
    draw.text(((W - (tb[2] - tb[0])) // 2, 115), title_text, fill=(38, 33, 28), font=font_title)

    font_sub = get_font(FONT_SEGOE_REG, 30)
    sub_text = "Barbantes 100% Algodão Ecológico • Toque Macio • Cores Vivas & Alto Rendimento"
    sb = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((W - (sb[2] - sb[0])) // 2, 210), sub_text, fill=(120, 105, 92), font=font_sub)

    draw.line([(W // 2 - 250, 275), (W // 2 + 250, 275)], fill=(185, 155, 120, 255), width=3)

    # Section 1 Header: Cores Tradicionais
    sec1_y = header_h + 35
    font_sec = get_font(FONT_SEGOE_BOLD, 36)
    title_sec1 = "LINHA TRADICIONAL"
    draw.text((90, sec1_y), title_sec1, fill=(45, 40, 35), font=font_sec)
    sec1_w = draw.textlength(title_sec1, font=font_sec)

    font_sec_sub = get_font(FONT_SEGOE_REG, 24)
    draw.text((90 + sec1_w + 25, sec1_y + 8), "—  (Cores 01 a 17 • Tons clássicos e contemporâneos)", fill=(130, 120, 110), font=font_sec_sub)
    draw.line([(90, sec1_y + 50), (W - 90, sec1_y + 50)], fill=(225, 218, 208, 255), width=2)

    cols = 4
    margin_x = 90
    card_gap = 32
    avail_w = W - (margin_x * 2) - ((cols - 1) * card_gap)
    card_w = avail_w // cols
    img_h = 420
    card_h = img_h + 96

    trad_items = [c for c in COLORS if not c["is_neon"]]

    start_y = sec1_y + 75
    for idx in range(16):
        r = idx // cols
        c = idx % cols
        cx = margin_x + c * (card_w + card_gap)
        cy = start_y + r * (card_h + card_gap)

        item = trad_items[idx]
        card_img = render_product_card(item, card_w, card_h, img_h)
        canvas.paste(card_img, (cx, cy), card_img)

    # Row 5: Item 17 + 3 Brand Highlights
    r = 4
    cy = start_y + r * (card_h + card_gap)

    cx = margin_x
    card_img = render_product_card(trad_items[16], card_w, card_h, img_h)
    canvas.paste(card_img, (cx, cy), card_img)

    highlights = [
        {"badge": "RENDIMENTO", "title": "Alto Rendimento", "desc": "Fios regulares e uniformes que deslizam perfeitamente na agulha, garantindo produtividade máxima."},
        {"badge": "MACIEZ", "title": "Toque Macio", "desc": "Estrutura confortável que não machuca as mãos e proporciona caimento impecável em tapetes e sousplats."},
        {"badge": "DURABILIDADE", "title": "Cores Firmes", "desc": "Tingimento premium de alta fixação que mantém o brilho e a vivacidade mesmo após muitas lavagens."}
    ]

    for h_idx, h_info in enumerate(highlights):
        hc = 1 + h_idx
        hcx = margin_x + hc * (card_w + card_gap)

        h_card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        h_draw = ImageDraw.Draw(h_card)
        h_draw.rounded_rectangle([0, 0, card_w, card_h], radius=22, fill=(244, 240, 233, 255), outline=(225, 218, 208, 255), width=2)
        h_draw.rounded_rectangle([15, 15, card_w - 15, card_h - 15], radius=16, outline=(235, 228, 218, 255), width=1)

        # Badge pill
        font_sym = get_font(FONT_SEGOE_BOLD, 20)
        bw_b = h_draw.textbbox((0, 0), h_info["badge"], font=font_sym)
        bp_w = (bw_b[2] - bw_b[0]) + 36
        h_draw.rounded_rectangle([card_w // 2 - bp_w // 2, 50, card_w // 2 + bp_w // 2, 95], radius=15, fill=(45, 40, 35, 255))
        h_draw.text((card_w // 2 - (bw_b[2] - bw_b[0]) // 2, 60), h_info["badge"], fill=(255, 255, 255), font=font_sym)

        font_ht = get_font(FONT_SEGOE_BOLD, 30)
        tb = h_draw.textbbox((0, 0), h_info["title"], font=font_ht)
        h_draw.text((card_w // 2 - (tb[2] - tb[0]) // 2, 125), h_info["title"], fill=(40, 35, 30), font=font_ht)

        font_hd = get_font(FONT_SEGOE_REG, 22)
        words = h_info["desc"].split(" ")
        lines = []
        cur_line = []
        for w_word in words:
            cur_line.append(w_word)
            test_line = " ".join(cur_line)
            if h_draw.textlength(test_line, font=font_hd) > card_w - 60:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [w_word]
        if cur_line:
            lines.append(" ".join(cur_line))

        line_y = 195
        for l in lines:
            lb = h_draw.textbbox((0, 0), l, font=font_hd)
            h_draw.text((card_w // 2 - (lb[2] - lb[0]) // 2, line_y), l, fill=(100, 90, 80), font=font_hd)
            line_y += 34

        font_st = get_font(FONT_SEGOE_BOLD, 20)
        stamp = "PADRÃO DE QUALIDADE"
        stb = h_draw.textbbox((0, 0), stamp, font=font_st)
        h_draw.text((card_w // 2 - (stb[2] - stb[0]) // 2, card_h - 60), stamp, fill=(160, 145, 130), font=font_st)

        canvas.paste(h_card, (hcx, cy), h_card)

    # Section 2: Cores Especiais (Neon)
    sec2_y = cy + card_h + 45
    title_sec2 = "CORES ESPECIAIS • LINHA NEON"
    draw.text((90, sec2_y), title_sec2, fill=(225, 75, 0), font=font_sec)
    sec2_w = draw.textlength(title_sec2, font=font_sec)
    draw.text((90 + sec2_w + 25, sec2_y + 8), "—  (Cores 1E e 2E • Pigmentação neon de altíssima luminosidade)", fill=(130, 120, 110), font=font_sec_sub)
    draw.line([(90, sec2_y + 50), (W - 90, sec2_y + 50)], fill=(255, 160, 100, 255), width=2)

    neon_items = [c for c in COLORS if c["is_neon"]]
    neon_y = sec2_y + 75
    neon_w = card_w + 40
    neon_h = card_h + 20
    neon_img_h = img_h + 20
    spacing = 80
    total_neon_w = (neon_w * 2) + spacing
    neon_start_x = (W - total_neon_w) // 2

    for n_idx, n_item in enumerate(neon_items):
        nx = neon_start_x + n_idx * (neon_w + spacing)
        neon_card = render_product_card(n_item, neon_w, neon_h, neon_img_h)
        canvas.paste(neon_card, (nx, neon_y), neon_card)

    # Footer
    footer_y = H - 150
    draw.line([(90, footer_y), (W - 90, footer_y)], fill=(225, 218, 208, 255), width=2)

    font_ft = get_font(FONT_SEGOE_REG, 24)
    ft_text1 = "* As cores podem apresentar pequenas variações de tonalidade dependendo do lote do barbante e da calibração do seu visor/monitor."
    draw.text((90, footer_y + 25), ft_text1, fill=(125, 115, 105), font=font_ft)

    ft_text2 = "Ideal para tapetes, jogos de banheiro, passadeiras, caminhos de mesa, bolsas e artesanatos em geral."
    draw.text((90, footer_y + 65), ft_text2, fill=(155, 145, 135), font=font_ft)

    font_ft_brand = get_font(FONT_SEGOE_BOLD, 28)
    draw.text((W - 350, footer_y + 40), "BARBANTES 2026", fill=(45, 40, 35), font=font_ft_brand)

    out_file = os.path.join(BASE_DIR, "Catalogo_Completo_Barbantes.jpg")
    canvas.convert("RGB").save(out_file, quality=95)
    print(f"Catálogo Geral salvo com sucesso: {out_file}")

# -------------------------------------------------------------
# 3. WHATSAPP & SOCIAL MEDIA EDITIONS (1080x1920)
# -------------------------------------------------------------
def generate_whatsapp_editions():
    print("-> Gerando edições especiais para WhatsApp e Celular (1080x1920)...")
    W = 1080
    H = 1920

    pages = [
        {
            "filename": "Catalogo_WhatsApp_Parte1.jpg",
            "tag": "PARTE 1 DE 2 • CORES TRADICIONAIS (01 A 09)",
            "items": COLORS[0:9],
        },
        {
            "filename": "Catalogo_WhatsApp_Parte2.jpg",
            "tag": "PARTE 2 DE 2 • CORES TRADICIONAIS & LINHA NEON",
            "items": COLORS[9:19],
        }
    ]

    for p_idx, page in enumerate(pages):
        canvas = Image.new("RGBA", (W, H), (249, 248, 245, 255))
        draw = ImageDraw.Draw(canvas)

        draw.rectangle([15, 15, W - 15, H - 15], outline=(225, 218, 210, 255), width=2)
        draw.rectangle([15, 15, W - 15, 185], fill=(255, 255, 255, 255))
        draw.line([(30, 185), (W - 30, 185)], fill=(225, 218, 210, 255), width=2)

        font_w_tag = get_font(FONT_SEGOE_BOLD, 18)
        draw.text((45, 32), page["tag"], fill=(195, 95, 30), font=font_w_tag)

        font_w_title = get_font(FONT_SEGOE_BOLD, 46)
        draw.text((45, 60), "CATÁLOGO DE BARBANTES", fill=(35, 30, 25), font=font_w_title)

        font_w_sub = get_font(FONT_SEGOE_REG, 22)
        draw.text((45, 122), "Fios Selecionados • Cores Vivas • 100% Algodão", fill=(120, 110, 100), font=font_w_sub)

        if p_idx == 0:
            margin_x = 35
            gap_x = 22
            gap_y = 22
            card_w = (W - (margin_x * 2) - (gap_x * 2)) // 3
            img_h = 385
            card_h = 500
            start_y = 210

            for idx, item in enumerate(page["items"]):
                r = idx // 3
                c = idx % 3
                cx = margin_x + c * (card_w + gap_x)
                cy = start_y + r * (card_h + gap_y)

                card = render_product_card(item, card_w, card_h, img_h, is_mobile=True)
                canvas.paste(card, (cx, cy), card)
        else:
            margin_x = 35
            gap_x = 20
            gap_y = 20
            card_w = (W - (margin_x * 2) - (gap_x * 2)) // 3
            img_h = 270
            card_h = 375
            start_y = 205

            items = page["items"]
            # Row 1: 10, 11, 12
            for c in range(3):
                cx = margin_x + c * (card_w + gap_x)
                cy = start_y
                card = render_product_card(items[c], card_w, card_h, img_h, is_mobile=True)
                canvas.paste(card, (cx, cy), card)

            # Row 2: 13, 14, 15
            for c in range(3):
                cx = margin_x + c * (card_w + gap_x)
                cy = start_y + card_h + gap_y
                card = render_product_card(items[3 + c], card_w, card_h, img_h, is_mobile=True)
                canvas.paste(card, (cx, cy), card)

            # Row 3: 16, 17
            w2_total = (card_w * 2) + gap_x
            start_x_r3 = (W - w2_total) // 2
            cy_r3 = start_y + (card_h + gap_y) * 2
            for c in range(2):
                cx = start_x_r3 + c * (card_w + gap_x)
                card = render_product_card(items[6 + c], card_w, card_h, img_h, is_mobile=True)
                canvas.paste(card, (cx, cy_r3), card)

            # Row 4: 1E, 2E
            cy_r4 = start_y + (card_h + gap_y) * 3
            draw.line([(40, cy_r4 - 12), (W - 40, cy_r4 - 12)], fill=(255, 140, 40, 255), width=2)
            font_neon_lbl = get_font(FONT_SEGOE_BOLD, 19)
            neon_txt = "• CORES ESPECIAIS NEON •"
            ntb = draw.textbbox((0, 0), neon_txt, font=font_neon_lbl)
            draw.text(((W - (ntb[2] - ntb[0])) // 2, cy_r4 - 24), neon_txt, fill=(230, 80, 0), font=font_neon_lbl)

            for c in range(2):
                cx = start_x_r3 + c * (card_w + gap_x)
                card = render_product_card(items[8 + c], card_w, card_h, img_h, is_mobile=True)
                canvas.paste(card, (cx, cy_r4), card)

        draw.line([(30, H - 75), (W - 30, H - 75)], fill=(225, 218, 210, 255), width=1)
        font_ft = get_font(FONT_SEGOE_REG, 18)
        draw.text((45, H - 55), "Consulte disponibilidade de espessuras (Fio 4, 6 ou 8).", fill=(130, 120, 110), font=font_ft)
        draw.text((W - 240, H - 55), "Qualidade Garantida", fill=(60, 50, 40), font=get_font(FONT_SEGOE_BOLD, 18))

        out_path = os.path.join(BASE_DIR, page["filename"])
        canvas.convert("RGB").save(out_path, quality=95)
        print(f"Salvo: {page['filename']}")

if __name__ == "__main__":
    generate_individual_images()
    generate_master_poster()
    generate_whatsapp_editions()
    print("TODAS AS IMAGENS DO CATÁLOGO FORAM REGENERADAS COM SUCESSO!")
