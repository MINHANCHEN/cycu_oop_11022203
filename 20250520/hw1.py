import pandas as pd

# Load CSV data
df = pd.read_csv('20250520/midterm_scores.csv')

subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

print("\nStudents with more than half of their subjects failing:")
failing_students = []  # 用於儲存超過一半科目不及格學生的資料

for idx, row in df.iterrows():
    failed_count = sum(1 for subj in subjects if row[subj] < 60)
    if failed_count > len(subjects) / 2:
        print(f"{row['Name']} (ID: {row['StudentID']}), Failed {failed_count} subjects")
        failing_students.append({
            'Name': row['Name'],
            'StudentID': row['StudentID'],
            'FailedCount': failed_count
        })

# 將超過一半科目不及格的學生名單寫入 CSV 檔案
failing_students_df = pd.DataFrame(failing_students)
failing_students_df.to_csv('20250520/failing_students_over_half.csv', index=False)
print("\nFailing students list (over half subjects failed) has been saved to '20250520/failing_students_over_half.csv'.")