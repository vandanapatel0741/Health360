"""Health360 - data collection (synthetic extraction) + data preparation.
Output: data/health360_raw.csv, data/health360_clean.csv (Tableau-ready)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N = 2000
age = rng.integers(18, 90, N)
gender = rng.choice(["Male", "Female"], N)
bmi = np.clip(rng.normal(26 + (age-45)*0.03, 5, N), 15, 50).round(1)
sys_bp = np.clip(rng.normal(115 + (age-40)*0.5 + (bmi-25)*0.8, 14, N), 85, 210).round()
dia_bp = np.clip(sys_bp*0.62 + rng.normal(0, 6, N), 50, 130).round()
chol = np.clip(rng.normal(185 + (age-40)*0.6 + (bmi-25)*1.5, 35, N), 100, 360).round()
glucose = np.clip(rng.normal(95 + (bmi-25)*1.8 + (age-40)*0.3, 22, N), 60, 320).round()
smoking = rng.choice(["Never", "Former", "Current"], N, p=[.55, .2, .25])
alcohol = rng.choice(["None", "Moderate", "Heavy"], N, p=[.4, .45, .15])
exercise = rng.choice(["Low", "Medium", "High"], N, p=[.38, .4, .22])
fatigue = rng.random(N) < (0.15 + (glucose > 125)*0.2 + (exercise == "Low")*0.1)
dizziness = rng.random(N) < (0.1 + (sys_bp > 140)*0.2)
chest_pain = rng.random(N) < (0.08 + (chol > 240)*0.15 + (smoking == "Current")*0.08)
df = pd.DataFrame(dict(Patient_ID=[f"P{i:04d}" for i in range(1, N+1)], Age=age, Gender=gender, BMI=bmi,
    Systolic_BP=sys_bp, Diastolic_BP=dia_bp, Cholesterol=chol, Glucose=glucose, Smoking=smoking,
    Alcohol=alcohol, Exercise_Level=exercise, Fatigue=fatigue.astype(int), Dizziness=dizziness.astype(int),
    Chest_Pain=chest_pain.astype(int)))
z = lambda s: (s - s.mean())/s.std()
smk = df.Smoking.map({"Never":0,"Former":.4,"Current":1}); alc = df.Alcohol.map({"None":0,"Moderate":.2,"Heavy":.8})
ex = df.Exercise_Level.map({"Low":.8,"Medium":0,"High":-.6})
def disease(base, lin): return (rng.random(N) < 1/(1+np.exp(-(base+lin)))).astype(int)
df["Heart_Disease"] = disease(-2.6, .5*z(df.Age)+.4*z(df.Cholesterol)+.3*z(df.Systolic_BP)+.6*smk+.9*df.Chest_Pain+.3*ex)
df["Diabetes"] = disease(-2.3, .5*z(df.Glucose)+.4*z(df.BMI)+.3*z(df.Age)+.4*ex+.3*df.Fatigue)
df["Stroke"] = disease(-3.2, .5*z(df.Age)+.5*z(df.Systolic_BP)+.4*smk+.3*alc+.4*df.Dizziness)
raw = df.copy()
# inject realistic dirt in raw file
for c in ["BMI","Cholesterol","Glucose"]:
    raw.loc[rng.choice(N, 25, replace=False), c] = np.nan
raw = pd.concat([raw, raw.sample(15, random_state=1)]).sample(frac=1, random_state=2)
raw.to_csv("data/health360_raw.csv", index=False)

# ---- Data preparation ----
c = raw.drop_duplicates("Patient_ID").copy()
for col in ["BMI","Cholesterol","Glucose"]:
    c[col] = c[col].fillna(c[col].median())
c["Age_Group"] = pd.cut(c.Age, [17,29,44,59,74,120], labels=["18-29","30-44","45-59","60-74","75+"])
c["BMI_Category"] = pd.cut(c.BMI, [0,18.5,25,30,100], labels=["Underweight","Normal","Overweight","Obese"], right=False)
c["BP_Category"] = np.select([(c.Systolic_BP>=140)|(c.Diastolic_BP>=90),(c.Systolic_BP>=120)|(c.Diastolic_BP>=80)],["High","Elevated"],"Normal")
c["Any_Disease"] = ((c.Heart_Disease+c.Diabetes+c.Stroke)>0).astype(int)
c["Disease_Count"] = c.Heart_Disease+c.Diabetes+c.Stroke
score = (c.Age>=60)*2+(c.BMI>=30)*2+(c.BP_Category=="High")*2+(c.Cholesterol>=240)*2+(c.Glucose>=126)*2+(c.Smoking=="Current")*2+(c.Alcohol=="Heavy")+(c.Exercise_Level=="Low")+c.Chest_Pain+c.Dizziness+c.Fatigue
c["Risk_Score"] = score
c["Risk_Level"] = pd.cut(score,[-1,4,8,30],labels=["Low","Medium","High"])
c.to_csv("data/health360_clean.csv", index=False)
print(raw.shape, c.shape); print(c.Risk_Level.value_counts()); print(c[["Heart_Disease","Diabetes","Stroke"]].mean())
