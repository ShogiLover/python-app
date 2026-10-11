import random

def main():
    # 偽物のコインの候補（1〜9）
    possible_fake_coins = set(range(1, 10))
    
    print("天秤ゲームを開始します。1〜9と書かれた合計9枚のコインがあります。")
    print("その中の1枚は他より重い偽物のコインです。")
    print("天秤を2回だけ使って、偽物のコインを特定してください。\n")

    for i in range(1, 3):
        print(f"--- {i}回目の天秤操作 ---")
        
        while True:
            try:
                num_on_each_side = int(input("左右の天秤に何枚ずつコインを乗せるか選んでください： "))
                if num_on_each_side <= 0 or num_on_each_side > 4:
                    print("1枚から4枚の間で選んでください。")
                    continue
                break
            except ValueError:
                print("数字を入力してください。")

        left_coins = []
        for n in range(1, num_on_each_side + 1):
            while True:
                try:
                    coin = int(input(f"左の天秤に乗せるコインの番号を入力してください。({n}枚目)： "))
                    if coin < 1 or coin > 9:
                        print("1から9の番号を入力してください。")
                    elif coin in left_coins:
                        print("そのコインは既に左の天秤に乗っています。")
                    else:
                        left_coins.append(coin)
                        break
                except ValueError:
                    print("数字を入力してください。")

        right_coins = []
        for n in range(1, num_on_each_side + 1):
            while True:
                try:
                    coin = int(input(f"右の天秤に乗せるコインの番号を入力してください。({n}枚目)： "))
                    if coin < 1 or coin > 9:
                        print("1から9の番号を入力してください。")
                    elif coin in left_coins or coin in right_coins:
                        print("そのコインは既に天秤に乗っています。")
                    else:
                        right_coins.append(coin)
                        break
                except ValueError:
                    print("数字を入力してください。")

        print(f"\n左の天秤に {', '.join(map(str, left_coins))} が、右の天秤に {', '.join(map(str, right_coins))} が乗っています")

        # 後出しで天秤の結果を判定
        candidates_left = possible_fake_coins.intersection(set(left_coins))
        candidates_right = possible_fake_coins.intersection(set(right_coins))
        candidates_balanced = possible_fake_coins.difference(set(left_coins).union(set(right_coins)))

        # 候補が最も多く残る選択肢を選ぶ
        max_size = max(len(candidates_left), len(candidates_right), len(candidates_balanced))
        
        options = []
        if len(candidates_left) == max_size:
            options.append(("left", candidates_left))
        if len(candidates_right) == max_size:
            options.append(("right", candidates_right))
        if len(candidates_balanced) == max_size:
            options.append(("balanced", candidates_balanced))
            
        # タイの場合はランダム（または優先順位）で選択
        choice, next_possible = random.choice(options)
        possible_fake_coins = next_possible

        if choice == "left":
            print("左の天秤が下に傾きました\n")
        elif choice == "right":
            print("右の天秤が下に傾きました\n")
        else:
            print("天秤は水平のままです\n")

    print("回答タイムです。偽物のコインの番号を指定してください。")
    while True:
        try:
            guess = int(input("偽物のコインの番号： "))
            if guess < 1 or guess > 9:
                print("1から9の番号を入力してください。")
                continue
            break
        except ValueError:
            print("数字を入力してください。")

    # 最終判定
    # 候補が2つ以上残っている場合、guess以外のものを正解にする
    if len(possible_fake_coins) > 1:
        other_candidates = list(possible_fake_coins - {guess})
        # もし guess が候補に含まれていなかった場合でも other_candidates は空にならない
        fake_coin = random.choice(other_candidates)
    else:
        fake_coin = list(possible_fake_coins)[0]

    if guess == fake_coin:
        print(f"正解です！おめでとうございます！偽物は {fake_coin} 番でした。")
    else:
        print(f"残念でした。正解は {fake_coin} 番でした。")

if __name__ == "__main__":
    main()
