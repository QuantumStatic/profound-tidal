# tidal/calendar_model.py
# month numbers are 1-12. Each entry: month -> (multiplier, cause)
# multiplier > 1 = spike, < 1 = trough. Rebalanced: dollar stories lead.

DRIVERS = {
    "Pricing":     {1: (1.3, "Q1 budgets unlock"), 10: (1.4, "Q4 procurement planning"),
                    11: (1.3, "year-end plan reviews"), 12: (1.4, "fiscal year-end reviews"), 2: (0.85, "post-budget lull")},
    "Enterprise":  {1: (1.3, "Q1 budgets unlock"), 10: (1.4, "Q4 procurement planning"), 12: (1.3, "fiscal year-end reviews")},
    "Support":     {11: (1.4, "holiday e-commerce ramp"), 12: (1.5, "holiday peak support demand")},
    "Vision":      {6: (1.2, "summer creative projects"), 11: (1.3, "holiday creative"), 12: (1.3, "holiday creative")},
    "API":         {5: (1.3, "Google I/O launch season"), 10: (1.4, "OpenAI DevDay"), 11: (1.2, "re:Invent")},
    "Coding":      {3: (1.2, "spring hackathon season"), 5: (1.3, "model-launch season"), 9: (1.2, "fall dev conferences")},
    "Reasoning":   {5: (1.2, "benchmark-drop season"), 10: (1.2, "new reasoning-model releases")},
    "Speed":       {5: (1.2, "new inference hardware"), 10: (1.2, "launch season")},
    "Writing":     {1: (1.3, "new-year content planning"), 11: (1.2, "NaNoWriMo")},
    "Privacy":     {1: (1.2, "Data Privacy Day"), 5: (1.2, "regulation milestones")},
    "Safety":      {5: (1.2, "regulation milestones"), 12: (1.1, "year-end safety reviews")},
    "Translation": {6: (1.3, "summer travel"), 7: (1.4, "peak travel season"), 8: (1.2, "late-summer travel")},
    "Education":   {8: (1.3, "back-to-school ramp"), 9: (1.4, "peak study season"),
                    12: (1.3, "December finals"), 5: (1.2, "spring finals"), 6: (0.8, "school's out")},
    "Math":        {9: (1.3, "back-to-school"), 10: (1.2, "midterms"), 12: (1.2, "finals"), 3: (1.2, "midterms"), 6: (0.8, "classrooms empty")},
    "Research":    {9: (1.3, "fall semester"), 2: (1.2, "spring deadlines"), 4: (1.2, "grant deadlines")},
}
