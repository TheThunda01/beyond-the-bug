"""Draw the two published GLASS reporting counts as a common-scale bar chart."""
import csv
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def draw() -> None:
    with (ROOT / "data/glass-participation.csv").open(newline="", encoding="utf-8") as source:
        rows = [(int(row["year"]), int(row["reporting_countries"])) for row in csv.DictReader(source)]
    if not rows or len({year for year, _ in rows}) != len(rows) or any(count < 0 for _, count in rows):
        raise ValueError("Expected unique years with nonnegative reporting counts")
    rows.sort()
    axis_max = max(25, ((max(count for _, count in rows) + 24) // 25) * 25)
    height = 98 + 44 * len(rows)
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", viewBox=f"0 0 560 {height}",
                     role="img", attrib={"aria-labelledby": "title desc"})
    ET.SubElement(svg, "title", id="title").text = "Countries reporting to WHO GLASS"
    ET.SubElement(svg, "desc", id="desc").text = ". ".join(f"{year}: {count} countries" for year, count in rows)
    g = ET.SubElement(svg, "g", fill="#16333e", attrib={"font-family": "system-ui, sans-serif"})
    ET.SubElement(g, "rect", width="560", height=str(height), fill="#fff")
    ET.SubElement(g, "text", x="12", y="23", attrib={"font-size": "18", "font-weight": "600"}).text = "Reporting countries"
    bottom = height - 40
    for value in range(0, axis_max + 1, 25):
        x = str(80 + 440 * value / axis_max)
        ET.SubElement(g, "line", x1=x, x2=x, y1="37", y2=str(bottom), stroke="#ccd7d8")
        ET.SubElement(g, "text", x=x, y=str(bottom + 22), attrib={"text-anchor": "middle"}).text = str(value)
    for index, (year, count) in enumerate(rows):
        y = 46 + 44 * index
        width = 440 * count / axis_max
        ET.SubElement(g, "text", x="12", y=str(y + 19)).text = str(year)
        ET.SubElement(g, "rect", x="80", y=str(y), width=str(width), height="26", fill="#18706d")
        ET.SubElement(g, "text", x=str(86 + width), y=str(y + 19), attrib={"font-weight": "600"}).text = str(count)
    ET.indent(svg)
    (ROOT / "figures").mkdir(exist_ok=True)
    ET.ElementTree(svg).write(ROOT / "figures/glass-participation.svg", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    draw()
