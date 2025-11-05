import numpy as np
import imageio_ffmpeg as ffmpeg
from manim import *

class LassoRegressionAnimation(Scene):
    """
    An animation to explain the intuition behind Lasso Regression
    by visualizing the interplay between the RSS ellipses and the
    L1 penalty diamond constraint.
    """
    def construct(self):
        # --- CONFIGURATION ---
        # Set up the coordinate system and colors
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            axis_config={"color": BLUE, "include_tip": False},
            x_length=7,
            y_length=7,
        ).add_coordinates()
        
        # Labels for the axes, representing model coefficients
        beta_1_label = axes.get_x_axis_label(MathTex(r"\beta_1"), edge=DOWN, direction=DOWN)
        beta_2_label = axes.get_y_axis_label(MathTex(r"\beta_2"), edge=LEFT, direction=LEFT)
        
        # --- SCENE 1: INTRODUCTION ---
        title = Title("Lasso Regression: Finding the Best Fit")
        self.play(Write(title))
        self.play(Create(axes), Write(beta_1_label), Write(beta_2_label))
        self.wait(1)

        # --- SCENE 2: VISUALIZING THE RSS (ERROR) ---
        # The center of the ellipses represents the Ordinary Least Squares (OLS) solution
        ols_solution_point = np.array([2.5, 2])
        ols_dot = Dot(axes.c2p(*ols_solution_point), color=RED)
        ols_label = MathTex(r"\hat{\beta}_{OLS}", color=RED).next_to(ols_dot, UR, buff=0.1)

        rss_text = MathTex(r"\text{Minimize Error (RSS)}", color=YELLOW).to_corner(UL)
        self.play(Write(rss_text))
        self.play(FadeIn(ols_dot), Write(ols_label))

        # Create concentric ellipses for the RSS
        ellipses = VGroup(*[
            Ellipse(
                width=1.5 * i, height=0.75 * i, color=YELLOW, stroke_width=2
            ).move_to(axes.c2p(*ols_solution_point))
            for i in range(1, 6)
        ])
        
        self.play(Create(ellipses[0]))
        self.play(*[Create(ellipses[i]) for i in range(1, 5)], run_time=2)
        self.wait(2)
        
        self.play(FadeOut(rss_text))

        # --- SCENE 3: INTRODUCING THE LASSO CONSTRAINT ---
        lambda_val = ValueTracker(2.5) # This will control the size of the diamond

        constraint_text = MathTex(r"\text{Lasso Constraint: } |\beta_1| + |\beta_2| \leq t", color=CYAN).to_corner(UL)
        
        # Create the diamond shape for the L1 penalty
        diamond = always_redraw(lambda: Polygon(
            axes.c2p(lambda_val.get_value(), 0),
            axes.c2p(0, lambda_val.get_value()),
            axes.c2p(-lambda_val.get_value(), 0),
            axes.c2p(0, -lambda_val.get_value()),
            color=CYAN,
            fill_opacity=0.2,
            stroke_width=3
        ))
        
        self.play(Write(constraint_text))
        self.play(Create(diamond))
        self.wait(2)

        # --- SCENE 4: FINDING THE LASSO SOLUTION ---
        solution_text = Text("The Lasso solution is the first point where the ellipses touch the diamond", font_size=24).to_edge(UP)
        self.play(Transform(title, solution_text))
        
        # Point where the ellipse first touches the diamond
        lasso_solution_point = axes.c2p(lambda_val.get_value(), 0) 
        lasso_dot = Dot(lasso_solution_point, color=GREEN)
        lasso_label = MathTex(r"\hat{\beta}_{Lasso}", color=GREEN).next_to(lasso_dot, DR, buff=0.1)
        
        # Animate the first ellipse touching the diamond
        first_touch_ellipse = Ellipse(
                width=1.5 * 2.8, height=0.75 * 2.8, color=YELLOW, stroke_width=3.5
            ).move_to(axes.c2p(*ols_solution_point))

        self.play(Transform(ellipses, first_touch_ellipse), run_time=1.5)
        self.play(FadeIn(lasso_dot), Write(lasso_label))
        self.wait(2)

        # --- SCENE 5: FEATURE SELECTION ---
        feature_selection_text = MathTex(
            r"\text{Notice: } \beta_2 = 0",
            r"\\ \text{Lasso performs feature selection!}",
            color=WHITE
        ).next_to(constraint_text, DOWN, buff=0.2).align_to(constraint_text, LEFT)
        
        # Highlight the zero coefficient
        zero_line = Line(axes.c2p(0,0), axes.c2p(lambda_val.get_value(), 0), color=GREEN, stroke_width=6)
        self.play(Create(zero_line))
        self.play(Write(feature_selection_text))
        self.wait(3)

        self.play(FadeOut(zero_line), FadeOut(feature_selection_text), FadeOut(ellipses))
        self.wait(1)
        
        # --- SCENE 6: EFFECT OF LAMBDA ---
        lambda_effect_text = MathTex(r"\text{Increasing } \lambda \text{ shrinks the constraint}", color=ORANGE).to_corner(DL)
        self.play(Write(lambda_effect_text))
        
        # Animate lambda changing, which shrinks the diamond
        self.play(lambda_val.animate.set_value(1.0), run_time=3)
        self.wait(2)
        
        final_text = Text("Forcing more coefficients to zero", font_size=28).move_to(axes.c2p(0, 2.5))
        self.play(Write(final_text))
        self.wait(3)
