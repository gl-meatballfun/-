import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def get_stocks_with_20d_gain_over_100():
    print("正在获取 A 股列表...")
    stock_list = ak.stock_zh_a_spot_em()
    codes = stock_list['代码'].tolist()

    results = []
    total = len(codes)

    # 计算 20 个交易日大概需要 45 个自然日
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=45)).strftime('%Y%m%d')

    print(f"共 {total} 只股票，开始获取近 20 个交易日数据...")

    for i, code in enumerate(codes, 1):
        try:
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq",
            )
            if len(df) < 20:
                continue

            # 取第 -20 个交易日和最新交易日的收盘价
            price_20d_ago = df.iloc[-20]['收盘']
            price_latest = df.iloc[-1]['收盘']
            gain_pct = (price_latest - price_20d_ago) / price_20d_ago * 100

            if gain_pct > 100:
                name = stock_list[stock_list['代码'] == code]['名称'].values[0]
                results.append(
                    {
                        '代码': code,
                        '名称': name,
                        '20交易日涨幅%': round(gain_pct, 2),
                        '20交易日前价格': round(price_20d_ago, 2),
                        '最新价格': round(price_latest, 2),
                    }
                )
                print(f"[{i}/{total}] {code} {name}: +{gain_pct:.2f}%")
            elif i % 100 == 0:
                print(f"进度: {i}/{total}")

        except Exception:
            continue

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('20交易日涨幅%', ascending=False)
    result_df.to_csv(
        'a_share_20d_gain_over_100.csv', index=False, encoding='utf-8-sig'
    )
    print(f"\n完成！共找到 {len(results)} 只涨幅超过 100% 的个股")
    print("结果已保存到 a_share_20d_gain_over_100.csv")
    print(result_df.to_string(index=False))
    return result_df


if __name__ == "__main__":
    get_stocks_with_20d_gain_over_100()
