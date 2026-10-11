import random

def main():
    # 偽物のコイン（1〜9）をランダムに決定
    fake_coin = random.randint(1, 9)
    
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

        # 天秤の判定
        if fake_coin in left_coins:
            print("左の天秤が下に傾きました\n")
        elif fake_coin in right_coins:
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

    if guess == fake_coin:
        print(f"正解です！おめでとうございます！偽物は {fake_coin} 番でした。")
    else:
        print(f"残念でした。正解は {fake_coin} 番でした。")

if __name__ == "__main__":
    main()
