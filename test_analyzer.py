import pandas as pd

def load_data():
    name = input("ファイル名を入力してください")
    df = pd.read_csv(name)
    return df

def analyze_student():
    try:
        df = load_data()
    except FileNotFoundError:
        print("ファイルが見つかりません")
        exit()
    print("\n--- 読み込んだデータの最初の5行 ---")
    print(df.head())
    print("\n--- 読み込んだデータの情報 ---")
    print(df.info())
    problem_columns = [col for col in df.columns if '問題' in col and col != '氏名']
    if not problem_columns:
        print("問題の列が見つかりません。CSVファイルの列名を確認してください。")
        exit()
    print(f"\n--- 検出された問題列: {problem_columns[:5]}... ---")
    min_score_threshold = int(input("抽出したい生徒の最低点数を入力してください: "))
    correct_rate_threshold = 0.8
    problem_correct_rates = df[problem_columns].mean()
    easy_problems = problem_correct_rates[problem_correct_rates >= correct_rate_threshold].index.tolist()
    if not easy_problems:
        print(f"\n正答率{int(correct_rate_threshold*100)}%以上の問題は見つかりませんでした。")
        print("問題のデータが1と0で構成されているか、正答率の閾値を調整してみてください。")
        exit()
    print(f"\n--- 正答率{int(correct_rate_threshold*100)}%以上の問題 (上位5つ): {easy_problems[:5]}... ---")
    if '氏名' in df.columns:
        df['合計点数'] = df[problem_columns].sum(axis=1) # axis=1で行ごとに合計
    else:
        print("\n'氏名'列が見つかりませんでした。生徒の識別には行番号を使用します。")
        df['合計点数'] = df[problem_columns].sum(axis=1)
    target_students_data = []
    for index, student_row in df.iterrows():
        student_name = student_row['氏名'] if '氏名' in df.columns else f"生徒 {index+1}"
        total_score = student_row['合計点数']
        if total_score >= min_score_threshold:
            missed_easy_problems = []
            for problem in easy_problems:
                if student_row[problem] == 0:
                    missed_easy_problems.append(problem)
            if missed_easy_problems:
                target_students_data.append({
                    '氏名': student_name,
                    '合計点数': total_score,
                    '間違えた簡単な問題': ", ".join(missed_easy_problems)
                })
    if target_students_data:
        print(f"\n--- 条件に合致する生徒 ({min_score_threshold}点以上、かつ正答率{int(correct_rate_threshold*100)}%以上の問題を間違えている) ---")
        result_df = pd.DataFrame(target_students_data)
        print(result_df)
    else:
        print(f"\n条件に合致する生徒は見つかりませんでした。")

def analyze_test():
    print("ただ今整備中です。")


def main():
    choise = input("1: 生徒分析 2: 悪問分析")
    if choise == "1":
        analyze_student()
    elif choise == "2":
        analyze_test()
    else:
        print("無効な選択です")

if __name__ == "__main__":
    main()
