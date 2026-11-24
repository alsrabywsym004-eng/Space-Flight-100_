
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import (
    Color, Rectangle, Ellipse, Line,
    RoundedRectangle, Triangle
)
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
import random
import json
import os
import math

Window.clearcolor = (0.015, 0.02, 0.08, 1)


class SpaceGame(Widget):

    GROUND_Y = 65
    TOP_MARGIN = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen = "menu"

        self.level = 1
        self.unlocked = 1

        self.player_x = 100
        self.player_y = 300
        self.velocity = 0

        self.thrust = False
        self.flight_touch = None
        self.fail_reason = ""

        self.rockets = []
        self.spawn_timer = 0

        self.elapsed = 0
        self.duration = 30

        self.stage_scroll = 0

        self.fireworks = []
        self.firework_timer = 0
        self.win_time = 0

        app = App.get_running_app()
        self.save_file = os.path.join(
            app.user_data_dir,
            "space_progress.json"
        )

        self.load_progress()

        Clock.schedule_interval(self.update, 1 / 60)
        self.bind(size=self.draw)

    # ---------------- SAVE ----------------

    def load_progress(self):
        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.unlocked = max(
                    1, min(100, int(data.get("unlocked", 1)))
                )
        except:
            self.unlocked = 1

    def save_progress(self):
        try:
            with open(self.save_file, "w") as f:
                json.dump({"unlocked": self.unlocked}, f)
        except:
            pass

    # ---------------- TEXT ----------------

    def text(self, message, x, y, size=20,
             color=(1, 1, 1, 1)):

        label = CoreLabel(
            text=str(message),
            font_size=size,
            color=color,
            bold=True
        )

        label.refresh()
        texture = label.texture

        Color(1, 1, 1, 1)

        Rectangle(
            texture=texture,
            pos=(
                x - texture.width / 2,
                y - texture.height / 2
            ),
            size=texture.size
        )

    def circle_button(self, x, y, radius,
                      color, label, size=20):

        Color(*color)

        Ellipse(
            pos=(x - radius, y - radius),
            size=(radius * 2, radius * 2)
        )

        Color(0.8, 0.9, 1, 1)

        Line(
            circle=(x, y, radius),
            width=2.5
        )

        self.text(label, x, y, size)

    # ---------------- BACKGROUND ----------------

    def background(self):

        w = self.width
        h = self.height

        Color(0.015, 0.025, 0.11, 1)
        Rectangle(pos=(0, 0), size=(w, h))

        for i in range(65):

            x = (i * 97 + 23) % max(1, int(w))
            y = (i * 151 + 47) % max(1, int(h))

            Color(0.65, 0.8, 1, 0.65)

            Ellipse(
                pos=(x, y),
                size=(2.5, 2.5)
            )

        Color(0.15, 0.2, 0.5, 0.45)

        Ellipse(
            pos=(w * 0.68, h * 0.72),
            size=(w * 0.38, w * 0.38)
        )

        Color(0.25, 0.35, 0.8, 0.4)

        Ellipse(
            pos=(w * 0.73, h * 0.77),
            size=(w * 0.27, w * 0.27)
        )

    # ---------------- SPACE PLANE ----------------

    def draw_plane(self, x, y):

        Color(0.05, 0.65, 1, 0.35)

        Ellipse(
            pos=(x - 18, y - 43),
            size=(36, 45)
        )

        if self.thrust:

            Color(1, 0.35, 0.02, 1)

            Triangle(
                points=[
                    x - 10, y - 32,
                    x + 10, y - 32,
                    x, y - 65
                ]
            )

            Color(1, 0.9, 0.1, 1)

            Triangle(
                points=[
                    x - 5, y - 35,
                    x + 5, y - 35,
                    x, y - 54
                ]
            )

        Color(0.05, 0.55, 0.95, 1)

        Triangle(
            points=[
                x - 12, y + 5,
                x - 48, y - 25,
                x - 12, y - 20
            ]
        )

        Triangle(
            points=[
                x + 12, y + 5,
                x + 48, y - 25,
                x + 12, y - 20
            ]
        )

        Color(0.75, 0.85, 1, 1)

        Ellipse(
            pos=(x - 15, y - 35),
            size=(30, 72)
        )

        Color(0.05, 0.65, 1, 1)

        Triangle(
            points=[
                x - 15, y + 20,
                x + 15, y + 20,
                x, y + 48
            ]
        )

        Color(0.01, 0.12, 0.28, 1)

        Ellipse(
            pos=(x - 8, y + 1),
            size=(16, 24)
        )

        Color(0.05, 0.9, 1, 1)

        Line(
            points=[
                x - 4, y - 20,
                x - 4, y + 20
            ],
            width=2
        )

        Line(
            points=[
                x + 4, y - 20,
                x + 4, y + 20
            ],
            width=2
        )

    # ---------------- ROCKETS ----------------

    def draw_rocket(self, rocket):

        x = rocket["x"]
        y = rocket["y"]

        Color(1, 0.12, 0.03, 0.25)

        Ellipse(
            pos=(x - 35, y - 12),
            size=(70, 24)
        )

        Color(0.75, 0.12, 0.12, 1)

        RoundedRectangle(
            pos=(x - 25, y - 9),
            size=(50, 18),
            radius=[7]
        )

        Color(1, 0.45, 0.08, 1)

        Triangle(
            points=[
                x - 23, y - 9,
                x - 23, y + 9,
                x - 39, y
            ]
        )

        Color(0.15, 0.75, 1, 1)

        Ellipse(
            pos=(x - 5, y - 4),
            size=(9, 8)
        )

        Color(1, 0.65, 0.05, 1)

        Triangle(
            points=[
                x + 24, y - 5,
                x + 24, y + 5,
                x + 40, y
            ]
        )

    # ---------------- FIREWORKS ----------------

    def create_firework(self):

        x = random.uniform(
            self.width * 0.15,
            self.width * 0.85
        )

        y = random.uniform(
            self.height * 0.35,
            self.height * 0.85
        )

        colors = [
            (1, 0.2, 0.2),
            (1, 0.8, 0.1),
            (0.1, 0.9, 1),
            (0.3, 1, 0.4),
            (1, 0.3, 0.9),
            (1, 1, 1)
        ]

        color = random.choice(colors)

        for i in range(24):

            angle = (math.pi * 2 * i) / 24
            speed = random.uniform(75, 190)

            self.fireworks.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.uniform(0.8, 1.5),
                "color": color,
                "size": random.uniform(3, 6)
            })

    def update_fireworks(self, dt):

        if self.screen != "win":
            return

        self.win_time += dt
        self.firework_timer += dt

        if self.firework_timer >= 0.35:

            self.firework_timer = 0
            self.create_firework()

        for particle in self.fireworks[:]:

            particle["x"] += particle["vx"] * dt
            particle["y"] += particle["vy"] * dt

            particle["vy"] -= 110 * dt
            particle["life"] -= dt

            if particle["life"] <= 0:
                self.fireworks.remove(particle)

    def draw_fireworks(self):

        for particle in self.fireworks:

            r, g, b = particle["color"]

            alpha = min(
                1,
                max(0, particle["life"])
            )

            Color(r, g, b, alpha)

            Ellipse(
                pos=(
                    particle["x"] - particle["size"] / 2,
                    particle["y"] - particle["size"] / 2
                ),
                size=(
                    particle["size"],
                    particle["size"]
                )
            )

    # ---------------- STAGES ----------------

    def start_stage(self, level):

        if level > self.unlocked:
            return

        self.level = level

        self.player_x = self.width * 0.23

        self.player_y = max(
            130, self.height * 0.55
        )

        self.velocity = 0
        self.thrust = False
        self.flight_touch = None
        self.fail_reason = ""

        self.rockets = []
        self.spawn_timer = 0

        self.elapsed = 0

        self.duration = 30 + (level - 1) * 5

        self.fireworks = []
        self.firework_timer = 0
        self.win_time = 0

        self.screen = "game"

    def finish_stage(self):

        self.screen = "win"

        self.thrust = False
        self.flight_touch = None

        self.fireworks = []
        self.firework_timer = 0
        self.win_time = 0

        for i in range(4):
            self.create_firework()

        if self.level < 100:

            self.unlocked = max(
                self.unlocked,
                self.level + 1
            )

        self.save_progress()

    def lose_stage(self, reason):

        self.screen = "over"

        self.thrust = False
        self.flight_touch = None
        self.velocity = 0

        self.fail_reason = reason

    def restart_stage(self):
        self.start_stage(self.level)

    # ---------------- GAME UPDATE ----------------

    def update(self, dt):

        dt = min(dt, 0.035)

        if self.screen == "win":

            self.update_fireworks(dt)
            self.draw()
            return

        if self.screen != "game":
            return

        # حركة الطائرة

        if self.thrust:
            self.velocity += 1700 * dt
        else:
            self.velocity -= 1900 * dt

        self.velocity = max(
            -900,
            min(720, self.velocity)
        )

        self.player_y += self.velocity * dt

        # الأرض

        if self.player_y <= self.GROUND_Y:

            self.player_y = self.GROUND_Y

            self.lose_stage("ground")
            self.draw()
            return

        # أعلى الشاشة

        top_limit = self.height - self.TOP_MARGIN - 48

        if self.player_y >= top_limit:

            self.player_y = top_limit

            self.lose_stage("top")
            self.draw()
            return

        # الوقت

        self.elapsed += dt

        if self.elapsed >= self.duration:

            self.finish_stage()
            self.draw()
            return

        # ظهور الصواريخ بسرعة أكبر

        self.spawn_timer += dt

        spawn_delay = max(
            0.35,
            1.8 - self.level * 0.012
        )

        if self.spawn_timer >= spawn_delay:

            self.spawn_timer = 0

            rocket_y = random.uniform(
                max(90, self.height * 0.12),
                max(100, self.height * 0.88)
            )

            self.rockets.append({
                "x": self.width + 55,
                "y": rocket_y,
                "speed": 500 + self.level * 15
            })

            # صواريخ إضافية في المراحل المتقدمة

            if (
                self.level >= 10
                and random.random() < self.level / 130
            ):

                self.rockets.append({
                    "x": self.width + 120,
                    "y": random.uniform(
                        100,
                        self.height * 0.85
                    ),
                    "speed": 550 + self.level * 15
                })

        # حركة الصواريخ وفحص الاصطدام

        for rocket in self.rockets[:]:

            rocket["x"] -= rocket["speed"] * dt

            dx = abs(
                rocket["x"] - self.player_x
            )

            dy = abs(
                rocket["y"] - self.player_y
            )

            if dx < 39 and dy < 30:

                self.lose_stage("rocket")
                self.draw()
                return

            if rocket["x"] < -100:

                self.rockets.remove(rocket)

        self.draw()

    # ---------------- MENU ----------------

    def draw_menu(self):

        w = self.width
        h = self.height

        self.background()

        self.text(
            "SPACE FLIGHT",
            w / 2, h - 42, 28
        )

        self.text(
            "100 SPACE MISSIONS",
            w / 2, h - 82, 18,
            (0.1, 0.85, 1, 1)
        )

        self.text(
            "OPEN: " + str(self.unlocked) + " / 100",
            w / 2, h - 120, 18
        )

        cols = 3

        radius = min(48, w / 7)
        gap_x = w / cols
        gap_y = radius * 2.75

        top = h - 200

        for level in range(1, 101):

            row = (level - 1) // cols
            col = (level - 1) % cols

            x = gap_x * (col + 0.5)
            y = top - row * gap_y + self.stage_scroll

            if y < 50 or y > h - 155:
                continue

            if level <= self.unlocked:
                color = (0.02, 0.48, 0.85, 1)
            else:
                color = (0.22, 0.24, 0.31, 1)

            self.circle_button(
                x, y, radius,
                color, str(level), 25
            )

            if level > self.unlocked:

                self.text(
                    "LOCKED",
                    x, y - radius - 12, 10,
                    (0.8, 0.8, 0.85, 1)
                )

        self.circle_button(
            w - 38, 38, 23,
            (0.8, 0.08, 0.08, 1),
            "X", 20
        )

        self.text(
            "اسحب للأعلى لرؤية باقي المراحل",
            w / 2, 15, 12
        )

    # ---------------- GAME SCREEN ----------------

    def draw_game(self):

        w = self.width
        h = self.height

        self.background()

        Color(0.08, 0.12, 0.22, 1)

        Rectangle(
            pos=(0, 0),
            size=(w, 9)
        )

        Color(0.05, 0.75, 1, 1)

        Rectangle(
            pos=(0, 9),
            size=(w, 3)
        )

        for rocket in self.rockets:
            self.draw_rocket(rocket)

        self.draw_plane(
            self.player_x,
            self.player_y
        )

        Color(0.01, 0.02, 0.08, 0.85)

        RoundedRectangle(
            pos=(8, h - 77),
            size=(w - 16, 65),
            radius=[12]
        )

        self.text(
            "STAGE " + str(self.level),
            w * 0.22, h - 35, 15
        )

        remaining = max(
            0, int(self.duration - self.elapsed)
        )

        self.text(
            "TIME: " + str(remaining),
            w * 0.63, h - 35, 16
        )

        progress = min(
            1,
            self.elapsed / self.duration
        )

        Color(0.15, 0.17, 0.25, 1)

        RoundedRectangle(
            pos=(20, 22),
            size=(w - 40, 10),
            radius=[5]
        )

        Color(0.02, 0.8, 1, 1)

        RoundedRectangle(
            pos=(20, 22),
            size=(
                max(1, (w - 40) * progress),
                10
            ),
            radius=[5]
        )

        self.circle_button(
            w - 40, h - 112, 27,
            (0.8, 0.45, 0.04, 1),
            "II", 19
        )

        if self.thrust:

            self.text(
                "ENGINE ON",
                w / 2, h - 105, 15,
                (0.1, 0.9, 1, 1)
            )

    # ---------------- PAUSE ----------------

    def pause_positions(self):

        cx = self.width / 2
        cy = self.height / 2

        return [
            (cx, cy + 105),
            (cx, cy),
            (cx, cy - 105)
        ]

    def draw_pause(self):

        self.draw_game()

        Color(0, 0, 0, 0.85)

        Rectangle(
            pos=(0, 0),
            size=self.size
        )

        self.text(
            "PAUSED",
            self.width / 2,
            self.height / 2 + 205,
            30
        )

        labels = [
            ("PLAY", "مواصلة"),
            ("RETRY", "إعادة"),
            ("STAGES", "المراحل")
        ]

        colors = [
            (0.02, 0.65, 0.25, 1),
            (0.1, 0.4, 0.9, 1),
            (0.75, 0.12, 0.15, 1)
        ]

        for i, (x, y) in enumerate(
            self.pause_positions()
        ):

            self.circle_button(
                x, y, 43,
                colors[i],
                labels[i][0], 14
            )

            self.text(
                labels[i][1],
                x, y - 60, 13
            )

    # ---------------- WIN / LOSE ----------------

    def draw_result(self):

        w = self.width
        h = self.height

        self.background()

        if self.screen == "win":

            self.draw_fireworks()

            self.text(
                "★ VICTORY ★",
                w / 2, h * 0.76, 31,
                (1, 0.85, 0.05, 1)
            )

            self.text(
                "MISSION COMPLETE!",
                w / 2, h * 0.66, 22,
                (0.1, 1, 0.5, 1)
            )

            self.text(
                "تم اجتياز المرحلة",
                w / 2, h * 0.57, 19,
                (1, 0.8, 0.2, 1)
            )

            self.text(
                "STAGE " + str(self.level),
                w / 2, h * 0.50, 18,
                (0.2, 0.85, 1, 1)
            )

            button_label = (
                "NEXT" if self.level < 100 else "MENU"
            )

        else:

            self.text(
                "MISSION FAILED!",
                w / 2, h * 0.70, 29,
                (1, 0.15, 0.12, 1)
            )

            if self.fail_reason == "ground":
                reason = "سقطت الطائرة على الأرض!"
            elif self.fail_reason == "top":
                reason = "اصطدمت الطائرة بسقف الفضاء!"
            else:
                reason = "اصطدمت الطائرة بصاروخ!"

            self.text(
                reason,
                w / 2, h * 0.60, 17
            )

            button_label = "RETRY"

        self.circle_button(
            w / 2, h * 0.40, 48,
            (0.02, 0.55, 0.9, 1),
            button_label, 16
        )

        self.circle_button(
            w / 2, h * 0.22, 42,
            (0.25, 0.3, 0.65, 1),
            "STAGES", 13
        )

    # ---------------- DRAW ----------------

    def draw(self, *args):

        self.canvas.clear()

        with self.canvas:

            if self.screen == "menu":
                self.draw_menu()

            elif self.screen == "game":
                self.draw_game()

            elif self.screen == "paused":
                self.draw_pause()

            elif self.screen in ("win", "over"):
                self.draw_result()

    # ---------------- TOUCH ----------------

    def on_touch_down(self, touch):

        x, y = touch.pos

        w = self.width
        h = self.height

        if self.screen == "menu":

            if y < 70 and x > w - 80:
                App.get_running_app().stop()
                return True

            cols = 3

            radius = min(48, w / 7)
            gap_x = w / cols
            gap_y = radius * 2.75

            top = h - 200

            for level in range(1, 101):

                row = (level - 1) // cols
                col = (level - 1) % cols

                cx = gap_x * (col + 0.5)
                cy = top - row * gap_y + self.stage_scroll

                if math.hypot(x - cx, y - cy) <= radius + 5:

                    if level <= self.unlocked:
                        self.start_stage(level)
                        self.draw()

                    return True

            touch.ud["scroll_y"] = y
            touch.ud["drag"] = False

            return True

        if self.screen == "game":

            pause_x = w - 40
            pause_y = h - 112

            if math.hypot(
                x - pause_x,
                y - pause_y
            ) <= 32:

                self.screen = "paused"

                self.thrust = False
                self.flight_touch = None

                self.draw()
                return True

            self.thrust = True
            self.flight_touch = touch.uid

            if self.velocity < 260:
                self.velocity = 260

            return True

        if self.screen == "paused":

            for i, (cx, cy) in enumerate(
                self.pause_positions()
            ):

                if math.hypot(x - cx, y - cy) < 49:

                    if i == 0:
                        self.screen = "game"

                    elif i == 1:
                        self.restart_stage()

                    else:
                        self.screen = "menu"
                        self.stage_scroll = 0

                    self.draw()
                    return True

            return True

        if self.screen in ("win", "over"):

            if abs(x - w / 2) < 95:

                if h * 0.32 < y < h * 0.48:

                    if self.screen == "win":

                        if self.level < 100:
                            self.start_stage(self.level + 1)
                        else:
                            self.screen = "menu"

                    else:
                        self.restart_stage()

                    self.draw()
                    return True

                if h * 0.15 < y < h * 0.29:

                    self.screen = "menu"
                    self.stage_scroll = 0

                    self.draw()
                    return True

            return True

        return True

    def on_touch_move(self, touch):

        y = touch.pos[1]

        if self.screen == "game":

            if self.flight_touch == touch.uid:
                self.thrust = True

            return True

        if self.screen == "menu":

            if "scroll_y" in touch.ud:

                old_y = touch.ud["scroll_y"]
                difference = y - old_y

                if abs(difference) > 3:
                    touch.ud["drag"] = True

                if touch.ud["drag"]:

                    self.stage_scroll += difference

                    radius = min(
                        48, self.width / 7
                    )

                    gap_y = radius * 2.75

                    max_scroll = max(
                        0,
                        34 * gap_y - self.height + 230
                    )

                    self.stage_scroll = max(
                        0,
                        min(
                            max_scroll,
                            self.stage_scroll
                        )
                    )

                    touch.ud["scroll_y"] = y
                    self.draw()

            return True

        return True

    def on_touch_up(self, touch):

        if self.flight_touch == touch.uid:

            self.thrust = False
            self.flight_touch = None

            return True

        return True


class SpaceApp(App):

    def build(self):

        self.title = "Space Flight 100"
        return SpaceGame()


if __name__ == "__main__":
    SpaceApp().run()
