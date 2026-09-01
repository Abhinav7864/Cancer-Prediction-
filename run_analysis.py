import os
import glob
import datetime
import pandas as pd
import numpy as np
import kagglehub

# Import all functions from tableau_functions library
from tableau_functions import (
    ABS, ROUND, SQRT, POWER, RAND, INT, FLOAT,
    UPPER, LOWER, LEN, SPLIT, LEFT, TRIM, MID, RIGHT, REPLACE, CONTAINS, STARTSWITH,
    TODAY, NOW, MAKEDATE, DATEPART, DATENAME, DATEADD, DATEDIFF, DATETRUNC,
    STR, BOOL, DATE,
    SUM, AVG, MAX, MIN, COUNT, COUNTD,
    IF_THEN_ELSE, IIF, AND_FUNC, OR_FUNC, NOT_FUNC,
    INDEX, FIRST, LAST, LOOKUP, RUNNING_SUM, WINDOW_SUM, RANK, TOTAL,
    USERNAME, FULLNAME, ISFULLNAME, ISMEMBEROF, USERDOMAIN,
    MAKEPOINT, DISTANCE, BUFFER, INTERSECTS, MAKELINE, AREA, CENTROID,
    MODEL_QUANTILE, MODEL_PERCENTILE, FORECAST, TRENDLINE
)

def format_category_table(category_name, rows_data):
    """
    Formats a category of functions into a clean ASCII table for console display.
    """
    col_widths = [28, 34, 22, 24, 12]
    headers = ["Function Signature", "Expression / Applied To", "Original Input", "Computed Output", "Output Type"]
    
    sep_line = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_line = "| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)) + " |"
    
    output = []
    output.append(f"\nCATEGORY: {category_name.upper()}")
    output.append(sep_line)
    output.append(header_line)
    output.append(sep_line)
    
    for row in rows_data:
        sig, expr, orig, comp, dtype = row
        line = f"| {str(sig):<{col_widths[0]}} | {str(expr):<{col_widths[1]}} | {str(orig):<{col_widths[2]}} | {str(comp):<{col_widths[3]}} | {str(dtype):<{col_widths[4]}} |"
        output.append(line)
        
    output.append(sep_line)
    return "\n".join(output)

def main():
    print("\n" + "=" * 128)
    print("APPENDIX CANCER PREDICTION DATASET - ALL NOTEBOOK FUNCTIONS ANALYSIS REPORT".center(128))
    print("=" * 128)
    
    print("\nStep 1: Downloading dataset via kagglehub...")
    path = kagglehub.dataset_download("ankushpanday1/appendix-cancer-prediction-dataset")
    print(f"Cache Directory : {path}")
    
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in {path}")
    
    csv_path = csv_files[0]
    df = pd.read_csv(csv_path)
    
    print(f"CSV File Loaded : {os.path.basename(csv_path)}")
    print(f"Dataset Shape   : {df.shape[0]:,} Rows x {df.shape[1]} Original Columns\n")
    
    print("=" * 128)
    print("EXECUTING ALL FUNCTIONS FROM ALL NOTEBOOK PAGES ON DATASET COLUMNS".center(128))
    print("=" * 128)

    # ----------------------------------------------------
    # 1. MATHEMATICAL / NUMBER FUNCTIONS
    # ----------------------------------------------------
    df["ABS_BMI_Deviation"] = ABS(df["BMI"] - 25.0)
    df["ROUND_Survival_Years"] = ROUND(df["Survival_Years_After_Diagnosis"], 1)
    df["SQRT_Age"] = SQRT(df["Age"])
    df["POWER_BMI_2"] = POWER(df["BMI"], 2)
    df["RAND_Score"] = RAND(len(df))
    df["INT_BMI"] = INT(df["BMI"])
    df["FLOAT_Blood_Pressure"] = FLOAT(df["Blood_Pressure"])

    math_rows = [
        ("ABS(number)", "ABS(BMI - 25.0)", f"BMI = {df['BMI'].iloc[0]}", f"{df['ABS_BMI_Deviation'].iloc[0]:.2f}", str(df['ABS_BMI_Deviation'].dtype)),
        ("ROUND(number, decimals)", "ROUND(Survival_Years, 1)", f"Survival = {df['Survival_Years_After_Diagnosis'].iloc[0]}", f"{df['ROUND_Survival_Years'].iloc[0]}", str(df['ROUND_Survival_Years'].dtype)),
        ("SQRT(number)", "SQRT(Age)", f"Age = {df['Age'].iloc[0]}", f"{df['SQRT_Age'].iloc[0]:.4f}", str(df['SQRT_Age'].dtype)),
        ("POWER(number, power)", "POWER(BMI, 2)", f"BMI = {df['BMI'].iloc[0]}", f"{df['POWER_BMI_2'].iloc[0]:.2f}", str(df['POWER_BMI_2'].dtype)),
        ("RAND()", "RAND()", "[Random Generation]", f"{df['RAND_Score'].iloc[0]:.6f}", str(df['RAND_Score'].dtype)),
        ("INT(expression)", "INT(BMI)", f"BMI = {df['BMI'].iloc[0]}", f"{df['INT_BMI'].iloc[0]}", str(df['INT_BMI'].dtype)),
        ("FLOAT(expression)", "FLOAT(Blood_Pressure)", f"BP = {df['Blood_Pressure'].iloc[0]}", f"{df['FLOAT_Blood_Pressure'].iloc[0]}", str(df['FLOAT_Blood_Pressure'].dtype)),
    ]
    print(format_category_table("1. Mathematical & Numeric Functions", math_rows))

    # ----------------------------------------------------
    # 2. STRING FUNCTIONS
    # ----------------------------------------------------
    df["UPPER_Country"] = UPPER(df["Country"])
    df["LOWER_Diet_Type"] = LOWER(df["Diet_Type"])
    df["LEN_Patient_ID"] = LEN(df["Patient_ID"])
    df["SPLIT_Patient_Num"] = SPLIT(df["Patient_ID"], "_", 2)
    df["LEFT_Patient_Prefix"] = LEFT(df["Patient_ID"], 3)
    df["TRIM_Country"] = TRIM(df["Country"])
    df["MID_Patient_ID"] = MID(df["Patient_ID"], 5, 3)
    df["RIGHT_Patient_Suffix"] = RIGHT(df["Patient_ID"], 4)
    df["REPLACE_Patient_ID"] = REPLACE(df["Patient_ID"], "PID_", "PATIENT_")
    df["CONTAINS_Vegetarian"] = CONTAINS(df["Diet_Type"], "Vegetarian")
    df["STARTSWITH_PID"] = STARTSWITH(df["Patient_ID"], "PID")

    string_rows = [
        ("UPPER(string)", "UPPER(Country)", f"Country = {df['Country'].iloc[0]}", f"{df['UPPER_Country'].iloc[0]}", str(df['UPPER_Country'].dtype)),
        ("LOWER(string)", "LOWER(Diet_Type)", f"Diet = {df['Diet_Type'].iloc[0]}", f"{df['LOWER_Diet_Type'].iloc[0]}", str(df['LOWER_Diet_Type'].dtype)),
        ("LEN(string)", "LEN(Patient_ID)", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['LEN_Patient_ID'].iloc[0]}", str(df['LEN_Patient_ID'].dtype)),
        ("SPLIT(string, delim, tok)", "SPLIT(Patient_ID, '_', 2)", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['SPLIT_Patient_Num'].iloc[0]}", str(df['SPLIT_Patient_Num'].dtype)),
        ("LEFT(string, number)", "LEFT(Patient_ID, 3)", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['LEFT_Patient_Prefix'].iloc[0]}", str(df['LEFT_Patient_Prefix'].dtype)),
        ("TRIM(string)", "TRIM(Country)", f"Country = {df['Country'].iloc[0]}", f"{df['TRIM_Country'].iloc[0]}", str(df['TRIM_Country'].dtype)),
        ("MID(string, start, len)", "MID(Patient_ID, 5, 3)", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['MID_Patient_ID'].iloc[0]}", str(df['MID_Patient_ID'].dtype)),
        ("RIGHT(string, number)", "RIGHT(Patient_ID, 4)", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['RIGHT_Patient_Suffix'].iloc[0]}", str(df['RIGHT_Patient_Suffix'].dtype)),
        ("REPLACE(string, sub, rep)", "REPLACE(Patient_ID, 'PID_')", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['REPLACE_Patient_ID'].iloc[0]}", str(df['REPLACE_Patient_ID'].dtype)),
        ("CONTAINS(string, sub)", "CONTAINS(Diet_Type, 'Veg')", f"Diet = {df['Diet_Type'].iloc[0]}", f"{df['CONTAINS_Vegetarian'].iloc[0]}", str(df['CONTAINS_Vegetarian'].dtype)),
        ("STARTSWITH(string, sub)", "STARTSWITH(Patient_ID, 'PID')", f"ID = {df['Patient_ID'].iloc[0]}", f"{df['STARTSWITH_PID'].iloc[0]}", str(df['STARTSWITH_PID'].dtype)),
    ]
    print(format_category_table("2. String & Text Functions", string_rows))

    # ----------------------------------------------------
    # 3. DATE FUNCTIONS
    # ----------------------------------------------------
    current_today = TODAY()
    current_now = NOW()
    
    df["TODAY_Date"] = current_today
    df["NOW_Timestamp"] = current_now
    df["MAKEDATE_Intake"] = MAKEDATE(2020 + (df["Age"] % 5), (df["Age"] % 12) + 1, 15)
    df["Diagnosis_Date"] = DATEADD("day", df["Diagnosis_Delay_Days"], df["MAKEDATE_Intake"])
    df["DATEPART_Year"] = DATEPART("year", df["Diagnosis_Date"])
    df["DATEPART_Month"] = DATEPART("month", df["Diagnosis_Date"])
    df["DATENAME_Month"] = DATENAME("month", df["Diagnosis_Date"])
    df["DATENAME_Day"] = DATENAME("day", df["Diagnosis_Date"])
    df["DATEADD_Followup"] = DATEADD("day", df["Survival_Years_After_Diagnosis"] * 365, df["Diagnosis_Date"])
    df["DATEDIFF_Days_Since_Diag"] = DATEDIFF("day", df["Diagnosis_Date"], pd.to_datetime(current_today))
    df["DATETRUNC_Month_Start"] = DATETRUNC("month", df["Diagnosis_Date"])

    date_rows = [
        ("TODAY()", "TODAY()", "[System Date]", str(current_today), "date"),
        ("NOW()", "NOW()", "[System Timestamp]", current_now.strftime("%Y-%m-%d %H:%M"), "datetime"),
        ("MAKEDATE(year, month, day)", "MAKEDATE(2022, 8, 15)", f"Age = {df['Age'].iloc[0]}", str(df['MAKEDATE_Intake'].iloc[0]), "date"),
        ("DATEPART(part, date)", "DATEPART('year', Diag_Date)", f"Date = {df['Diagnosis_Date'].iloc[0].strftime('%Y-%m-%d')}", f"{df['DATEPART_Year'].iloc[0]}", str(df['DATEPART_Year'].dtype)),
        ("DATENAME(part, date)", "DATENAME('month', Diag_Date)", f"Date = {df['Diagnosis_Date'].iloc[0].strftime('%Y-%m-%d')}", f"{df['DATENAME_Month'].iloc[0]}", str(df['DATENAME_Month'].dtype)),
        ("DATEADD(part, num, date)", "DATEADD('day', Survival, Date)", f"Delay = {df['Diagnosis_Delay_Days'].iloc[0]}d", str(df['DATEADD_Followup'].iloc[0].strftime("%Y-%m-%d")), "datetime64"),
        ("DATEDIFF(part, start, end)", "DATEDIFF('day', Date, TODAY)", f"Date = {df['Diagnosis_Date'].iloc[0].strftime('%Y-%m-%d')}", f"{df['DATEDIFF_Days_Since_Diag'].iloc[0]} days", str(df['DATEDIFF_Days_Since_Diag'].dtype)),
        ("DATETRUNC(part, date)", "DATETRUNC('month', Diag_Date)", f"Date = {df['Diagnosis_Date'].iloc[0].strftime('%Y-%m-%d')}", str(df['DATETRUNC_Month_Start'].iloc[0].strftime("%Y-%m-%d")), "datetime64"),
    ]
    print(format_category_table("3. Date & Time Functions", date_rows))

    # ----------------------------------------------------
    # 4. TYPE & LOGICAL CONVERSION FUNCTIONS
    # ----------------------------------------------------
    df["STR_Age"] = STR(df["Age"])
    df["BOOL_Cancer_Positive"] = BOOL(df["Appendix_Cancer_Prediction"] == "Yes")
    df["DATE_Diagnosis_Only"] = DATE(df["Diagnosis_Date"])

    type_rows = [
        ("STR(expression)", "STR(Age)", f"Age = {df['Age'].iloc[0]} (int)", f"'{df['STR_Age'].iloc[0]}' (str)", str(df['STR_Age'].dtype)),
        ("BOOL(expression)", "BOOL(Prediction == 'Yes')", f"Prediction = {df['Appendix_Cancer_Prediction'].iloc[0]}", f"{df['BOOL_Cancer_Positive'].iloc[0]}", str(df['BOOL_Cancer_Positive'].dtype)),
        ("DATE(expression)", "DATE(Diagnosis_Date)", f"Timestamp", str(df['DATE_Diagnosis_Only'].iloc[0]), "date"),
    ]
    print(format_category_table("4. Type & Logical Conversion Functions", type_rows))

    # ----------------------------------------------------
    # 5. AGGREGATION & SUMMARY FUNCTIONS (NEW FROM IMAGE 1)
    # ----------------------------------------------------
    tot_sum_bp = SUM(df["Blood_Pressure"])
    avg_bmi = AVG(df["BMI"])
    max_age = MAX(df["Age"])
    min_age = MIN(df["Age"])
    total_count = COUNT(df["Patient_ID"])
    unique_countries = COUNTD(df["Country"])

    agg_rows = [
        ("SUM(expression)", "SUM(Blood_Pressure)", f"Total Rows = {total_count:,}", f"{tot_sum_bp:,}", "int64"),
        ("AVG(expression)", "AVG(BMI)", f"Dataset BMI Series", f"{avg_bmi:.2f}", "float64"),
        ("MAX(expression)", "MAX(Age)", f"Age Range", f"{max_age} years", "int64"),
        ("MIN(expression)", "MIN(Age)", f"Age Range", f"{min_age} years", "int64"),
        ("COUNT(expression)", "COUNT(Patient_ID)", f"Patient ID Series", f"{total_count:,} patients", "int64"),
        ("COUNTD(expression)", "COUNTD(Country)", f"Country Series", f"{unique_countries} unique countries", "int64"),
    ]
    print(format_category_table("5. Aggregation & Summary Functions", agg_rows))

    # ----------------------------------------------------
    # 6. LOGICAL & CONDITIONAL FUNCTIONS (NEW FROM IMAGE 2)
    # ----------------------------------------------------
    # IF ... THEN ... ELSEIF ... ELSE ... END
    df["IF_Age_Group"] = IF_THEN_ELSE(df["Age"] >= 60, "Senior", IF_THEN_ELSE(df["Age"] >= 30, "Adult", "Youth"))
    
    # IIF(condition, true_val, false_val)
    df["IIF_High_Risk"] = IIF((df["BMI"] > 30.0) | (df["Smoking_Status"] == "Yes"), "High Risk", "Standard Risk")
    
    # AND Function
    df["AND_Senior_Smoker"] = AND_FUNC(df["Age"] >= 60, df["Smoking_Status"] == "Yes")
    
    # OR Function
    df["OR_History_Or_Mutations"] = OR_FUNC(df["Family_History_Cancer"] == "Yes", df["Genetic_Mutations"] == "Yes")
    
    # NOT Function
    df["NOT_Non_Smoker"] = NOT_FUNC(df["Smoking_Status"] == "Yes")

    logical_rows = [
        ("IF..THEN..ELSE..END", "IF Age>=60 THEN 'Senior'...", f"Age = {df['Age'].iloc[0]}", f"{df['IF_Age_Group'].iloc[0]}", str(df['IF_Age_Group'].dtype)),
        ("IIF(cond, true, false)", "IIF(BMI>30 | Smoker, High, Std)", f"BMI={df['BMI'].iloc[0]}, Smoke={df['Smoking_Status'].iloc[0]}", f"{df['IIF_High_Risk'].iloc[0]}", str(df['IIF_High_Risk'].dtype)),
        ("AND Function", "AND(Age>=60, Smoking=='Yes')", f"Age={df['Age'].iloc[0]}, Smoke={df['Smoking_Status'].iloc[0]}", f"{df['AND_Senior_Smoker'].iloc[0]}", str(df['AND_Senior_Smoker'].dtype)),
        ("OR Function", "OR(History=='Yes', Mutation=='Yes')", f"Hist={df['Family_History_Cancer'].iloc[0]}, Mut={df['Genetic_Mutations'].iloc[0]}", f"{df['OR_History_Or_Mutations'].iloc[0]}", str(df['OR_History_Or_Mutations'].dtype)),
        ("NOT Function", "NOT(Smoking == 'Yes')", f"Smoke = {df['Smoking_Status'].iloc[0]}", f"{df['NOT_Non_Smoker'].iloc[0]}", str(df['NOT_Non_Smoker'].dtype)),
    ]
    print(format_category_table("6. Logical & Conditional Functions", logical_rows))

    # ----------------------------------------------------
    # 7. TABLE CALCULATIONS & WINDOW FUNCTIONS (NEW FROM IMAGE 1)
    # ----------------------------------------------------
    df["INDEX_Row_Num"] = INDEX(df)
    df["FIRST_Row_Offset"] = FIRST(df)
    df["LAST_Row_Offset"] = LAST(df)
    df["LOOKUP_Prev_BMI"] = LOOKUP(df["BMI"], offset=-1)
    df["RUNNING_SUM_BP"] = RUNNING_SUM(df["Blood_Pressure"])
    df["WINDOW_SUM_BP"] = WINDOW_SUM(df["Blood_Pressure"])
    df["RANK_BMI"] = RANK(df["BMI"], ascending=False)
    df["TOTAL_BP"] = TOTAL(df["Blood_Pressure"])

    table_calc_rows = [
        ("INDEX()", "INDEX()", f"Row Position", f"{df['INDEX_Row_Num'].iloc[0]}", str(df['INDEX_Row_Num'].dtype)),
        ("FIRST()", "FIRST()", f"Offset to 1st row", f"{df['FIRST_Row_Offset'].iloc[0]}", str(df['FIRST_Row_Offset'].dtype)),
        ("LAST()", "LAST()", f"Offset to last row", f"{df['LAST_Row_Offset'].iloc[0]}", str(df['LAST_Row_Offset'].dtype)),
        ("LOOKUP(col, offset)", "LOOKUP(BMI, -1)", f"Prev Row BMI", f"{df['LOOKUP_Prev_BMI'].iloc[1]}", str(df['LOOKUP_Prev_BMI'].dtype)),
        ("RUNNING_SUM(col)", "RUNNING_SUM(Blood_Pressure)", f"Cumulative BP", f"{df['RUNNING_SUM_BP'].iloc[0]:,}", str(df['RUNNING_SUM_BP'].dtype)),
        ("WINDOW_SUM(col)", "WINDOW_SUM(Blood_Pressure)", f"Total Window BP", f"{df['WINDOW_SUM_BP'].iloc[0]:,}", str(df['WINDOW_SUM_BP'].dtype)),
        ("RANK(col)", "RANK(BMI, desc)", f"BMI = {df['BMI'].iloc[0]}", f"Rank #{df['RANK_BMI'].iloc[0]}", str(df['RANK_BMI'].dtype)),
        ("TOTAL(col)", "TOTAL(Blood_Pressure)", f"Dataset BP Total", f"{df['TOTAL_BP'].iloc[0]:,}", str(df['TOTAL_BP'].dtype)),
    ]
    print(format_category_table("7. Table Calculations & Window Functions", table_calc_rows))

    # ----------------------------------------------------
    # 8. USER & SECURITY FUNCTIONS (NEW FROM IMAGE 1)
    # ----------------------------------------------------
    df["USERNAME_Col"] = USERNAME()
    df["FULLNAME_Col"] = FULLNAME()
    df["ISFULLNAME_Check"] = ISFULLNAME(df["FULLNAME_Col"].iloc[0])
    df["ISMEMBEROF_Check"] = ISMEMBEROF("Cancer_Research")
    df["USERDOMAIN_Col"] = USERDOMAIN()

    user_rows = [
        ("USERNAME()", "USERNAME()", "[System User]", f"{df['USERNAME_Col'].iloc[0]}", "str"),
        ("FULLNAME()", "FULLNAME()", "[Full Name]", f"{df['FULLNAME_Col'].iloc[0]}", "str"),
        ("ISFULLNAME()", "ISFULLNAME(Fullname)", "[User Check]", f"{df['ISFULLNAME_Check'].iloc[0]}", "bool"),
        ("ISMEMBEROF(group)", "ISMEMBEROF('Cancer_Research')", "[Group Security]", f"{df['ISMEMBEROF_Check'].iloc[0]}", "bool"),
        ("USERDOMAIN()", "USERDOMAIN()", "[Network Domain]", f"{df['USERDOMAIN_Col'].iloc[0]}", "str"),
    ]
    print(format_category_table("8. User Session & Security Functions", user_rows))

    # ----------------------------------------------------
    # 9. SPATIAL & GEOGRAPHIC FUNCTIONS (NEW FROM IMAGE 1)
    # ----------------------------------------------------
    # Assign synthetic country center coordinates
    country_coords = {
        "China": (35.8617, 104.1954),
        "USA": (37.0902, -95.7129),
        "France": (46.2276, 2.2137),
        "Russia": (61.5240, 105.3188),
        "Saudi Arabia": (23.8859, 45.0792)
    }
    hospital_lat, hospital_lon = 40.7128, -74.0060 # Hospital benchmark center (NYC)
    
    df["Patient_Lat"] = df["Country"].map(lambda c: country_coords.get(c, (20.0, 0.0))[0])
    df["Patient_Lon"] = df["Country"].map(lambda c: country_coords.get(c, (20.0, 0.0))[1])
    
    df["MAKEPOINT_Patient"] = MAKEPOINT(df["Patient_Lat"], df["Patient_Lon"])
    df["DISTANCE_To_Hospital_KM"] = DISTANCE(df["Patient_Lat"], df["Patient_Lon"], hospital_lat, hospital_lon)
    df["BUFFER_Zone"] = BUFFER(df["Patient_Lat"], df["Patient_Lon"], 50.0)
    df["INTERSECTS_Check"] = INTERSECTS(df["Country"], "China")
    df["MAKELINE_To_Hospital"] = MAKELINE(df["Patient_Lat"], df["Patient_Lon"], hospital_lat, hospital_lon)
    df["AREA_Zone_KM2"] = AREA(50.0)
    df["CENTROID_Point"] = CENTROID(df["Patient_Lat"], df["Patient_Lon"], hospital_lat, hospital_lon)

    spatial_rows = [
        ("MAKEPOINT(lat, lon)", "MAKEPOINT(Lat, Lon)", f"Country = {df['Country'].iloc[0]}", f"{df['MAKEPOINT_Patient'].iloc[0]}", "str"),
        ("DISTANCE(pt1, pt2)", "DISTANCE(Patient, Hospital)", f"Country = {df['Country'].iloc[0]}", f"{df['DISTANCE_To_Hospital_KM'].iloc[0]:,.1f} km", "float64"),
        ("BUFFER(pt, radius)", "BUFFER(Patient, 50km)", f"Lat/Lon", f"{df['BUFFER_Zone'].iloc[0]}", "str"),
        ("INTERSECTS(g1, g2)", "INTERSECTS(Country, 'China')", f"Country = {df['Country'].iloc[0]}", f"{df['INTERSECTS_Check'].iloc[0]}", "bool"),
        ("MAKELINE(pt1, pt2)", "MAKELINE(Patient, Hospital)", f"Lat/Lon -> Hospital", f"{df['MAKELINE_To_Hospital'].iloc[0][:30]}...", "str"),
        ("AREA(radius_km)", "AREA(50km)", f"Radius = 50 km", f"{df['AREA_Zone_KM2'].iloc[0]:,.2f} sq km", "float64"),
        ("CENTROID(pt1, pt2)", "CENTROID(Patient, Hospital)", f"Midpoint", f"{df['CENTROID_Point'].iloc[0]}", "str"),
    ]
    print(format_category_table("9. Spatial & Geographic Functions", spatial_rows))

    # ----------------------------------------------------
    # 10. PREDICTIVE & STATISTICAL ANALYTICS (NEW FROM IMAGE 1)
    # ----------------------------------------------------
    median_bmi = MODEL_QUANTILE(df["BMI"], 0.5)
    df["MODEL_PERCENTILE_BMI"] = MODEL_PERCENTILE(df["BMI"])
    survival_forecast = FORECAST(df["Survival_Years_After_Diagnosis"].head(1000), periods=1)
    age_survival_slope = TRENDLINE(df["Age"].head(1000), df["Survival_Years_After_Diagnosis"].head(1000))

    df["MODEL_QUANTILE_BMI_Median"] = median_bmi
    df["FORECAST_Survival_Next"] = survival_forecast
    df["TRENDLINE_Slope"] = age_survival_slope

    predictive_rows = [
        ("MODEL_QUANTILE(col, q)", "MODEL_QUANTILE(BMI, 0.5)", f"BMI Median", f"{median_bmi:.2f}", "float64"),
        ("MODEL_PERCENTILE(col)", "MODEL_PERCENTILE(BMI)", f"BMI = {df['BMI'].iloc[0]}", f"Top {df['MODEL_PERCENTILE_BMI'].iloc[0]*100:.1f}%", "float64"),
        ("FORECAST(col, periods)", "FORECAST(Survival, 1)", f"Survival History", f"{survival_forecast:.2f} yrs", "float64"),
        ("TRENDLINE(x, y)", "TRENDLINE(Age, Survival)", f"Age vs Survival", f"Slope: {age_survival_slope:.4f}", "float64"),
    ]
    print(format_category_table("10. Predictive & Statistical Analytics Functions", predictive_rows))

    # ----------------------------------------------------
    # SAMPLE DATASET PREVIEW
    # ----------------------------------------------------
    print("\n" + "=" * 128)
    print("SAMPLE DATASET PREVIEW (FIRST 5 PATIENTS x KEY CALCULATED FIELDS FROM ALL CATEGORIES)".center(128))
    print("=" * 128 + "\n")
    
    preview_cols = [
        "Patient_ID", "Country", "Age", "BMI", "ABS_BMI_Deviation", 
        "UPPER_Country", "SPLIT_Patient_Num", "IF_Age_Group", "IIF_High_Risk",
        "INDEX_Row_Num", "RANK_BMI", "DISTANCE_To_Hospital_KM", "MODEL_PERCENTILE_BMI"
    ]
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'left')
    
    preview_df = df[preview_cols].head(5).copy()
    preview_df["ABS_BMI_Deviation"] = preview_df["ABS_BMI_Deviation"].round(2)
    preview_df["DISTANCE_To_Hospital_KM"] = preview_df["DISTANCE_To_Hospital_KM"].round(1)
    preview_df["MODEL_PERCENTILE_BMI"] = preview_df["MODEL_PERCENTILE_BMI"].round(3)
    
    print(preview_df.to_string(index=False))

    # Export output
    output_filename = "appendix_cancer_analyzed.csv"
    df.to_csv(output_filename, index=False)
    
    print("\n" + "=" * 128)
    print("PROCESS COMPLETED SUCCESSFULLY".center(128))
    print(f"File Saved       : {os.path.abspath(output_filename)}")
    print(f"Final Dimensions : {df.shape[0]:,} Rows x {df.shape[1]} Columns ({df.shape[1] - 25} new calculated fields added)")
    print("=" * 128 + "\n")

if __name__ == "__main__":
    main()
