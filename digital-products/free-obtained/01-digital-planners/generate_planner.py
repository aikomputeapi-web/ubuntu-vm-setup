"""
Hyperlinked Digital Planner PDF Generator
==========================================
Generates a complete 2026-2027 digital planner PDF with:
- Monthly calendar grids (July 2026 - December 2027)
- Weekly spreads (2-page layout)
- Daily pages
- Hyperlinked index/tabs for navigation
- Aesthetic minimal design

Each year/variant is just a re-run with different parameters.
Requires: reportlab, pypdf
"""

import calendar
import io
from datetime import date, timedelta
from reportlab.lib.pagesizes import landscape, portrait, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

# Configuration
PAGE_SIZE = landscape(portrait(letter))  # ~612 x 792 pts
LAND_W, LAND_H = PAGE_SIZE  # For landscape letter
# Actually use landscape letter for tablet-friendly ratio
from reportlab.lib.pagesizes import letter
PAGE_W, PAGE_H = landscape(letter)  # 792 x 612

# Colors - Aesthetic palette
PRIMARY = HexColor("#2C3E50")
ACCENT = HexColor("#E8B4B8")
LIGHT_BG = HexColor("#FAF7F2")
TEXT = HexColor("#333333")
SUBTLE = HexColor("#CCCCCC")
LINE = HexColor("#D5CFC7")
MONTH_COLORS = [
    HexColor("#E8B4B8"),  # Jan - blush
    HexColor("#D4A5A5"),  # Feb
    HexColor("#B8D8BA"),  # Mar - sage green
    HexColor("#A8D5BA"),  # Apr
    HexColor("#95C6B8"),  # May
    HexColor("#7FB5A6"),  # Jun
    HexColor("#6BA8B5"),  # Jul - teal
    HexColor("#5C9B9A"),  # Aug
    HexColor("#E8C4A0"),  # Sep - warm
    HexColor("#D4A574"),  # Oct
    HexColor("#C4956C"),  # Nov
    HexColor("#9B7B8D"),  # Dec - mauve
]

DAY_NAMES_SUN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
DAY_NAMES_MON = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class PlannerGenerator:
    def __init__(self, year=2026, start_month=1, num_months=24, 
                 week_starts_monday=True, theme_name="Minimalist", accent_color=None):
        self.year = year
        self.start_month = start_month
        self.num_months = num_months
        self.week_starts_monday = week_starts_monday
        self.day_names = DAY_NAMES_MON if week_starts_monday else DAY_NAMES_SUN
        self.theme_name = theme_name
        self.accent = accent_color or HexColor("#E8B4B8")
        self.pages_buffer = io.BytesIO()
        self.c = canvas.Canvas(self.pages_buffer, pagesize=landscape(letter))
        self.page_count = 0
        # Track page boundaries for linking
        # Maps: (section, year, month, day) -> page_index (0-based)
        self.page_map = {}
        
    def _get_month_dates(self, year, month):
        """Get all dates in a month."""
        num_days = calendar.monthrange(year, month)[1]
        return [date(year, month, d) for d in range(1, num_days + 1)]
    
    def _draw_background(self):
        """Draw a subtle background."""
        self.c.setFillColor(LIGHT_BG)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    def _draw_header(self, title, subtitle=""):
        """Draw a page header."""
        self.c.setFillColor(PRIMARY)
        self.c.setFont("Helvetica", 20)
        self.c.drawString(40, PAGE_H - 50, title)
        if subtitle:
            self.c.setFont("Helvetica", 11)
            self.c.setFillColor(SUBTLE)
            self.c.drawString(40, PAGE_H - 65, subtitle)
        # Accent line
        self.c.setStrokeColor(self.accent)
        self.c.setLineWidth(2)
        self.c.line(40, PAGE_H - 75, PAGE_W - 40, PAGE_H - 75)
    
    def _draw_tab_navigation(self, current_section=None, pages_for_tabs=None):
        """Draw bottom tab navigation bar."""
        tab_w = (PAGE_W - 80) / 5
        tabs = [
            ("Index", "index"),
            ("Months", "months"),
            ("Weekly", "weekly"),
            ("Daily", "daily"),
            ("Notes", "notes"),
        ]
        y = 20
        for i, (label, section) in enumerate(tabs):
            x = 40 + i * tab_w
            bg = HexColor("#E8E6E0") if section == current_section else white
            self.c.setFillColor(bg)
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(x, y, tab_w - 5, 28, 5, fill=1, stroke=1)
            self.c.setFillColor(PRIMARY)
            self.c.setFont("Helvetica", 9)
            self.c.drawCentredString(x + (tab_w - 5) / 2, y + 10, label)
        return y
    
    def _finish_page(self):
        """Finalize current page."""
        self.c.showPage()
        self.page_count += 1
    
    def draw_index_page(self):
        """Draw the index/home page with navigation links."""
        self.page_map["index"] = self.page_count
        self._draw_background()
        self._draw_header(f"{self.year} Digital Planner", self.theme_name)
        
        # Welcome text
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(TEXT)
        self.c.drawString(40, PAGE_H - 120, "Tap a section to navigate:")
        
        sections = [
            ("Monthly Calendars", "Jump to month grid views"),
            ("Weekly Spreads", "Two-page weekly layouts with planning space"),
            ("Daily Pages", "One page per day with hourly schedule"),
            ("Notes & Lists", "Blank lined pages for free notes"),
        ]
        
        y = PAGE_H - 160
        box_w = (PAGE_W - 80) / 2 - 10
        for i, (title, desc) in enumerate(sections):
            col = i % 2
            row = i // 2
            x = 40 + col * (box_w + 20)
            by = y - row * 80
            
            self.c.setFillColor(white)
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(x, by - 60, box_w, 65, 8, fill=1, stroke=1)
            
            self.c.setFillColor(PRIMARY)
            self.c.setFont("Helvetica-Bold", 14)
            self.c.drawString(x + 15, by - 25, title)
            self.c.setFillColor(SUBTLE)
            self.c.setFont("Helvetica", 9)
            self.c.drawString(x + 15, by - 45, desc)
        
        # Calendar year info
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(SUBTLE)
        self.c.drawString(40, 60, f"Generated {date.today().isoformat()} | {self.page_count + 1} pages | Free open-source planner")
        
        self._draw_tab_navigation("index")
        self._finish_page()
    
    def draw_monthly_page(self, year, month):
        """Draw a monthly calendar grid."""
        key = f"month-{year}-{month:02d}"
        self.page_map[key] = self.page_count
        self.page_map.setdefault("months", self.page_count)
        
        self._draw_background()
        month_name = calendar.month_name[month]
        self._draw_header(f"{month_name} {year}", "Monthly Overview")
        
        # Calendar grid
        cal = calendar.Calendar()
        if not self.week_starts_monday:
            cal = calendar.Calendar(firstweekday=6)  # Sunday
        else:
            cal = calendar.Calendar(firstweekday=0)  # Monday
        
        weeks = list(cal.monthdatescalendar(year, month))
        
        # Grid dimensions
        grid_x = 40
        grid_y = 90
        grid_w = PAGE_W - 80 - 120  # Leave room for side panel
        grid_h = PAGE_H - 180
        col_w = grid_w / 7
        row_h = grid_h / (len(weeks) + 1)  # +1 for header
        
        accent = MONTH_COLORS[(month - 1) % 12]
        
        # Day headers
        for i, day_name in enumerate(self.day_names):
            x = grid_x + i * col_w
            self.c.setFillColor(accent)
            self.c.roundRect(x, grid_y + grid_h - row_h, col_w - 2, row_h - 2, 3, fill=1, stroke=0)
            self.c.setFillColor(white if accent != HexColor("#E8B4B8") else PRIMARY)
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawCentredString(x + col_w / 2, grid_y + grid_h - row_h + 8, day_name[:3])
        
        # Day cells
        for wi, week in enumerate(weeks):
            for di, d in enumerate(week):
                x = grid_x + di * col_w
                y = grid_y + grid_h - (wi + 2) * row_h
                is_current = d.month == month
                bg = white if is_current else HexColor("#F0EDE8")
                
                self.c.setFillColor(bg)
                self.c.setStrokeColor(LINE)
                self.c.setLineWidth(0.3)
                self.c.roundRect(x, y, col_w - 2, row_h - 2, 2, fill=1, stroke=1)
                
                # Day number
                self.c.setFillColor(PRIMARY if is_current else SUBTLE)
                self.c.setFont("Helvetica-Bold", 10 if is_current else 8)
                self.c.drawString(x + 5, y + row_h - 12, str(d.day))
                
                # Small dot for link indicator
                if is_current:
                    self.c.setFillColor(accent)
                    self.c.circle(x + col_w - 8, y + row_h - 8, 2, fill=1, stroke=0)
        
        # Side panel for notes
        side_x = grid_x + grid_w + 10
        self.c.setFillColor(HexColor("#F5F2ED"))
        self.c.setStrokeColor(LINE)
        self.c.roundRect(side_x, grid_y, 110, grid_h, 5, fill=1, stroke=1)
        
        self.c.setFillColor(PRIMARY)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(side_x + 10, grid_y + grid_h - 20, "Goals")
        
        # Lines for notes
        self.c.setStrokeColor(SUBTLE)
        self.c.setLineWidth(0.3)
        for i in range(8):
            ly = grid_y + grid_h - 40 - i * 24
            self.c.line(side_x + 10, ly, side_x + 100, ly)
        
        self._draw_tab_navigation("months")
        self._finish_page()
    
    def draw_weekly_page(self, year, month, week_num, week_dates):
        """Draw a weekly spread (landscape, 7 days across)."""
        key = f"weekly-{year}-{week_num:02d}"
        self.page_map[key] = self.page_count
        self.page_map.setdefault("weekly", self.page_count)
        
        self._draw_background()
        
        month_name = calendar.month_name[month]
        d = week_dates[0]
        end_d = week_dates[-1]
        self._draw_header(f"Week of {d.strftime('%b %d')} - {end_d.strftime('%b %d, %Y')}")
        
        accent = MONTH_COLORS[(month - 1) % 12]
        
        # 7 columns for 7 days
        col_w = (PAGE_W - 80) / 7
        for i, day in enumerate(week_dates):
            x = 40 + i * col_w
            y = 90
            h = PAGE_H - 160
            
            self.c.setFillColor(white)
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(0.3)
            self.c.roundRect(x, y, col_w - 4, h, 3, fill=1, stroke=1)
            
            # Day header
            self.c.setFillColor(accent)
            self.c.roundRect(x, y + h - 25, col_w - 4, 22, 3, fill=1, stroke=0)
            self.c.setFillColor(white)
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawCentredString(x + (col_w - 4) / 2, y + h - 14, day.strftime("%a %d"))
            
            # Lines for tasks
            self.c.setStrokeColor(SUBTLE)
            self.c.setLineWidth(0.3)
            for j in range(12):
                ly = y + h - 45 - j * 22
                if ly > y + 20:
                    self.c.line(x + 6, ly, x + col_w - 10, ly)
        
        self._draw_tab_navigation("weekly")
        self._finish_page()
    
    def draw_daily_page(self, d):
        """Draw a single daily page."""
        key = f"daily-{d.year}-{d.month:02d}-{d.day:02d}"
        self.page_map[key] = self.page_count
        self.page_map.setdefault("daily", self.page_count)
        
        self._draw_background()
        
        month_name = calendar.month_name[d.month]
        self._draw_header(
            f"{d.strftime('%A, %B %d')}",
            f"{d.year}"
        )
        
        accent = MONTH_COLORS[(d.month - 1) % 12]
        
        # Left: Hourly schedule
        left_w = PAGE_W * 0.45 - 40
        self.c.setFillColor(white)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(40, 90, left_w, PAGE_H - 160, 5, fill=1, stroke=1)
        
        self.c.setFillColor(accent)
        self.c.roundRect(40, PAGE_H - 95, left_w, 25, 5, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(50, PAGE_H - 82, "Schedule")
        
        # Hourly slots (6am - 10pm)
        hours = list(range(6, 23))
        slot_h = (PAGE_H - 220) / len(hours)
        for i, hr in enumerate(hours):
            y = PAGE_H - 110 - (i + 1) * slot_h
            self.c.setStrokeColor(SUBTLE)
            self.c.setLineWidth(0.3)
            self.c.line(50, y, 40 + left_w - 10, y)
            
            self.c.setFillColor(PRIMARY)
            self.c.setFont("Helvetica", 8)
            am_pm = "AM" if hr < 12 else "PM"
            hr12 = hr if hr <= 12 else hr - 12
            if hr12 == 0:
                hr12 = 12
            self.c.drawString(50, y - 10, f"{hr12}:00 {am_pm}")
        
        # Right: Tasks + Notes
        right_x = 40 + left_w + 15
        right_w = PAGE_W - right_x - 40
        
        # Task section
        self.c.setFillColor(white)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(right_x, PAGE_H - 320, right_w, PAGE_H - 95 - (PAGE_H - 320), 5, fill=1, stroke=1)
        # Actually just calculate:
        task_top = PAGE_H - 95
        task_bot = 250
        self.c.setFillColor(white)
        self.c.setStrokeColor(LINE)
        # Redraw properly
        self.c.setFillColor(LIGHT_BG)
        self.c.roundRect(right_x, task_bot, right_w, task_top - task_bot, 5, fill=1, stroke=1)
        
        self.c.setFillColor(accent)
        self.c.roundRect(right_x, task_top - 25, right_w, 22, 5, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(right_x + 10, task_top - 14, "Top Priorities")
        
        # Task lines with checkboxes
        for i in range(5):
            y = task_top - 45 - i * 25
            self.c.setStrokeColor(SUBTLE)
            self.c.setLineWidth(0.3)
            # Checkbox
            self.c.setFillColor(white)
            self.c.setStrokeColor(accent)
            self.c.setLineWidth(0.8)
            self.c.rect(right_x + 10, y - 8, 12, 12, fill=1, stroke=1)
            # Line
            self.c.setStrokeColor(SUBTLE)
            self.c.setLineWidth(0.3)
            self.c.line(right_x + 28, y, right_x + right_w - 10, y)
        
        # Notes section
        notes_top = 230
        self.c.setFillColor(LIGHT_BG)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(right_x, 90, right_w, notes_top - 90, 5, fill=1, stroke=1)
        
        self.c.setFillColor(accent)
        self.c.roundRect(right_x, notes_top - 25, right_w, 22, 5, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(right_x + 10, notes_top - 14, "Notes")
        
        # Lines
        self.c.setStrokeColor(SUBTLE)
        self.c.setLineWidth(0.3)
        for i in range(7):
            y = notes_top - 40 - i * 20
            if y > 100:
                self.c.line(right_x + 10, y, right_x + right_w - 10, y)
        
        # Bottom: mood/gratitude
        self.c.setFillColor(HexColor("#F5F2ED"))
        self.c.roundRect(40, 90, left_w, 110, 5, fill=1, stroke=1)
        self.c.setFillColor(PRIMARY)
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(50, 180, "Mood:")
        self.c.drawString(50, 150, "Grateful for:")
        
        # Mood circles
        for i in range(5):
            self.c.setStrokeColor(SUBTLE)
            self.c.setFillColor(white)
            self.c.circle(90 + i * 25, 177, 8, fill=1, stroke=1)
        
        self.c.setStrokeColor(SUBTLE)
        self.c.setLineWidth(0.3)
        self.c.line(50, 138, 40 + left_w - 10, 138)
        
        self._draw_tab_navigation("daily")
        self._finish_page()
    
    def draw_notes_page(self):
        """Draw a blank notes page with lines."""
        self.page_map.setdefault("notes", self.page_count)
        
        self._draw_background()
        self._draw_header("Notes", "Free writing space")
        
        self.c.setFillColor(white)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(40, 90, PAGE_W - 80, PAGE_H - 170, 5, fill=1, stroke=1)
        
        # Lined paper effect
        self.c.setStrokeColor(SUBTLE)
        self.c.setLineWidth(0.3)
        for y in range(int(PAGE_H) - 130, 100, -25):
            self.c.line(55, y, PAGE_W - 55, y)
        
        self._draw_tab_navigation("notes")
        self._finish_page()
    
    def generate(self, output_path):
        """Generate the complete planner PDF."""
        # Index page
        self.draw_index_page()
        
        # Generate months
        current_year = self.year
        current_month = self.start_month
        for mi in range(self.num_months):
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            # Monthly page
            self.draw_monthly_page(current_year, current_month)
            
            # Weekly pages for this month
            cal = calendar.Calendar(firstweekday=0 if self.week_starts_monday else 6)
            weeks_seen = set()
            week_num = 1
            for week in cal.monthdatescalendar(current_year, current_month):
                # Only include weeks that have days in this month
                has_current_month = any(d.month == current_month for d in week)
                if has_current_month and id(week) not in weeks_seen:
                    self.draw_weekly_page(current_year, current_month, week_num, week)
                    weeks_seen.add(id(week))
                    week_num += 1
            
            # Daily pages - only for this month's days
            for d in self._get_month_dates(current_year, current_month):
                self.draw_daily_page(d)
            
            current_month += 1
        
        # Notes pages (3 extra)
        for _ in range(3):
            self.draw_notes_page()
        
        # Save the base PDF
        self.c.save()
        self.pages_buffer.seek(0)
        
        # Now add hyperlinks using pypdf
        reader = PdfReader(self.pages_buffer)
        writer = PdfWriter()
        
        for i, page in enumerate(reader.pages):
            writer.add_page(page)
        
        # Add internal link annotations on the index page
        # Split the index page into 4 clickable quadrants for navigation
        if len(writer.pages) > 0:
            page0 = writer.pages[0]
            page_w = float(page0.mediabox.width)
            page_h = float(page0.mediabox.height)
            
            def make_link_dict(rect, target_page_idx):
                """Create a link annotation dict in pypdf's expected format.
                pypdf's add_annotation resolves target_page_index to proper IndirectReference."""
                return {
                    "/Subtype": "/Link",
                    "/Rect": rect,
                    "/Dest": {
                        "target_page_index": target_page_idx,
                        "fit": "/XYZ",
                        "fit_args": [0, page_h, 1.0],
                    },
                }
            
            # Index page: 4 quadrant navigation links
            positions = [
                (0.0, 0.5, 0.5, 1.0),  # top-left -> months
                (0.5, 0.5, 1.0, 1.0),  # top-right -> weekly
                (0.0, 0.0, 0.5, 0.5),  # bottom-left -> daily
                (0.5, 0.0, 1.0, 0.5),  # bottom-right -> notes
            ]
            section_order = ["months", "weekly", "daily", "notes"]
            
            for si, sk in enumerate(section_order):
                if sk in self.page_map:
                    target_idx = self.page_map[sk]
                    x0, y0, x1, y1 = positions[si]
                    rect = [x0 * page_w, y0 * page_h, x1 * page_w, y1 * page_h]
                    writer.add_annotation(page_number=0, annotation=make_link_dict(rect, target_idx))
            
            # Add tab navigation links to EVERY page (bottom tabs)
            # Tab positions match _draw_tab_navigation: 5 tabs at bottom
            tab_labels = ["index", "months", "weekly", "daily", "notes"]
            # Tab y-coordinates match _draw_tab_navigation (y=20, height=28)
            tab_y0 = 15  # Slightly wider hit area than visible
            tab_y1 = 55
            tab_w = (page_w - 80) / 5
            
            for page_idx in range(len(writer.pages)):
                for ti, section in enumerate(tab_labels):
                    if section in self.page_map:
                        target_idx = self.page_map[section]
                        tx0 = 40 + ti * tab_w
                        tx1 = tx0 + tab_w - 5
                        writer.add_annotation(page_number=page_idx, annotation=make_link_dict([tx0, tab_y0, tx1, tab_y1], target_idx))

        
        # Add bookmarks
        # Index
        writer.add_outline_item("Index", 0)
        
        current_year = self.year
        current_month = self.start_month
        page_tracker = 1  # After index
        
        for mi in range(self.num_months):
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            month_name = calendar.month_name[current_month]
            month_start_page = page_tracker
            writer.add_outline_item(f"{month_name} {current_year}", month_start_page)
            
            # Count pages for this month: 1 monthly + N weeks + D days
            cal = calendar.Calendar(firstweekday=0 if self.week_starts_monday else 6)
            weeks = list(cal.monthdatescalendar(current_year, current_month))
            weeks_in_month = sum(1 for w in weeks if any(d.month == current_month for d in w))
            days_in_month = calendar.monthrange(current_year, current_month)[1]
            
            page_tracker += 1 + weeks_in_month + days_in_month
            
            current_month += 1
        
        # Notes
        writer.add_outline_item("Notes", page_tracker)
        
        with open(output_path, "wb") as f:
            writer.write(f)
        
        return self.page_count



if __name__ == "__main__":
    import sys
    
    # Default: 6-month planner (Jan-Jun 2026) for reasonable size
    # Full 24-month is also supported but generates a large file
    months = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    year = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    
    gen = PlannerGenerator(
        year=year,
        start_month=1,
        num_months=months,
        week_starts_monday=True,
        theme_name="Minimalist Aesthetic",
    )
    
    output = f"planner_{year}_{months}month_hyperlinked.pdf"
    count = gen.generate(output)
    print(f"Generated: {output}")
    print(f"Total pages: {count + 1}")
    print(f"Features: Monthly grids, Weekly spreads, Daily pages with schedule, Notes, Hyperlinked index, Bookmarks")
