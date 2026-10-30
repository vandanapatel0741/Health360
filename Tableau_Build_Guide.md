# Health360 – Tableau Build Guide (follow in order)

Tools: Tableau Desktop / Tableau Public, file `data/health360_clean.csv`

## 1. Data Collection & Extraction
- Tableau > Connect > Text file > `health360_raw.csv` (shows source) – then connect `health360_clean.csv` for dashboards.
- Raw data has 2015 rows (15 duplicates, 75 missing values).

## 2. Data Preparation (already done in scripts/generate_and_prepare.py)
Duplicates removed, missing BMI/Cholesterol/Glucose filled with median, derived: Age_Group, BMI_Category, BP_Category, Any_Disease, Disease_Count, Risk_Score, Risk_Level.
In Tableau: set Patient_ID = Dimension; Fatigue/Dizziness/Chest_Pain/Heart_Disease/Diabetes/Stroke = Measure (Sum).
Calculated fields:
- `Disease Prevalence %` = SUM([Any_Disease]) / COUNT([Patient_ID])
- `Heart %` = SUM([Heart_Disease])/COUNT([Patient_ID]) (same for Diabetes, Stroke)
- `High Risk Patients` = SUM(IF [Risk_Level]="High" THEN 1 ELSE 0 END)

## 3. Data Visualization (one sheet each)
1. KPI cards: Total Patients, High-Risk Patients, Heart %, Diabetes %, Stroke %
2. Disease by Age_Group – clustered bar (Heart/Diabetes/Stroke via Measure Names)
3. Disease by BMI_Category – stacked bar
4. BP / Cholesterol / Glucose vs Age – scatter, colour = Risk_Level
5. Lifestyle heatmap – Rows: Smoking, Columns: Exercise_Level, Colour: Disease Prevalence %
6. Alcohol vs Disease – bar
7. Symptom prevalence (Fatigue, Dizziness, Chest_Pain) – bar
8. Risk_Level distribution – donut/pie
9. Trend analysis – line: Age vs Disease Prevalence %

## 4. Dashboards (map to scenarios)
- **Dashboard 1 – Clinical Risk Overview (Dr. Michael Carter):** sheets 1, 4, 8 + filters Age_Group, Gender, Risk_Level; KPIs on top; highlight table of High-risk patients.
- **Dashboard 2 – Lifestyle Analysis (Emily Rodriguez):** sheets 5, 6, 9, 7 + filters Smoking, Alcohol, Exercise_Level.
- **Dashboard 3 – Public Health (Dr. Priya Nair):** sheets 2, 3, 7 + BMI/Age filters.
Use Dashboard Actions > Filter (Use as Filter) so clicking one chart filters the rest. Layout: Automatic/Device-friendly.

## 5. Story
Tableau > New Story (5 points): 1 Problem & KPIs → 2 Age & BMI effect → 3 Lifestyle effect → 4 Symptoms & high-risk patients → 5 Recommendations (early screening, lifestyle programs, resource allocation).

## 6. Performance Testing
Use Extract (.hyper) instead of live; hide unused fields; fewer filters (use "Apply to context"); Help > Settings and Performance > Start Performance Recording; target load < 5 sec. Note findings in documentation.

## 7. Web Integration
Publish: Server > Tableau Public > Save to Tableau Public (account required). Then Share > copy "Embed code" and paste in `web/index.html` (placeholder provided).

## 8. Demonstration & Documentation
Record 3–5 min screen demo (dashboards, filters, story), upload to Drive/YouTube (unlisted) → that is the **Demo Link**. Push this folder to GitHub → **GitHub Link**.
