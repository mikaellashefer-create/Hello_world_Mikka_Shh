import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

# -----------------------------------------------------------------------------
# БЛОК 1: ПОДКЛЮЧЕНИЕ И ИЗВЛЕЧЕНИЕ ДАННЫХ
# -----------------------------------------------------------------------------

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5435",               # ваш порт
        user="postgres_task",      # ваш пользователь
        password="student",        # ваш пароль
        database="student"         # ваша база
    )
    print("✓ Подключение установлено")

    # --- Запрос 1: средняя цена и количество цен по категориям ---
    df_categories = pd.read_sql("""
        SELECT 
            p.category,
            ROUND(AVG(pr.price)::numeric, 2) AS avg_price,
            COUNT(pr.price) AS price_count
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        GROUP BY p.category
        ORDER BY avg_price DESC
    """, connection)

    # --- Запрос 2: количество товаров по категориям ---
    df_products_count = pd.read_sql("""
        SELECT 
            category,
            COUNT(id) AS product_count
        FROM products
        GROUP BY category
        ORDER BY category
    """, connection)

    # --- Запрос 3: все цены с категориями — для boxplot ---
    df_all_prices = pd.read_sql("""
        SELECT 
            p.category,
            pr.price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
    """, connection)

    # --- Запрос 4: аномалии — товары без цен ---
    df_missing_prices = pd.read_sql("""
        SELECT 
            p.name AS product_name,
            p.category
        FROM products p
        LEFT JOIN prices pr ON p.id = pr.product_id
        WHERE pr.price IS NULL
        ORDER BY p.category
    """, connection)

    print(f"Категорий в выборке:           {len(df_categories)}")
    print(f"Всего записей о ценах:         {len(df_all_prices)}")
    print(f"Товаров без цен (ан.):         {len(df_missing_prices)}")

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто\n")

# -----------------------------------------------------------------------------
# БЛОК 2: ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ
# -----------------------------------------------------------------------------

# Короткие названия категорий для подписей осей (длинные не влезают)
NAME_MAP = {
    "Электроника": "Эл",
    "Бытовая техника": "Быт. тех",
    "Одежда": "Од",
    "Книги": "Кн",
    "Продукты": "Про",
}
df_categories["short_name"] = df_categories["category"].map(NAME_MAP)

# Порог «нормы» — категории ниже порога по средней цене выделим красным
PRICE_THRESHOLD = 10000
overall_avg = df_categories["avg_price"].mean()

# Цвет столбца: синий — норма, красный — ниже порога
bar_colors = [
    "#d9534f" if p < PRICE_THRESHOLD else "#4a90d9"
    for p in df_categories["avg_price"]
]

# Подписи для круговой диаграммы вида «Электроника (5 шт.)»
pie_labels = [
    f"{row.category} ({row.product_count} шт.)"
    for row in df_products_count.itertuples()
]

# -----------------------------------------------------------------------------
# БЛОК 3: ПОСТРОЕНИЕ ГРАФИКОВ
#
# Схема сетки:
#
#   ┌──────────────────────┬──────────────────┐
#   │                      │                  │
#   │  График 1 (2 колонки)│  График 2        │
#   │  Средняя цена        │  Кол-во товаров  │
#   │  по категориям       │  по категориям   │
#   │                      │                  │
#   ├──────────┬───────────┴──────────────────┤
#   │          │                              │
#   │ График 3 │  График 4                    │
#   │ Круговая │  Гистограмма цен             │
#   │ диаграмма│                              │
#   └──────────┴──────────────────────────────┘
# -----------------------------------------------------------------------------

plt.rcParams.update({
    "font.family":       "DejaVu Sans", #шрифт
    "font.size":         8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True, #сетка
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "figure.dpi":        130,#качество
})

fig = plt.figure(figsize=(18, 12))
fig.suptitle("Анализ товарной базы данных", fontsize=15, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig, #к какой фигуре привязать
                       height_ratios=[5, 4], #соотношение высот строк
                       width_ratios=[2, 1, 2], #соотношение ширин колонок
                       hspace=0.6, wspace=0.5) #гор и верт отступы

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1:3])

# ── ГРАФИК 1: Горизонтальная столбчатая диаграмма — средняя цена по категориям ──
bars1 = ax1.barh(
    df_categories["short_name"], #ось Y
    df_categories["avg_price"], #определяет длину столбцов
    color=bar_colors,
    edgecolor="white",
    height=0.6,
)

for bar, val in zip(bars1, df_categories["avg_price"]): #соединяет в пары
    ax1.text( #добавляет текст
        bar.get_width() + 30,
        bar.get_y() + bar.get_height() / 2,
        f"{val:,.0f} руб.",
        va="center", fontsize=7, #выравнивание по центру
    )

ax1.axvline(overall_avg, color="darkorange", linestyle="--", #вертикальная линия
            linewidth=1.3, label=f"Среднее: {overall_avg:.0f} руб.")

ax1.set_xlabel("Средняя цена (руб.)")
ax1.set_title("Средняя цена по категориям", fontweight="bold", pad=8)

legend_patches = [ #цветной прямоугольник для легенды
    Patch(facecolor="#4a90d9", label=f"Норма (≥ {PRICE_THRESHOLD} руб.)"),
    Patch(facecolor="#d9534f", label="Ниже нормы"),
]
ax1.legend(handles=legend_patches, fontsize=8, loc="upper right") #что показывать и где

# ── ГРАФИК 2: Вертикальная столбчатая диаграмма — количество товаров по категориям ──
bars2 = ax2.bar(
    df_products_count["category"],
    df_products_count["product_count"],
    color="#5cb85c",
    edgecolor="white", #граница
    width=0.6,
)

for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        str(int(bar.get_height())),#преобразует число в целое, далее в строку
        ha="center", fontsize=7,
    )

ax2.set_ylim(0, max(df_products_count["product_count"]) + 2)
ax2.set_ylabel("Количество товаров")
ax2.set_title("Количество товаров\nпо категориям", fontweight="bold", pad=8)

ax2.set_xticks(range(len(df_products_count)))
ax2.set_xticklabels(df_products_count["category"], rotation=40, ha="right", fontsize=8) #поворот надписей и выравнивание

# ── ГРАФИК 3: Круговая диаграмма — товары по категориям ──
pie_colors = ["#4a90d9", "#5cb85c", "#f0ad4e", "#7b68ee", "#d9534f"]

wedges, texts, autotexts = ax3.pie(
    df_products_count["product_count"], #количество
    labels=None, #подпись секторов
    autopct="%1.0f%%", #проценты
    colors=pie_colors, #цвет
    startangle=90, #начать с 12 часов
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},#стиль векторов
    pctdistance=0.7, #расстояние % от центра
)

for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_fontweight("bold")

ax3.set_title("Товары\nпо категориям", fontweight="bold", pad=8)

ax3.legend(
    wedges, pie_labels,
    loc="lower right",
    bbox_to_anchor=(0.5, -0.22),#смещение графика
    fontsize=8,
    frameon=False,
)

# ── ГРАФИК 4: Ящик с усами (Boxplot) — распределение цен по категориям ──
#
# Почему boxplot лучше гистограммы для этих данных?
# 1. Показывает медиану, квартили и выбросы одной картинкой
# 2. Компактно сравнивает несколько категорий
# 3. Автоматически выделяет аномалии (точки за "усами")

# Подготовка данных: список цен по категориям
categories_order = df_categories["category"].tolist()
box_data = []
box_labels = []

for cat in categories_order:
    prices_cat = df_all_prices[df_all_prices["category"] == cat]["price"].values # счет значений и сортировка по росту
    if len(prices_cat) > 0:
        box_data.append(prices_cat)
        # Сокращённые названия для подписей
        short_name = NAME_MAP.get(cat, cat)
        box_labels.append(f"{short_name}\n(n={len(prices_cat)})")

# Построение boxplot
bp = ax4.boxplot(
    box_data,
    labels=box_labels,
    patch_artist=True,           # чтобы можно было закрасить коробки
    showmeans=False,             # не показываем среднее (есть медиана)
    medianprops={'color': 'darkred', 'linewidth': 2, 'label': 'Медиана'},
    whiskerprops={'color': '#333', 'linewidth': 1},
    capprops={'color': '#333', 'linewidth': 1},
    flierprops={
        'marker': 'o',
        'markerfacecolor': '#d9534f',
        'markeredgecolor': '#333',
        'markersize': 7,
        #'label': 'Выбросы'
    }
)
# Поворот подписей на boxplot
ax4.set_xticklabels(box_labels, rotation=45, ha='right', fontsize=7)

# Закрашиваем коробки разными цветами (по категориям)
box_colors = ["#4a90d9", "#5cb85c", "#f0ad4e", "#7b68ee", "#d9534f"]
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(box_colors[i % len(box_colors)])
    box.set_alpha(0.7)
    box.set_edgecolor('#333')
    box.set_linewidth(1.2)

# Добавляем горизонтальную линию общего среднего
overall_mean = df_all_prices["price"].mean()
ax4.axhline(overall_mean, color='darkorange', linestyle='--',
            linewidth=1.5, label=f'Общее среднее: {overall_mean:,.0f} руб.')

ax4.set_ylabel('Цена (руб.)')
ax4.set_title('Распределение цен по категориям',
              fontweight='bold', pad=8)
#ax4.legend(fontsize=8, loc='upper right')
ax4.grid(axis='y', alpha=0.3)

# Добавляем подпись о выбросах
#ax4.text(0.02, 0.98, '● — выбросы (аномалии)',
         #transform=ax4.transAxes, fontsize=8,
         #color='#d9534f', va='top')

# Дополнительная статистика в углу
stats_text = (
    f"Всего цен: {len(df_all_prices)}\n"
    f"Медиана: {df_all_prices['price'].median():,.0f} руб.\n"
    f"Среднее: {df_all_prices['price'].mean():,.0f} руб.\n"
    f"Ст. откл.: {df_all_prices['price'].std():,.0f} руб."
)
ax4.text(0.97, 0.97, stats_text,
         transform=ax4.transAxes,
         va='top', ha='right', fontsize=8,
         bbox={'boxstyle': 'round,pad=0.4',
               'facecolor': 'lightyellow',
               'edgecolor': 'lightgray',
               'alpha': 0.8})

# Аномалия на отдельном текстовом блоке под всей фигурой
if len(df_missing_prices) > 0:
    fig.text( #текст на фигуру
        0.5, -0.03,
        f"⚠ Аномалия: {len(df_missing_prices)} товаров не имеют цен: "
        f"{', '.join(df_missing_prices['product_name'].head(3).tolist())}", #объединение в список, первые 3 эл и преобразует в обычный список
        ha="center", fontsize=9, color="#8b0000",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#fff3f3", "edgecolor": "#d9534f"}
    )
else:
    fig.text(
        0.5, -0.03,
        "✓ Аномалий не обнаружено",
        ha="center", fontsize=9, color="#2ecc71",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f0fff0", "edgecolor": "#5cb85c"}
    )

# -----------------------------------------------------------------------------
# БЛОК 4: СОХРАНЕНИЕ
# -----------------------------------------------------------------------------

OUTPUT_FILE = "products_analysis.png" #формат пнг
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"✓ График сохранён: {OUTPUT_FILE}")
plt.show()